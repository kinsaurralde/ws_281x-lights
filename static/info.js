class Info {
    constructor() {
        this.location = document.getElementById("info-section");
        this.table = document.getElementById("info-table");
        this.controllers_div = document.getElementById("controllers");
        this.pixels = [];
        this.isSetup = false;
        this.data = [];
        this.refresh();

    }

    setup(data) {
        console.log("Setting up with:", data);
        let controllers = [];
        for (let i = 0; i < data.length; i++) {
            controllers.push(this.addController(data[i], i));
        }
        this.isSetup = true;
        this.pixels = controllers;
    }

    refresh() {
        this.send("/info/get");
    }

    recieveData(data) {
        this.data = data;
        if (this.isSetup == false) {
            this.setup(data);
        }
        this.clearTable();
        if (data.length != this.pixels.length) {
            location.reload();
        }
        for (let i = 0; i < this.pixels.length; i++) {
            this.appendRow(data[i], i);
            if (data[i]["error"] == false) {
                for (let j = 0; j < data[i]["strips"].length; j++) {
                    for (let k = 0; k < data[i]["strips"][j]["data"].length; k++) {
                        let pixel_data = data[i]["strips"][j]["data"][k];
                        this.pixels[i]["strips"][j][k].setPixel(pixel_data.r, pixel_data.g, pixel_data.b);
                    }
                }
            }
        }
    }

    appendRow(data, i) {
        console.log("Data:", data, i);
        let row = this.table.insertRow();
        for (let j = 0; j < 10; j++) {
            row.insertCell();
        }
        if (data["error"] == false) {
            this.table.rows[this.table.rows.length - 1].cells[0].innerHTML = i;
            this.table.rows[this.table.rows.length - 1].cells[1].innerHTML = data["power"]["now_watts"].toFixed(3) + " / " + data["power"]["strip_max"];
            this.table.rows[this.table.rows.length - 1].cells[2].innerHTML = data["power"]["max_watts"];
            this.table.rows[this.table.rows.length - 1].cells[3].innerHTML = data["settings"]["brightness"];
            this.table.rows[this.table.rows.length - 1].cells[4].innerHTML = data["settings"]["num_pixels"];
            this.table.rows[this.table.rows.length - 1].cells[5].innerHTML = data["strip_info"].length;
            this.table.rows[this.table.rows.length - 1].cells[6].innerHTML = data["ping"].toFixed(3);
        } else {
            for (let i = 0; i < this.table.rows[this.table.rows.length - 1].cells.length - 2; i++) {
                this.table.rows[this.table.rows.length - 1].cells[i].innerHTML = " --- ";
            }
        }
        this.table.rows[this.table.rows.length - 1].cells[7].innerHTML = data["enabled"][0] + " / " + data["enabled"][1];
        let button_e = document.createElement("input");
        button_e.type = "button";
        button_e.value = "Enable";
        button_e.onclick = new Function("info.toggle_enable(" + i + ", true)");
        this.table.rows[this.table.rows.length - 1].cells[8].appendChild(button_e);
        let button_d = document.createElement("input");
        button_d.type = "button";
        button_d.value = "Disable";
        button_d.onclick = new Function("info.toggle_enable(" + i + ", false)");
        this.table.rows[this.table.rows.length - 1].cells[9].appendChild(button_d);
    }

    clearTable() {
        let table_size = this.table.rows.length;
        for (let i = 1; i < table_size; i++) {
            this.table.deleteRow(1);
        }
    }

    addController(data, id) {
        console.log("Add Controller: ", data);
        let div = document.createElement("div");
        div.innerHTML = "Controller: " + id;
        if (data["error"] == true) {
            return
        }
        let strips = [];
        for (let i = 0; i < data["strips"].length; i++) {
            let strips_div = document.createElement("div");
            strips_div.className = "section-flex";
            let strip_info = document.createElement("div");
            strip_info.className = "text-1-25";
            strip_info.innerHTML = i + ": ";
            strips_div.appendChild(strip_info);
            strips.push(this.addStrip(strips_div, data["strips"][i], id));
            div.appendChild(strips_div);
        }
        this.controllers_div.appendChild(div);
        let divider = document.createElement("div");
        divider.className = "divider";
        this.controllers_div.appendChild(divider);
        return {
            "id": id,
            "strips": strips,
        };
    }

    addStrip(div, data, controller_id) {
        let pixels = [];
        for (let i = 0; i < data["data"].length; i++) {
            pixels.push(new Pixel(controller_id, data["strip_id"], i, div));
            pixels[i].setupInfo();
        }
        return pixels;
    }

    toggle_enable(controller_id, enable) {
        let key = document.getElementById("webkey-value").value; 
        if (enable) {
            this.send("/" + key + "/controllers/enable/" + controller_id);
        } else {
            this.send("/" + key + "/controllers/disable/" + controller_id);
        }
    }

    send(path) {
        let url = path;
        let request = new XMLHttpRequest();
        console.log("Sending:", url)
        request.open('GET', url, true);
        request.onload = function () {
            console.log("Status code: ", this.status);
            if (this.status >= 200 && this.status < 400) {
                let data = JSON.parse(this.response);
                console.log("Recieved Data:", data);
                info.recieveData(data);
            } else {
                console.log("There was an error");
            }
        };
        request.onerror = function () {
            console.log("Connection Error: ", this.status, request);
        };
        request.send();
    }
}
