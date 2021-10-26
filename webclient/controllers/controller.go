package controllers

import (
	"github.com/beego/beego/v2/server/web"
	"github.com/michaelsusanto81/tweetream/webclient/services"
)

type MainController struct {
	web.Controller
}

func (c *MainController) Get() {
	c.TplName = "index.html"
}

func (c *MainController) GetTopics() {
	Response := services.GetTopics()
	c.Data["json"] = Response
	c.ServeJSON()
}
