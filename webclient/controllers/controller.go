package controllers

import (
	"encoding/json"
	"log"
	"os"

	"github.com/beego/beego/v2/server/web"
	"github.com/joho/godotenv"
	"github.com/michaelsusanto81/tweetream/webclient/models"
	"github.com/michaelsusanto81/tweetream/webclient/services"
)

type MainController struct {
	web.Controller
}

func (c *MainController) Get() {
	c.TplName = "index.html"
	Response := services.GetTopics()
	c.Data["topics"] = Response

	// load .env credentials
	err_env := godotenv.Load(".env")
	if err_env != nil {
		log.Fatalf(err_env.Error())
	}

	// pass streamer server IP address information
	c.Data["STREAMER_SERVER"] = os.Getenv("STREAMER_SERVER")
}

func (c *MainController) GetTopics() {
	Response := services.GetTopics()
	c.Data["json"] = Response
	c.ServeJSON()
}

func (c *MainController) CreateTopic() {
	// parse json input
	var topic models.TweetreamTopic
	json.Unmarshal(c.Ctx.Input.RequestBody, &topic)

	// create topic
	err := services.CreateTopic(topic.Name)

	// return responses
	if err != nil {
		c.Ctx.ResponseWriter.WriteHeader(500)
		c.Data["json"] = map[string]interface{}{"error": err.Error()}
	} else {
		c.Ctx.ResponseWriter.WriteHeader(201)
		c.Data["json"] = map[string]interface{}{"msg": "Success"}
	}
	c.ServeJSON()
}

func (c *MainController) DeleteTopic() {
	// parse json input
	var topic models.TweetreamTopic
	json.Unmarshal(c.Ctx.Input.RequestBody, &topic)

	// delete topic
	err := services.DeleteTopic(topic.Name)

	// return responses
	if err != nil {
		c.Ctx.ResponseWriter.WriteHeader(500)
		c.Data["json"] = map[string]interface{}{"error": err.Error()}
	} else {
		c.Ctx.ResponseWriter.WriteHeader(201)
		c.Data["json"] = map[string]interface{}{"msg": "Success"}
	}
	c.ServeJSON()
}
