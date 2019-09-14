class Generic {
    constructor() {
        this.rows = [];
        this.functions = generic_functions;
        this.table = document.getElementById("generic-table");
    }

    add_row(initial) {
        let row = this.table.insertRow();
        for (let i = 0; i < 12; i++) {
            let cell = row.insertCell();
        }
        this.rows.push(new GenericRow(initial, this.rows.length, this));
    }

    remove_row() {
        if (this.rows.length > 0) {
            this.rows.pop();
            this.table.deleteRow(this.table.rows.length - 1);
        }
    }

    recreateAll() {
        for (let i = 0; i < this.rows.length; i++) {
            this.rows[i].create();
        }
    }


};

class GenericRow {
    constructor(initial_function, num, generic) {
        this.data = {
            "controllers": "default",
            "strip_id": "default",
            "function": initial_function,
        };
        this.num = num;
        this.id = "generic-row-" + this.num + "-";
        this.generic = generic;
        this.table = document.getElementById("generic-table");
        this.create();
    }

    create() {
        for (let i = 0; i < 12; i++) {
            this.table.rows[this.num + 1].cells[i].innerHTML = "";
        }
        let id = this.id;
        let func = this.data["function"];
        let func_data = this.generic.functions[func];

        let cell = this.table.rows[this.num + 1].cells[0];
        cell.appendChild(html.createText5(this.data["controllers"], id + "controllers"));

        cell = this.table.rows[this.num + 1].cells[1];
        cell.appendChild(html.createSelect(this.data["strip_id"], id + "strip_id", this.getStripIds("default")));

        cell = this.table.rows[this.num + 1].cells[2];
        cell.appendChild(html.createSelect(this.getValue("types"), id + "type", func_data["types"]));

        cell = this.table.rows[this.num + 1].cells[3];
        cell.appendChild(html.createSelect(func, id + "function", Object.keys(generic.functions), "generic.rows[" + this.num + "].update()"));

        cell = this.table.rows[this.num + 1].cells[4];
        if (func_data.hasOwnProperty("color")) {
            cell.appendChild(html.createText5(this.getValue("color"), id + "color"));
        } else {
            cell.appendChild(html.createNONE(id + "color"))
        }

        cell = this.table.rows[this.num + 1].cells[5];
        if (func_data.hasOwnProperty("wait_ms")) {
            cell.appendChild(html.createNumber(this.getValue("wait_ms"), id + "wait_ms"));
        } else {
            cell.appendChild(html.createNONE(id + "wait_ms"))
        }

        cell = this.table.rows[this.num + 1].cells[6];
        if (func_data.hasOwnProperty("wait_mode")) {
            cell.appendChild(html.createSelect(this.getValue("wait_mode"), id + "wait_mode", func_data["wait_mode"]));
        } else {
            cell.appendChild(html.createNONE(id + "wait_mode"))
        }

        cell = this.table.rows[this.num + 1].cells[7];
        if (func_data.hasOwnProperty("direction")) {
            cell.appendChild(html.createSelect(this.getValue("direction"), id + "direction", func_data["direction"]));
        } else {
            cell.appendChild(html.createNONE(id + "direction"))
        }

        cell = this.table.rows[this.num + 1].cells[8];
        if (func_data.hasOwnProperty("num_value")) {
            cell.innerHTML = func_data["num_value"]["label"];
            cell.innerHTML += ": ";
            cell.appendChild(html.createNumber(this.getValue("num_value"), id + "num_value"));
        } else {
            cell.appendChild(html.createNONE(id + "num_value"))
        }

        cell = this.table.rows[this.num + 1].cells[9];
        if (func_data.hasOwnProperty("option")) {
            cell.innerHTML = func_data["option"]["label"];
            cell.innerHTML += ": ";
            if (func_data["option"].hasOwnProperty("mode")) {
                if (func_data["option"]["mode"] == "number") {
                    cell.appendChild(html.createNumber(this.getValue("option"), id + "option", null))
                }
            } else {
                cell.appendChild(html.createSelect(this.getValue("option"), id + "option", func_data["option"]["default"]));
            }
        } else {
            cell.appendChild(html.createNONE(id + "option"))
        }

        cell = this.table.rows[this.num + 1].cells[11];
        cell.appendChild(html.createButton("Send", id + "send", "generic.rows[" + this.num + "].send()"));
    }

    update() {
        this.getValues();
        this.create();
    }

    updateStripId() {
        this.data["controllers"] = document.getElementById("generic-row-" + this.num + "-controllers").value;
        let cell = this.table.rows[this.num + 1].cells[1];
        cell.innerHTML = "";
        cell.appendChild(html.createSelect("default", this.id + "strip_id", this.getStripIds(this.data["controllers"])));
    }

    getStripIds(controller) {
        let values = ["default"];
        let max_len = 0;
        if (lights.controller_data.length > 0) {
            let controllers = this.getControllers(controller);
            for (let i = 0; i < controllers.length; i++) {
                let cur = lights.controller_data[controllers[i]]["strips"].length;
                if (cur > max_len) {
                    max_len = cur;
                }
            }
        }
        for (let i = 0; i < max_len; i++) {
            values.push(i);
        }
        return values;
    }

    getControllers(value) {
        if (value == "default") {
            value = lights.controllers;
        } else {
            value = value.split(',');
        }
        let values = [];
        for (let i = 0; i < value.length; i++) {
            if (value[i] < lights.controller_data.length) {
                values.push(value[i]);
            }
        }
        return values;
    }

    getValues() {
        let properties = ["controllers", "strip_id", "type", "function", "color", "wait_ms", "wait_mode", "num_value", "direction", "option"];
        for (let i = 0; i < properties.length; i++) {
            let cur_value = document.getElementById("generic-row-" + this.num + "-" + properties[i]).value;
            if (cur_value == "---") {
                this.data[properties[i]] = null;
            } else {
                this.data[properties[i]] = cur_value;
            }
        }
    }

    process() {
        let value = []
        value["controller_ids"] = this.data["controllers"];
        value["strip_id"] = this.data["strip_id"];
        if (value["controller_ids"] == "default") {
            value["controller_ids"] = lights.controllers;
        }
        if (value["strip_id"] == "default") {
            value["strip_id"] = lights.strip_id;
        }
        value["key_ids"] = lights.key + ":" + value["controller_ids"] + ":" + value["strip_id"];
        let func_data = this.generic.functions[this.data["function"]];
        if (this.data["color"] != null) {
            if (func_data["color"]["mode"] == "single") {
                let cur_color = getSaveColor(this.data["color"], this.id + "color");
                value["r"] = cur_color["r"];
                value["g"] = cur_color["g"];
                value["b"] = cur_color["b"];
            } else {
                value["colors"] = colorsToStr(getSaveColors(this.id + "color"));
            }
        }
        value["dir"] = 1;
        if (this.data["direction"] != null) {
            if (this.data["direction"] == "left") {
                value["dir"] = -1;
            }
        }
        value["wait_mode"] = "false";
        if (this.data["wait_mode"] != null) {
            let accept = ["full", "Full", "Instant", "fraction"];
            if (accept.includes(this.data["wait_mode"])) {
                value["wait_mode"] = "true";
            }
        }
        value["option"] = "false";
        if (this.data["option"] != null) {
            value["option"] = this.data["option"];
        }
        value["iterations"] = 1;
        if (value["type"] == "run") {
            value["iterations"] = 0;
        }
        value["wait_ms"] = this.data["wait_ms"];
        value["num_value"] = this.data["num_value"];
        value["type"] = this.data["type"];
        return value;
    }

    send() {
        this.getValues();
        let data = this.process()
        switch (this.data["function"]) {
            case "color":
                lights.colorAll(data["r"], data["g"], data["b"], data["key_ids"]);
                break;
            case "random":
                lights.random(data["num_value"], data["wait_ms"], data["type"], data["key_ids"]);
                break;
            case "wipe":
                lights.wipe(data["r"], data["g"], data["b"], data["dir"], data["wait_ms"], data["type"], data["wait_mode"], data["key_ids"]);
                break;
            case "single":
                lights.sendPixel(data["num_value"], data["r"], data["g"], data["b"], data["key_ids"]);
                break;
            case "pulse":
                lights.pulse(data["type"], data["r"], data["g"], data["b"], data["dir"], data["wait_ms"], data["num_value"], data["option"], data["wait_mode"],0, data["key_ids"]);
                break;
            case "chase":
                lights.chase(data["r"], data["g"], data["b"], data["wait_ms"], data["num_value"], data["dir"], data["option"], data["key_ids"]);
                break;
            case "shift":
                lights.shift(data["num_value"] * data["dir"], data["wait_ms"], data["type"], data["key_ids"]);
                break;
            case "rainbowCycle":
                lights.rainbowCycle(data["type"], data["wait_ms"], data["dir"], data["wait_mode"], data["iterations"], data["key_ids"]);
                break;
            case "rainbowChase":
                lights.rainbowChase(data["type"], data["wait_ms"], data["dir"], data["iterations"], data["key_ids"]);
                break;
            case "mix":
                lights.switch(data["type"], data["colors"], data["wait_ms"], data["wait_mode"], data["option"], data["key_ids"]);
                break;
            case "reverse":
                lights.reverseStrip(data["key_ids"]);
                break;
            case "bounce":
                lights.bounce(data["type"], data["colors"], data["wait_ms"], data["num_value"], data["dir"], data["option"], data["wait_mode"], data["key_ids"]);
                break;
            case "pattern":
                lights.pattern(data["colors"], data["num_value"], data["wait_mode"], data["option"], data["key_ids"]);
                break;
            case "blend":
                lights.blend(data["num_value"], data["wait_ms"], data["option"], data["key_ids"])
                break;
            case "fade":
                lights.fade(data["num_value"], data["wait_ms"], data["option"], 100, data["key_ids"]);
                break;
        }
    }

    getValue(property) {
        if (Array.isArray(this.generic.functions[this.data["function"]][property])) {
            return this.generic.functions[this.data["function"]][property][0];
        }
        return this.generic.functions[this.data["function"]][property]["default"][0];
    }
}

function addGeneric() {
    generic.add_row(Object.keys(generic_functions)[Math.floor(Math.random() * Object.keys(generic_functions).length)]);
}

function removeGeneric() {
    generic.remove_row();
}
