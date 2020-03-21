class Controllers {
    constructor() {
        this.brightness_sliders = {};
        this.brightness_number = {};
        sender.add_listen('brightness_change', this, this.set_brightness);
    }

    send_brightness(id) {
        if (!(id in this.brightness_sliders)) {
            console.debug("Saving brightness slider", id);
            this.brightness_sliders[id] = document.getElementById("controller_" + id + "_brightness_slider");
            this.brightness_number[id] = document.getElementById("controller_" + id + "_brightness");
        }
        let value = this.brightness_sliders[id].value;
        sender.emit("set_brightness", [{"id": id, "value": value}]);
    }

    set_brightness(self, data) {
        for (let i = 0; i < 1; i++) {
            console.debug("Setting brightness slider for", data[i]["id"], "to", data[i]["value"]);
            if (data[i]["id"] in self.brightness_sliders) {
                self.brightness_sliders[data[i]["id"]].value = data[i]["value"];
                self.brightness_number[data[i]["id"]].innerText = data[i]["value"];
            }
        }
    }

};