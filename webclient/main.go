package main

import (
	"github.com/beego/beego/v2/server/web"
	"github.com/michaelsusanto81/tweetream/webclient/controller"
)

func main() {
	web.Router("/", &controller.MainController{})
	web.Run()
}
