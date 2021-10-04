package controllers

import (
	"time"

	"github.com/beego/beego/v2/server/web"
	"github.com/michaelsusanto81/tweetream/webclient/database"
	"github.com/michaelsusanto81/tweetream/webclient/models"
)

type MainController struct {
	web.Controller
}

func (c *MainController) Get() {
	db := database.GetDB()
	time1, _ := time.Parse(time.RubyDate, "Mon Oct 04 12:05:41 +0000 2021")
	db = append(db, models.Tweet{
		Username:  "@michaels",
		Tweet:     "Jakarta lagi macet",
		Type:      "Traffic",
		CreatedAt: time1,
	})
	db = append(db, models.Tweet{
		Username:  "@michaels",
		Tweet:     "Jakarta merupakan ibu kota NKRI",
		Type:      "Non Traffic",
		CreatedAt: time1,
	})
	c.Data["tweets"] = db
	c.TplName = "index.tpl"
}
