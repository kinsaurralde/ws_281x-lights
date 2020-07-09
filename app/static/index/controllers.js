class Controllers {
    constructor() {
        this.divs = {}
        sender.add_listen('brightness_change', this, this.set_brightness);
        sender.add_listen('framerate_change', this, this.set_framerate);
        this._init_divs();
        this.last_brightness = Date.now();
        this.last_framerate = Date.now();
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
            this.divs[id]["animation_framerate_slider"] = document.getElementById("controller_" + id + "_animation_framerate_slider");
            this.divs[id]["animation_framerate_number"] = document.getElementById("controller_" + id + "_animation_framerate_number");
            this.divs[id]["animation_multiplier"] = document.getElementById("controller_" + id + "_animation_multiplier");
            this.divs[id]["brightness_slider"] = document.getElementById("controller_" + id + "_brightness_slider");
            this.divs[id]["brightness_number"] = document.getElementById("controller_" + id + "_brightness");
            this.divs[id]["send"] = document.getElementById("controller_" + id + "_send");
        }
    }

    send_brightness(id) {
        console.log("id", id);
        this._div_saved(id);
        let value = this.divs[id]["brightness_slider"].value;
        sender.emit("set_brightness", [{"id": id, "value": value}]);
        this.last_brightness = Date.now();
    }

    send_framerate(id) {
        console.log("id", id);
        this._div_saved(id);
        let value = this.divs[id]["animation_framerate_slider"].value;
        let multiplier = this.divs[id]["animation_multiplier"].value;
        sender.emit("set_framerate", [{"id": id, "data": {"animation": value, "animation_multiplier": multiplier}}]);
        this.last_brightness = Date.now();
    }

    set_brightness(self, data) {
        console.debug("Setting brightness", data);
        let update = Date.now() - self.last_brightness > 500
        for (let i = 0; i < 1; i++) {
            let id = data[i]["id"];
            self._div_saved(id);
            self.divs[id]["brightness_number"].innerText = data[i]["value"];
            if (update) {
                self.divs[id]["brightness_slider"].value = data[i]["value"];
            }
        }
    }

    set_framerate(self, data) {
        console.debug("Setting framerate", data);
        let update = Date.now() - self.last_framerate > 500
        for (let i = 0; i < 1; i++) {
            let id = data[i]["id"];
            self._div_saved(id);
            let animation_multiplier = data[i]["value"]["animation_multiplier"];
            let animation_framerate = data[i]["value"]["animation_framerate"];
            self.divs[id]["animation_framerate_number"].innerText = animation_framerate * animation_multiplier;
            if (update) {
                self.divs[id]["animation_framerate_slider"].value = animation_framerate;
                self.divs[id]["animation_multiplier"].value = animation_multiplier;
            }
        }
    }

    set_send(id) {
        this._div_saved(id);
    }

    get_options() {
        let controllers = []
        for (let controller in this.divs) {
            if (this.divs[controller]["send"].checked) {
                controllers.push(controller);
            }
        }   
        return {"controllers": controllers}
    }
};
