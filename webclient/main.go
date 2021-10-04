package main

import (
	"github.com/beego/beego/v2/server/web"
	_ "github.com/michaelsusanto81/tweetream/webclient/routers"
)

func main() {
	web.Run()
}
