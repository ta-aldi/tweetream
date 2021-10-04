package controllers

import (
	"github.com/beego/beego/v2/server/web"
	"github.com/michaelsusanto81/tweetream/webclient/database"
	"github.com/michaelsusanto81/tweetream/webclient/models"
)

type MainController struct {
	web.Controller
}

func (c *MainController) Get() {
	db := database.GetDB()
	db = append(db, models.Tweet{
		Username: "@michaels",
		Tweet:    "Jakarta lagi macet",
		Type:     "Traffic",
	})
	db = append(db, models.Tweet{
		Username: "@michaels",
		Tweet:    "Jakarta merupakan ibu kota NKRI",
		Type:     "Non Traffic",
	})
	c.Data["tweets"] = db
	c.TplName = "index.tpl"
}
