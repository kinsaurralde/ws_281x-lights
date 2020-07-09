class Colors {
    constructor() {
        this.colors = {};
        this.recieved = false;
        this.custom_max = parseInt(document.getElementById("custom_colors").children.length);
        this.custom_pos = parseInt(document.getElementById("custom_colors_count").innerText);
    }

    get(name) {
        if (name in this.colors) {
            return {"r": this.colors[name]["value"]["r"], "g": this.colors[name]["value"]["g"], "b": this.colors[name]["value"]["b"]};
        }
        return {"r": 255, "g": 255, "b": 255}
    }

    get_names() {
        let names = []
        for (let i in this.colors) {
            names.push(i);
        }
        return names
    }

    custom_add() {
        let new_value = this.custom_pos + 1;
        if (new_value <= this.custom_max) {
            document.getElementById("color_" + new_value).style.display = "block";
            this.custom_pos += 1;
        }
    }

    custom_remove() {
        if (this.custom_pos > 0) {
            document.getElementById("color_" + this.custom_pos).style.display = "none";
            this.custom_pos -= 1;
        }
    }
    
    add_color(name, r, g, b) {
        this.colors[name] = {"value": {
            "r": r,
            "g": g,
            "b": b
        }};
    }

    default(name, value=null) {
        if (!(name in this.colors)) {
            this.add_color(name, value[0], value[1], value[2]);
        }
        this.send(name);
    }

    add_defaults(data) {
        let div = document.getElementById("default_colors");
        for (let i in data["colors"]["noedit"]) {
            let color = data["colors"]["noedit"][i]
            this.add_color(color["name"], color["value"][0], color["value"][1], color["value"][2]);
            let button = w.createButton(color["display"], "default_color_" + color["name"], "colors.default('" + color['name'] + "')");
            button.style.margin = ".12vw";
            div.appendChild(button);
        }
        this.recieved = true;
    }

    custom(name, id) {
        if (!(name in this.colors)) {
            this.add_custom(name, id);
        }
        this.send(name);
    }

    add_custom(name, id) {
        let r = document.getElementById(id + "_r");
        let g = document.getElementById(id + "_g");
        let b = document.getElementById(id + "_b");
        this.add_color(name, r.value, g.value, b.value);
        this.colors[name]["divs"] = {"r": r, "g": g, "b": b};
        this.colors[name]["divs"]["r_txt"] = document.getElementById(id + "_r_txt");
        this.colors[name]["divs"]["g_txt"] = document.getElementById(id + "_g_txt");
        this.colors[name]["divs"]["b_txt"] = document.getElementById(id + "_b_txt");
        this.colors[name]["divs"]["display"] = document.getElementById(id + "_display");
    }

    change_color(id) {
        let name = document.getElementById(id + "_name").innerText;
        if (!(name in this.colors)) {
            this.add_custom(name, id);
        }
        let r = this.colors[name]["divs"]["r"].value;
        let g = this.colors[name]["divs"]["g"].value;
        let b = this.colors[name]["divs"]["b"].value;
        this.colors[name]["value"]["r"] = r;
        this.colors[name]["value"]["g"] = g;
        this.colors[name]["value"]["b"] = b;
        this.colors[name]["divs"]["r_txt"].innerText = r;
        this.colors[name]["divs"]["g_txt"].innerText = g;
        this.colors[name]["divs"]["b_txt"].innerText = b;
        this.colors[name]["divs"]["display"].style.backgroundColor = "rgb(" + r + "," + g + "," + b + ")";
    }

    send(name) {
        if (name in this.colors) {
            let color = this.colors[name]['value'];
            let json = {
                "actions": [],
                "options": controllers.get_options()
            };
            if (this._clear_animation()) {
                json["actions"].push({"type": "run", "function": "clear"});
            }
            json["actions"].push({"type": "base", "function": "color", "arguments": {
                "r": color["r"],
                "g": color["g"],
                "b": color["b"]
            }});
            console.log("Sendgin", json);
            sender.emit('action', json);
        }
    }

    _clear_animation() {
        return true
    }
};
