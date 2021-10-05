package services

import (
	"encoding/json"
	"fmt"
	"log"
	"os"

	"github.com/confluentinc/confluent-kafka-go/kafka"
	"github.com/gorilla/websocket"
	"github.com/joho/godotenv"
	"github.com/michaelsusanto81/tweetream/webclient/models"
)

func Subscribe(ws *websocket.Conn) {
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
	consumer.SubscribeTopics([]string{os.Getenv("TOPICS_SUB")}, nil)

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
