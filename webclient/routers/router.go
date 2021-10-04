package routers

import (
	"github.com/beego/beego/v2/server/web"
	"github.com/michaelsusanto81/tweetream/webclient/controllers"
)

func init() {
	web.Router("/", &controllers.MainController{})
}
