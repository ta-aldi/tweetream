package services

import (
	"encoding/json"
	"fmt"
	"log"
	"os"
	"strings"

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
	excluded_topics := strings.Split(os.Getenv("EXCLUDE_TOPICS"), ",")
	topics := []string{}
	for key, _ := range metadata.Topics {
		isExcluded := false

		for _, excluded_topic := range excluded_topics {
			if key == excluded_topic {
				isExcluded = true
				break
			}
		}

		if !isExcluded {
			topics = append(topics, key)
		}
	}

	return topics
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
