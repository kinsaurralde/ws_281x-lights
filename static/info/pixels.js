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

    redraw(data) {
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
            this.redraw(data);
        }
        if (this.controllers[id].isDifferent(data["strip_info"])) {
            this.redraw(data);
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
        let title = document.createElement('div');
        title.className = "text-1-25";
        title.innerText = "Controller: " + this.id;
        this.container.appendChild(title);
        this.num_strips = data["strip_info"].length;
        this.strips = new Array(this.num_strips);
        for (let i = 0; i < this.num_strips; i++) {
            this.addPixelStrip(i, data["strip_info"][i]);
        }
        this.strip_info = data["strip_info"];
    }

    addPixelStrip(i, data) {
        this.strips[i] = new PixelStrip(this.disp_id, data["id"], data["end"] - data["start"] + 1);
        let divider = document.createElement('div');
        divider.className = "divider";
        divider.style.width = "100%";
        this.container.appendChild(divider);
        this.container.appendChild(this.strips[i].get());
    }

    isDifferent(strip_info) {
        if (strip_info.length != this.strip_info.length) {
            return true
        }
        return false
    }

    get() {
        return this.container
    }

    set(data) {
        for (let i = 0; i < this.num_strips; i++) {
            let info = data["strip_info"][i];
            this.strips[i].set(data["pixels"].slice(info["start"], info["end"] + 1));
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
        for (let i = 0; i < this.num_pixels; i++) {
            this.pixels[i].set(data[i]['r'], data[i]['g'], data[i]['b']);
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

    set(r = 0, g = 0, b = 0) {
        this.r = r;
        this.g = g;
        this.b = b;
        this.container.style.backgroundColor = "rgb(" + (r + this.adjust) + "," + (g + this.adjust) + "," + (b + this.adjust) + ")";
    }

    get() {
        return this.container;
    }
}

