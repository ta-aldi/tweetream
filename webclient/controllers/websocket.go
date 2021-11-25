package controllers

import (
	"fmt"
	"net/http"

	"github.com/beego/beego/v2/server/web"
	"github.com/gorilla/websocket"
	"github.com/michaelsusanto81/tweetream/webclient/services"
)

type WebSocketController struct {
	web.Controller
}

func (wsc *WebSocketController) Connect() {
	// Get user-requested Topic
	topic := "TW-" + wsc.GetString("topic")

	// Upgrade from http request to WebSocket.
	ws, err := websocket.Upgrade(wsc.Ctx.ResponseWriter, wsc.Ctx.Request, nil, 1024, 1024)
	if _, ok := err.(websocket.HandshakeError); ok {
		http.Error(wsc.Ctx.ResponseWriter, "Not a websocket handshake", 400)
		return
	} else if err != nil {
		err_msg := fmt.Sprintf("Cannot setup WebSocket connection: %v", err)
		http.Error(wsc.Ctx.ResponseWriter, err_msg, 400)
		return
	}

	// Subscribe to Kafka
	services.Subscribe(ws, topic)
}
