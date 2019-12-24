class Display {
    constructor(div_id) {
        this.container = document.getElementById(div_id);
        this.num_controllers = 0
        this.controllers = new Array(this.num_controllers);
    }

    setup(data) {
        console.log("Setting up Display with data:", data);
        this.container.innerHTML = "";
        this.num_controllers = data.length;
        this.controllers = new Array(this.num_controllers);
        for (let i = 0; i < this.num_controllers; i++) {
            this.controllers[i] = new Controller(i, data[i]);
            this.container.appendChild(this.controllers[i].get());
        }
    }

    set(data) {
        for (let i = 0; i < this.num_controllers; i++) {
            this.controllers[i].set(data[i]);
        }
    }
};

class Controller {
    constructor(id, data) {
        this.id = id;
        this.container = document.createElement('div');
        this.container.className = "section-flex";
        this.num_strips = data.length;
        this.strips = new Array(this.num_strips);
        for (let i = 0; i < this.num_strips; i++) {
            this.strips[i] = new PixelStrip(data[i]["strip_id"], data[i]["data"].length);
            this.container.appendChild(this.strips[i].get())
        }
    }

    get() {
        return this.container
    }

    set(data) {
        for (let i = 0; i < this.num_strips; i++) {
            this.strips[i].set(data[i]);
        }
    }
};

class PixelStrip {
    constructor(id, num_pixels) {
        this.id = id;
        this.container = document.createElement('div');
        this.container.className = "pixel-display-row";
        this.num_pixels = num_pixels
        this.pixels = new Array(this.num_pixels);
        for (let i = 0; i < this.num_pixels; i++) {
            this.pixels[i] = new Pixel();
            this.container.appendChild(this.pixels[i].get())
        }
    }

    set(data) {
        let colors = data['data'];
        for (let i = 0; i < this.num_pixels; i++) {
            this.pixels[i].set(colors[i]['r'], colors[i]['g'], colors[i]['b']);
        }
    }

    get() {
        console.debug("Pixel Strip", this.id, "container:", this.container);
        return this.container;
    }
};

class Pixel {
    constructor() {
        this.r = 0;
        this.g = 0;
        this.b = 0;
        this.adjust = 50;
        this.container = document.createElement('div');
        this.container.className = "pixel-display";
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

