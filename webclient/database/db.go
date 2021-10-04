package database

import "github.com/michaelsusanto81/tweetream/webclient/models"

var DB []models.Tweet

func InitDB() {
	DB = []models.Tweet{}
}

func GetDB() []models.Tweet {
	if DB == nil {
		InitDB()
	}
	return DB
}
