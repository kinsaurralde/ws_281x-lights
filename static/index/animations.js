class Animations {
    constructor() {
        //let self = this;
        //sender.get('/config/animations', this.add_animations, self);
        this.table = document.getElementById("animations_table");
        this.rows = {};
    }

    add_animations(data) {
        for (let i in data["animations"]) {
            this._add_row(data["animations"][i]);
        }
    }

    send(id) {
        console.log("sending", id);
    }

    row_colors(id, action, args) {
        if (id in this.rows) {
            this.rows[id].row_colors(action, args);
        }
    }

    _add_row(row_data) {
        let id = this._pick_id();
        this.rows[id] = new Row(id, row_data["name"], row_data["display"], row_data["arguments"]);
        this.rows[id].create();
        let row = this.table.insertRow();
        let cells = this.rows[id].get();
        for (let i = 0; i < cells.length; i++) {
            let cell = row.insertCell();
            cell.appendChild(cells[i]);
        }
    }

    _pick_id() {
        let id = Math.floor(Math.random() * 1000);
        while (id in this.rows) {
            id = Math.floor(Math.random() * 1000);
        }
        return id
    }
};

class Row {
    constructor(id, name, display, args) {
        this.id = id;
        this.name = name;
        this.display = display;
        this.args = args;
        this.cells = [];
    }

    create() {
        for (let i = 0; i < 9; i++) {
            let blank = document.createElement("div");
            blank.className = "text-1-25";
            blank.innerText = "---";
            this.cells.push(blank);
        }
        this.cells[0] = w.createButton("Send", null, "animations.send('" + this.id + "')");
        this.cells[0].style.width = "5vw";
        this.cells[1] = this._color(["NONE"], false);
        this.cells[2] = document.createTextNode(this.display);
        if ("color" in this.args) {
            this.cells[3] = this._color(this.args["color"], true);
        }
        this.cells[4] = this._wait_ms(100);
        if ("wait_ms" in this.args) {
            this.cells[4] = this._wait_ms(this.args["wait_ms"]);
        }
        if ("arg1" in this.args) {
            this.cells[5] = this._arg(this.args["arg1"]);
        }
        if ("arg2" in this.args) {
            this.cells[6] = this._arg(this.args["arg2"]);
        }
        if ("arg3" in this.args) {
            this.cells[7] = this._arg(this.args["arg3"]);
        }
    }

    get() {
        return this.cells
    }

    row_colors(action, args) {
        if (action == "delete") {
            let div = document.getElementById("animations_color_" + this.id + "_" + args);
            if (div.value == "NONE" && div.parentElement.children.length > 2) {
                div.parentNode.removeChild(div);
            }
        } else if (action == "add") {
            let button = document.getElementById("animations_color_" + this.id + "_plus");
            let div = button.parentElement;
            let i = div.children.length;
            let color_names = colors.get_names();
            div.insertBefore(this._create_color(color_names[0], color_names, true, i), button);
        }
    }

    _color(defaults, multiple=false) {
        let div = document.createElement("div");
        let color_names = ["NONE"];
        color_names.push(...colors.get_names());
        for (let i = 0; i < defaults.length; i++) {
            div.appendChild(this._create_color(defaults[i], color_names, true, i));
        }
        if (multiple) {
            let button = w.createButton("+", "animations_color_" + this.id + "_plus", "animations.row_colors('" + this.id + "', 'add', null)");
            button.className = "small-button";
            div.appendChild(button);
        }
        return div
    }

    _create_color(value, color_names, multiple, i) {
        let select = w.createSelect(value, "animations_color_" + this.id, color_names);
        if (multiple) {
            select.className = "small-select";
            select.id = "animations_color_" + this.id + "_" + i;
            select.oninput = new Function("animations.row_colors('" + this.id + "', 'delete', '" + i + "')");
        }
        return select
    }

    _wait_ms(value) {
        let input = w.createNumber(value, "animations_wait_ms_" + this.id);
        input.min = 1;
        return input
    }

    _arg(data) {
        console.log("Daa", data);
        let div = document.createElement("div");
        let input = document.createElement("div");
        let text = document.createTextNode(data["name"] + ": ");
        div.appendChild(text);
        let id = "animations_" + this.id + "_arg1";
        if (data["type"] == "int") {
            input = w.createNumber(data["default"], id);
            input.min = data["min"];
        } else if (data["type"] == "option") {
            input = w.createSelect(data["default"], id, data["options"])
        } else if (data["type"] == "bool") {
            input = w.createSelect(data["default"], id, [{"name": "True", "value": true}, {"name": "False", "value": false}])
        }
        input.style.width = "3.5vw";
        div.appendChild(input);
        return div
    }
};
