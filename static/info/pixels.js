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
        for (let i in data) {
            let id = data[i]["controller_id"];
            if (!(id in this.controllers)) {
                this._redraw(data[i]);
            }
            this.controllers[id].set(data[i]);
        }  
    }

    set_brightness(data) {
        console.log("DAAT", data, this);
        for (let i in data) {
            if (data[i]["id"] in this.controllers) {
                this.controllers[data[i]["id"]].set_brightness(data[i]["value"]);
            }
        }
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
        this.container.appendChild(w.createDivider());
        this.strip = new PixelStrip(this.disp_id, this.id, data["pixels"].length);
        this.container.appendChild(this.strip.get());

        this.update = true;
    }

    _getButtons() {
        let div = document.createElement('div');
        div.className = "section-flex-no-border";
        div.appendChild(w.create125Text("Controller: " + this.id));
        div.appendChild(w.createVDivider());
        div.appendChild(w.create125Text("Update:"));
        div.appendChild(w.createSpacerS1());
        this.div_should_update = w.createInputCheckBox("Update", this.disp_id + "-update", true);
        div.appendChild(this.div_should_update);
        div.appendChild(w.createVDivider());
        div.appendChild(w.create125Text("Brightness:"))
        div.appendChild(w.createSpacerS1());
        this.div_brightness = w.create125Text("---", "controller_" + this.id + "_brightness");
        div.appendChild(this.div_brightness);
        div.appendChild(w.createVDivider());
        div.appendChild(w.create125Text("Power Usage (W):"));
        div.appendChild(w.createSpacerS1());
        this.div_power = w.create125Text("---");
        div.appendChild(this.div_power);
        return div
    }

    get() {
        return this.container
    }

    set_brightness(value) {
        this.div_brightness.innerText = value;
    }

    set(data) {
        if (this.div_should_update.checked) {
            this.strip.set(data["pixels"]);
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

    set(data) {
        console.debug(data);
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

