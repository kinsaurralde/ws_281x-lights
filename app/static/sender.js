class Sender {
    constructor() {
        this.socket = io();
        this.socket.on('connection_response', function() {
            console.log("Now Connected");
        });
    }

    add_listen(message, self, response) {
        this.socket.on(message, function(data) {
            response(self, data);
        });
    }

    emit(message, json, response=null) {
        this.socket.emit(message, json, function(data) {
            if (response != null) {
                response(data);
            }
        });
    }

    post(url, json, success_func=null) {
        let request = new XMLHttpRequest();
        let data = JSON.stringify(json);
        request.open('POST', url, true);
        request.setRequestHeader("Content-type", "application/json");
        console.log("POST", url, data);
        request.onload = function () {
            if (this.status >= 200 && this.status < 400) {
                let data = JSON.parse(this.response);
                console.log("Recieved Data:", data);
                if (success_func != null) {
                    success_func(data);
                }
            } else {
                console.log("Error", this.response);
            }
        };
        request.send(data);
    }

    get(url, success_func=null) {
        let request = new XMLHttpRequest();
        request.open('GET', url, true);
        request.setRequestHeader("Content-type", "application/json");
        console.log("GET", url);
        request.onload = function() {
            if (this.status >= 200 && this.status < 400) {
                let data = JSON.parse(this.response);
                console.log("Received Data:", data);
                if (success_func != null) {
                    success_func(data);
                }
            } else {
                console.log("Error", this.response);
            }
        };
        request.send();
    }
};
