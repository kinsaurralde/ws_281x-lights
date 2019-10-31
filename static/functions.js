class Functions {
    constructor(self) {
        this.sender = new Sender();
        this.data = [];
        this.self = self;
    }

    create_buttons(data) {
        let div = document.getElementById("functions-buttons");
        div.innerHTML = "";
        for (let i = 0; i < data.length; i++)  {
            let name = data[i].split('.')[0]
            let id = "function-button-" + name;
            let button = html.createButton(name.replace('_', ' '), id, "func.run('" + name + "')");
            let spacer = html.createSpacerS1()
            div.appendChild(button);
            div.appendChild(spacer);
        }
    }

    disp_vars(data) {
        window.open().document.write("<pre>" + JSON.stringify(data[0]["variables"], null, 2) + "</pre>")
    }

    list() {
        let send_url = "http://" + lights.hostname + ":" + lights.port + "/saved/functions/list";
        this.sender.send(send_url, func.create_buttons);
    }

    list_vars() {
        let send_url = "http://" + lights.hostname + ":" + lights.port + "/info/get";
        this.sender.send(send_url, func.disp_vars);
    }

    run(name) {
        let path = "saved/functions/run/" + name;
        let send_url = "http://" + lights.hostname + ":" + lights.port + "/" + path;
        this.sender.send(send_url);
        lights.updateLog(path);
    }
}