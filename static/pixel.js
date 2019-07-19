class Pixel {
    constructor(controller_id, strip_id, id, parent_div) {
        this.controller_id = controller_id;
        this.strip_id = strip_id;
        this.id = id;
        this.r = 0;
        this.g = 0;
        this.b = 0;
        this.display_div = parent_div;
    }

    setupInfo() {
        let div = document.createElement("div");
        div.className = "pixel-display";
        div.id = "pixel-display-" + this.controller_id + "-" + this.strip_id + "-" + this.id;
        this.display_div.appendChild(div);
        this.display_div = document.getElementById("pixel-display-" + this.controller_id + "-" + this.strip_id + "-" + this.id);
    }

    setupIndividual() {   // For sending individual pixels
        let target = document.getElementById("pixel-holder");
        let div = document.createElement("div");
        div.className = "pixel-display";
        div.id = "pixel-display-" + this.id;
        let onoverfunc = "lights.setIndividual(" + this.id + ")";
        div.onmouseover = new Function(onoverfunc);
        target.appendChild(div);
        this.display_div = document.getElementById("pixel-display-" + this.id);
    }

    setPixel(r, g, b) {
        this.r = r;
        this.g = g;
        this.b = b;
        this.display_div.style.backgroundColor = "rgb(" + r + "," + g + "," + b + ")";
    }
}