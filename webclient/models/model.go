package models

type Tweet struct {
	Username  string `json:"username"`
	Tweet     string `json:"text"`
	Type      string `json:"prediction"`
	CreatedAt string `json:"created_at"`
}
