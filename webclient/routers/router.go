package routers

import (
	"github.com/beego/beego/v2/server/web"
	"github.com/michaelsusanto81/tweetream/webclient/controllers"
)

func init() {
	web.Router("/", &controllers.MainController{})
	web.Router("/topics", &controllers.MainController{}, "get:GetTopics")
	web.Router("/topics", &controllers.MainController{}, "post:CreateTopic")
	web.Router("/topics", &controllers.MainController{}, "delete:DeleteTopic")

	web.Router("/ws", &controllers.WebSocketController{}, "get:Connect")
}
