class Controllers {
    constructor() {
        this.divs = {}
        sender.add_listen('brightness_change', this, this.set_brightness);
        this._init_divs();
    }

    _init_divs() {
        let controllers = document.getElementById("controller_table").rows;
        for (let i = 1; i < controllers.length; i++) {
            this._div_saved(controllers[i].cells[0].innerText);
        }
    }

    _div_saved(id) {
        if (!(id in this.divs)) {
            console.debug("Saving divs of", id);
            this.divs[id] = {};
            this.divs[id]["brightness_slider"] = document.getElementById("controller_" + id + "_brightness_slider");
            this.divs[id]["brightness_number"] = document.getElementById("controller_" + id + "_brightness");
            this.divs[id]["send"] = document.getElementById("controller_" + id + "_send");
        }
    }

    send_brightness(id) {
        this._div_saved(id);
        let value = this.divs[id]["brightness_slider"].value;
        sender.emit("set_brightness", [{"id": id, "value": value}]);
    }

    set_brightness(self, data) {
        for (let i = 0; i < 1; i++) {
            let id = data[i]["id"];
            console.debug("Setting brightness slider for", id, "to", data[i]["value"]);
            self._div_saved(id);
            self.divs[id]["brightness_slider"].value = data[i]["value"];
            self.divs[id]["brightness_number"].innerText = data[i]["value"];
        }
    }

    set_send(id) {
        this._div_saved(id);
        let checked = this.divs[id]["send"].checked;
        if (id == "ALL" && checked) {
            for (let controller in this.divs) {
                if (controller != "ALL") {
                    this.divs[controller]["send"].checked = false;
                }
            } 
        } else if (id != "ALL" && checked) {
            if (this.divs["ALL"]["send"].checked) {
                this.divs[id]["send"].checked = false;
            }
        }
    }

    get_options() {
        let vcontrollers = []
        for (let controller in this.divs) {
            if (this.divs[controller]["send"].checked) {
                vcontrollers.push(controller);
            }
        }   
        return {"virtual_controllers": vcontrollers}
    }

};