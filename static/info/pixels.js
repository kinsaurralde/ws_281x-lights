class Display {
    constructor(div_id) {
        this.id = div_id
        this.container = document.getElementById(this.id);
        this.num_controllers = 0
        this.controllers = new Object();
    }

    setup(data) {
        let id = data["controller_id"]
        this.controllers[id] = new Controller(this.id, id, data);
        this.num_controllers++;
        this.container.appendChild(this.controllers[id].get());
    }

    _redraw(data) {
        this.container.innerHTML = "";
        for (let key in this.controllers) {
            if (key != data["controller_id"]) {
                this.container.appendChild(this.controllers[key].get());
            }
        }
        this.setup(data);
    }

    set(data) {
        let id = data["controller_id"];
        if (!(id in this.controllers)) {
            this._redraw(data);
        }
        if (this.controllers[id].isDifferent(data["strip_info"])) {
            this._redraw(data);
        }
        this.controllers[id].set(data);
    }
};

class Controller {
    constructor(disp_id, id, data) {
        console.debug("Creating controller", id, "with:", data);
        this.id = id;
        this.disp_id = disp_id + "-" + this.id;
        this.container = document.createElement('div');
        this.container.className = "section-flex";
        this.container.id = this.disp_id;
        this.container.appendChild(this._getButtons());
        this.container_expanded = document.createElement('div');
        this.container_expanded.className = "section-flex-no-border";
        this.container_expanded.style.display = "none";
        this.num_strips = data["strip_info"].length;
        this.strips = new Array(this.num_strips);
        for (let i = 0; i < this.num_strips; i++) {
            this._addPixelStrip(i, data["strip_info"][i]);
        }
        this.container.appendChild(this.container_expanded);
        this.strip_info = data["strip_info"];
        this.update = true;
    }

    _addPixelStrip(i, data) {
        this.strips[i] = new PixelStrip(this.disp_id, data["id"], data["end"] - data["start"] + 1);
        if (i == 0) {
            this.container.appendChild(w.createDivider());
            this.container.appendChild(this.strips[i].get());
        } else {
            this.container_expanded.appendChild(w.createDivider());
            this.container_expanded.appendChild(this.strips[i].get());
        }
    }

    _getButtons() {
        let self = this;
        let div = document.createElement('div');
        div.className = "section-flex-no-border";
        div.appendChild(w.create125Text("Controller: " + this.id));
        div.appendChild(w.createVDivider());
        div.appendChild(w.create125Text("Update:"));
        div.appendChild(w.createSpacerS1());
        this.div_should_update = w.createInputCheckBox("Update", this.disp_id + "-update", true);
        div.appendChild(this.div_should_update);
        div.appendChild(w.createVDivider());
        div.appendChild(w.create125Text("Show Expanded:"));
        div.appendChild(w.createSpacerS1());
        this.div_show_expanded = w.createInputCheckBox("Show Expanded", this.disp_id + "-show-expanded", false);
        this.div_show_expanded.onclick = function() {
            self.show_expanded(self);
        };
        div.appendChild(this.div_show_expanded);
        div.appendChild(w.createVDivider());
        div.appendChild(w.create125Text("Brightness:"))
        div.appendChild(w.createSpacerS1());
        this.div_brightness = w.create125Text("---");
        div.appendChild(this.div_brightness);
        div.appendChild(w.createVDivider());
        div.appendChild(w.create125Text("Power Usage (W):"));
        div.appendChild(w.createSpacerS1());
        this.div_power = w.create125Text("---");
        div.appendChild(this.div_power);
        return div
    }

    test() {
        console.log(this.id);
    }

    isDifferent(strip_info) {
        if (strip_info.length != this.strip_info.length) {
            return true
        }
        for (let i = 0; i < strip_info.length; i++) {
            if (strip_info[i]["start"] != this.strip_info[i]["start"] || strip_info[i]["end"] != this.strip_info[i]["end"]) {
                return true
            }
        }
        return false
    }

    _setUpdate(self) {
        self.update = self.div_should_update.checked;
    }

    show_expanded(self) {
        if (self.div_show_expanded.checked) {
            self.container_expanded.style.display = "flex";
        } else {
            self.container_expanded.style.display = "none";
        }
    }

    get() {
        return this.container
    }

    set(data) {
        if (this.div_should_update.checked) {
            this.div_brightness.innerText = data["brightness"];
            //this.div_power.innerText = data["power"].toFixed(3);
            for (let i = 0; i < this.num_strips; i++) {
                let info = data["strip_info"][i];
                this.strips[i].set(data["pixels"].slice(info["start"], info["end"] + 1));
            }
        }
    }
};

class PixelStrip {
    constructor(disp_id, id, num_pixels) {
        console.debug("Creating pixelstrip", id, "with", num_pixels);
        this.id = id;
        this.disp_id = disp_id + "-" + this.id;
        this.container = document.createElement('div');
        this.container.className = "pixel-display-row";
        this.num_pixels = num_pixels;
        this.pixels = new Array(this.num_pixels);
        for (let i = 0; i < this.num_pixels; i++) {
            this.pixels[i] = new Pixel(this.disp_id, i);
            this.container.appendChild(this.pixels[i].get())
        }
    }

    show() {

    }

    hide() {

    }

    set(data) {
        for (let i = 0; i < this.num_pixels; i++) {
            this.pixels[i].set(data[i]);
        }
    }

    get() {
        console.debug("Pixel Strip", this.id, "container:", this.container);
        return this.container;
    }
};

class Pixel {
    constructor(disp_id, id) {
        this.id = id;
        this.disp_id = disp_id + "-" + this.id;
        this.r = 0;
        this.g = 0;
        this.b = 0;
        this.adjust = 50;
        this.container = document.createElement('div');
        this.container.className = "pixel-display";
        this.container.id = this.disp_id;
        this.set();
    }

    set(value = 0) {
        this.r = (value >> 16) & 0xFF;
        this.g = (value >> 8) & 0xFF;
        this.b = value & 0xFF;
        this.container.style.backgroundColor = "rgb(" + (this.r + this.adjust) + "," + (this.g + this.adjust) + "," + (this.b + this.adjust) + ")";
    }

    get() {
        return this.container;
    }
}

