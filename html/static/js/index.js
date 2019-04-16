var bus = new Vue()

let tpos = localStorage._timelinesPositions
let json = tpos?JSON.parse(tpos):'{}'

var sockets = {}


var app = new Vue({
    el: '#main'
    , data: {
        url: "ws://127.0.0.1:8004/"
        , messages: []
        , apiKey: 'api_key_1'
        , connected: false
        , message: 'Hello World.'
        , time: 1000
    }

    , methods: {
        connect(){
            this.push('connecting')
            let url = `${this.url}?api_key=${this.apiKey}`
            let socket = sockets[this] = this.newSocket(url)
        }

        , push(item) {
            return this.messages.push(item)
        }

        , newSocket(url) {
            let ws = new WebSocket(url);

            ws.onopen = function(ev){
                this.onOpen(ws, ev)
            }.bind(this)

            ws.onclose = function(ev){
                this.onClose(ws, ev)
            }.bind(this)

            ws.onmessage = function(ev){
                this.onMessage(ws, ev)
            }.bind(this)

            ws.onerror = function(ev){
                this.onError(ws, ev)
            }.bind(this)

            return ws
        }

        , close() {
            sockets[this].close()
        }

        , send(){
            if(this.message.length > 0){
                sockets[this].send(this.message)
                //this.message = ''
            }
        }

        , onOpen(socket, ev) {
            this.push(`onOpen ${socket}`)
            console.log(socket, ev)
            this.connected = true
        }
        , onClose(socket, ev) {
            this.push(`onClose ${socket}`)
            console.log(socket, ev)
            this.connected = false
        }
        , onMessage(socket, ev) {
            this.push(ev.data)
        }

        , onError(socket, ev) {
            console.error(socket, ev)
            this.push(`Error: ${ev}`)
        }

        , toggleTicker(){
            T=0

            if(this.timer){
                clearInterval(this.timer)
                delete this.timer
                return
            }

            this.timer = setInterval(function(){
                T++
                if(app.connected){
                    app.close()
                }else {
                    app.messages=[]
                    app.connect()
                }
            }, this.time);
        }
    }


})

