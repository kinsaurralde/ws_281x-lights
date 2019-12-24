class Sender {
    constructor() {
        this.message_box = document.getElementById("info-messages");
        this.message_box.innerHTML = "";
    }

    send(url, success_func=null) {
        let request = new XMLHttpRequest();
        console.log("Send URL: ", url);
        request.open('GET', url, true);
        request.onload = function () {
            if (this.status >= 200 && this.status < 400) {
                lights.sender.removeBorder();
                let data = JSON.parse(this.response);
                console.log("Recieved Data:", data);
                if (success_func != null) {
                    success_func(data);
                }
                if (data.hasOwnProperty("error") && data["error"].toLowerCase() == "true") {
                    lights.sender.displayWarnBorder();
                    lights.sender.sendWarning(data["message"]);
                }
            } else {
                lights.sender.displayBorder();
                lights.sender.sendError(request.status, request.statusText);
            }
        };
        request.onerror = function () {
            lights.sender.displayBorder();
            lights.sender.sendError(request.status, request.statusText);
        };
        request.send();
    }

    displayBorder() {
        let error_display = document.getElementById("settings-status");
        error_display.style.backgroundColor = "var(--color-red)";
        error_display.value = "Click to see errors";
        let body = document.getElementsByTagName("body")[0];
        body.style.outline = "1vw solid red";
    }

    displayWarnBorder() {
        let error_display = document.getElementById("settings-status");
        error_display.style.backgroundColor = "var(--color-yellow)";
        error_display.value = "Click to see warnings";
        let body = document.getElementsByTagName("body")[0];
        body.style.outline = "1vw solid yellow";
    }

    removeBorder() {
        let error_display = document.getElementById("settings-status");
        error_display.style.backgroundColor = "var(--color-green)";
        error_display.value = "OK";
        let body = document.getElementsByTagName("body")[0];
        body.style.outline = "0vw solid red";
    }

    sendError(status_code, status_text) {
        console.log("Request recieved error:", status_code, status_text);
        switch (status_code) {
            case 0:
                this.message_box.innerHTML += "Connection Refused\n";
                break;
            case 404:
                this.message_box.innerHTML += "Command not found\n";
                break;
            default:
                this.message_box.innerHTML += "Request recieved error: " + status_code + " with message: " + status_text + "\n";
        }
    }

    sendWarning(message) {
        console.log("Request recieved warning with message:", message);
        this.message_box.innerHTML += message + "\n";
    }
}
