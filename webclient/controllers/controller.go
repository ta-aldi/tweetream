package controllers

import (
	"log"
	"os"

	"github.com/beego/beego/v2/server/web"
	"github.com/joho/godotenv"
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
