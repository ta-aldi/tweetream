package models

import "time"

type Tweet struct {
	Username  string
	Tweet     string
	Type      string
	CreatedAt time.Time
}
