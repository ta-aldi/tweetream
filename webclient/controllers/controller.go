package controllers

import (
	"encoding/json"
	"fmt"
	"log"
	"os"

	"github.com/beego/beego/v2/server/web"
	"github.com/joho/godotenv"
	"github.com/michaelsusanto81/tweetream/webclient/database"
	"github.com/michaelsusanto81/tweetream/webclient/models"
	"gopkg.in/confluentinc/confluent-kafka-go.v1/kafka"
)

type MainController struct {
	web.Controller
}

func (c *MainController) Get() {
	var (
		data models.Tweet
	)
	db := database.GetDB()
	err_env := godotenv.Load(".env")
	if err_env != nil {
		log.Fatalf(err_env.Error())
	}

	consumer, err := kafka.NewConsumer(&kafka.ConfigMap{
		"bootstrap.servers": os.Getenv("KAFKA_SERVERS"),
		"group.id":          os.Getenv("GROUP_ID"),
		"auto.offset.reset": "earliest",
	})

	if err != nil {
		panic(err)
	}

	consumer.SubscribeTopics([]string{os.Getenv("TOPICS_SUB")}, nil)

	for {
		msg, err := consumer.ReadMessage(-1)
		if err == nil {
			data = models.Tweet{}
			json.Unmarshal(msg.Value, &data)

			db = append([]models.Tweet{data}, db...)
			fmt.Println(db)
			// c.Data["tweets"] = db
			// c.TplName = "index.tpl"
		} else {
			// The client will automatically try to recover from all errors.
			fmt.Printf("Consumer error: %v (%v)\n", err, msg)
		}
	}

	consumer.Close()

}
