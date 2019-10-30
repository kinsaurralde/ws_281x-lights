class Functions {
    constructor() {
        this.sender = new Sender();
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

    list() {
        let send_url = "http://" + lights.hostname + ":" + lights.port + "/saved/functions/list";
        this.sender.send(send_url, func.create_buttons);
    }

    run(name) {
        let send_url = "http://" + lights.hostname + ":" + lights.port + "/saved/functions/run/" + name;
        this.sender.send(send_url);
    }
}