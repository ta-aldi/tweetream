package services

import (
	"context"
	"encoding/json"
	"errors"
	"fmt"
	"log"
	"os"
	"time"

	"github.com/confluentinc/confluent-kafka-go/kafka"
	"github.com/gorilla/websocket"
	"github.com/joho/godotenv"
	"github.com/michaelsusanto81/tweetream/webclient/models"
)

func GetTopics() []string {
	// load .env credentials
	err_env := godotenv.Load(".env")
	if err_env != nil {
		log.Fatalf(err_env.Error())
	}

	// create Kafka Admin client
	admin, err := kafka.NewAdminClient(&kafka.ConfigMap{
		"bootstrap.servers": os.Getenv("KAFKA_SERVERS"),
	})
	if err != nil {
		panic(err)
	}

	// get all metadata
	metadata, err := admin.GetMetadata(nil, true, 5000)
	if err != nil {
		panic(err)
	}

	// list all topics
	topics := []string{}
	for key, _ := range metadata.Topics {
		if key[0:3] == "TW-" {
			topics = append(topics, key[3:])
		}
	}

	return topics
}

func CreateTopic(topic string) error {

	// load .env credentials
	err_env := godotenv.Load(".env")
	if err_env != nil {
		return err_env
	}

	// create Kafka Admin client
	adminClient, err := kafka.NewAdminClient(&kafka.ConfigMap{
		"bootstrap.servers": os.Getenv("KAFKA_SERVERS"),
	})
	if err != nil {
		return err
	}

	// Contexts are used to abort or limit the amount of time
	// the Admin call blocks waiting for a result.
	ctx, cancel := context.WithCancel(context.Background())
	defer cancel()

	// Create topics on cluster.
	// Set Admin options to wait for the operation to finish (or at most 60s)
	maxDuration, err := time.ParseDuration("60s")
	if err != nil {
		return errors.New("time.ParseDuration(60s)")
	}

	results, err := adminClient.CreateTopics(ctx,
		[]kafka.TopicSpecification{{
			Topic:             topic,
			NumPartitions:     2,
			ReplicationFactor: 2}},
		kafka.SetAdminOperationTimeout(maxDuration))

	if err != nil {
		err_msg := fmt.Sprintf("Problem during the topic creation: %v\n", err)
		return errors.New(err_msg)
	}

	// Check for specific topic errors
	for _, result := range results {
		if result.Error.Code() != kafka.ErrNoError &&
			result.Error.Code() != kafka.ErrTopicAlreadyExists {
			err_msg := fmt.Sprintf("Topic creation failed for %s: %v",
				result.Topic, result.Error.String())
			return errors.New(err_msg)
		}
	}

	adminClient.Close()
	return nil
}

func Subscribe(ws *websocket.Conn, topic string) {
	var (
		data models.Tweet
	)

	// load .env credentials
	err_env := godotenv.Load(".env")
	if err_env != nil {
		log.Fatalf(err_env.Error())
	}

	// create Kafka Consumer client
	consumer, err := kafka.NewConsumer(&kafka.ConfigMap{
		"bootstrap.servers": os.Getenv("KAFKA_SERVERS"),
		"group.id":          os.Getenv("GROUP_ID"),
		"auto.offset.reset": "earliest",
	})
	if err != nil {
		panic(err)
	}

	// subscribe to topic
	consumer.SubscribeTopics([]string{topic}, nil)

	// listen for close event from client
	go func(ws *websocket.Conn, consumer *kafka.Consumer) {
		for {
			_, message, err := ws.ReadMessage()
			if err != nil || string(message) == "close" {
				ws.Close()
				consumer.Close()
				return
			}
		}
	}(ws, consumer)

	// poll messages
	for {
		msg, err := consumer.ReadMessage(-1)
		if err == nil {
			// bind message to struct (for future use)
			data = models.Tweet{}
			json.Unmarshal(msg.Value, &data)

			// encode struct into  bytes
			enc_data, err_enc := json.Marshal(data)
			if err_enc != nil {
				fmt.Println("Fail to marshal event")
				break
			}

			// send message into websocket clients
			if ws != nil {
				if ws.WriteMessage(websocket.TextMessage, enc_data) != nil {
					break
				}
			}
		} else {
			// The client will automatically try to recover from all errors.
			fmt.Printf("Consumer error: %v (%v)\n", err, msg)
		}
	}

	// close connections
	consumer.Close()
	ws.Close()
}
