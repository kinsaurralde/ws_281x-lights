class LightStrip {
    constructor(numPixels) {
        this.currentSendWindow = 0;
        this.maxSendWindows = 4;
        this.numPixels = numPixels;
        this.direction = -1;
        this.currentColor = 1;
        this.pixels = new Array(numPixels);
        this.sendWindow = new Array(numPixels);
        this.pathLog = new Array();

        this.createPixels();
        this.createSendWindows();
    }

    // Setups

    createPixels() {
        for (let i = 0; i < this.numPixels; i++) {
            this.pixels[i] = new Pixel(i);
        }
        let section_flex = document.createElement("div");
        section_flex.className = "section-flex";
        html.appendSetting(section_flex, "Color Save Number", html.createInputNumber(0, 3, 1,  "checkSaveNumber('individual-pixel-save-color')", "individual-pixel-save-color"));
        html.appendSetting(section_flex, "Live", html.createInputCheckBox("Live", "individual-pixels-live-check"));
        html.appendSetting(section_flex, "Resend", html.createButton("Send", "individual-pixels-resend", "lights.resendIndividual()"));
        html.appendSetting(section_flex, "Multiple", [html.createInputNumber(0, 60, 0,  null, "individual-pixels-multi-start"), html.createInputNumber(0, 60, 29,  null, "individual-pixels-multi-end"),html.createButton("Send", "individual-pixels-multi-send", "lights.setMultiple()")], true);
        document.getElementById("individual-pixels-settings").appendChild(section_flex);
    }


    createSendWindows() {
        for (let i = 0; i < this.maxSendWindows; i++) {
            this.sendWindow[i] = document.getElementById("send-data-" + i);
        }
    }

    // Other

    applyDirection(id) {
        if (this.direction == 1) {
            return id;
        } else {
            return this.numPixels - id - 1;
        }
    }

    updatePixel(id, r, g, b) {
        this.pixels[id].setPixel(r, g, b);
    }

    updateAllPixels(r, g, b) {
        for (let i = 0; i < this.numPixels; i++) {
            this.updatePixel(i, r, g, b);
        }
    }

    setIndividual(id) {
        let update_individual = document.getElementById("individual-pixels-live-check").checked;
        if (update_individual) {
            let color = getSaveColor(document.getElementById("individual-pixel-save-color").value);
            let r = color.r;
            let g = color.g;
            let b = color.b;
            this.updatePixel(id, r, g, b);
            this.updateColorDisplay(id);
            this.sendPixel(id, r, g, b);
        }
    }

    setMultiple() {
        let start_num = document.getElementById("individual-pixels-multi-start").value;
        let end_num = document.getElementById("individual-pixels-multi-end").value;
        if (start_num >= 0 && end_num < this.numPixels) {
            let color = getSaveColor(document.getElementById("individual-pixel-save-color").value);
            let r = color.r;
            let g = color.g;
            let b = color.b;
            let params = "";
            for (let i = start_num; i <= end_num; i++) {
                i = this.applyDirection(i);
                params += i + "." + r + "." + g + "." + b;
                if (this.applyDirection(i) != end_num) {
                    params += ",";
                }
                this.updatePixel(this.applyDirection(i), r, g, b);
                this.updateColorDisplay(this.applyDirection(i));
                i = this.applyDirection(i);
            }
            let path = "run/specific/" + params;
            this.send(path, false);
        }
    }

    sendMultiple(data) {
        let params = "";
        for (let i = 0; i < data.length; i++) {
            let start = data[i].start;
            let end = data[i].end;
            let r = data[i].r;
            let g = data[i].g;
            let b = data[i].b;
            for (let j = start; j <= end; j++) {
                params += this.applyDirection(j) + "." + r + "." + g + "." + b + ",";
                this.updatePixel(j, r, g, b);
                this.updateColorDisplay(j);
            }
        }
        params = params.slice(0, -1)
        let path = "run/specific/" + params + "0";
        this.send(path, false);
    }

    updateColorDisplay(id) {
        let current = document.getElementById("pixel-display-" + id);
        let r = this.pixels[id].r;
        let g = this.pixels[id].g;
        let b = this.pixels[id].b;
        current.style.backgroundColor = "rgb(" + r + "," + g + "," + b + ")";
    }

    resendIndividual() {
        let params = "";
        for (let i = 0; i < this.numPixels; i++) {
            params += i + "." + this.pixels[i].r + "." + this.pixels[i].g + "." + this.pixels[i].b;
            if (i != this.numPixels - 1) {
                params += ",";
            }
        }
        let path = "run/specific/" + params;
        this.send(path, false);
    }




    // Set Paths

    sendPixel(id, r, g, b) {
        id = this.applyDirection(id);
        //this.updatePixel(id, r, g, b);
        let path = "run/single/" + id + "," + r + "," + g + "," + b;
        this.send(path, true);
    }

    colorAll(r, g, b) {
        let path = "run/color/" + r + "," + g + "," + b;
        //this.updateAllPixels(r, g, b);
        this.send(path, true);
    }

    wipe(r, g, b, dir, wait_ms) {
        dir *= this.direction;
        let path = "run/wipe/" + r + "," + g + "," + b + "," + dir + "," + wait_ms;
        //this.updateAllPixels(r, g, b);
        this.send(path, false);
    }

    chase(r, g, b, wait_ms) {
        let path = "animate/chase/" + r + "," + g + "," + b + "," + wait_ms;
        //this.updateAllPixels(r, g, b);
        this.send(path, true);
    }

    pulse(type, r, g, b, dir, wait_ms, length, delay) {
        dir *= this.direction;
        let path = type + "/pulse/" + r + "," + g + "," + b + "," + dir + "," + wait_ms + "," + length;
        if (type == "animate") {
            path += ",1," + delay;
        }
        this.send(path, false);
    }

    shift(amount, post_delay) {
        amount *= this.direction;
        let path = "operations/shift/" + amount + "," + post_delay;
        this.send(path, false);
    }

    animateShift(amount, post_delay) {
        amount *= this.direction;
        let path = "animate/shift/" + amount + "," + post_delay;
        this.send(path, false);
    }

    switch(wait_ms, instant, id, max_num, loop_start) {
        if (instant) {
            wait_ms *= -1;
        }
        let color_string = "";
        for (let i = 0; i < max_num; i++) {
            color_string += ",";
            let current_color_save = document.getElementById(id + i).value;
            let color = getSaveColor(current_color_save, id + i);
            color_string += color.r + "." + color.g + "." + color.b;
        }
        if (loop_start || max_num < 2) {
            let current_color_save = document.getElementById(id + 0).value;
            let color = getSaveColor(current_color_save);
            color_string += "," + color.r + "." + color.g + "." + color.b;
        }
        let path = "animate/mix/" + wait_ms + color_string;
        this.send(path, false);
    }

    rainbowChase(wait_ms) {
        let path = "animate/rainbowChase/" + wait_ms;
        this.updateAllPixels(0, 0, 0);
        this.send(path, true);
    }

    rainbowCycle(wait_ms) {
        let path = "animate/rainbowCycle/" + wait_ms;
        this.updateAllPixels(0, 0, 0);
        this.send(path, true);
    }

    random(each) {
        
    }

    randomCycle(each, wait_ms) {
        let path = "";
        if (each) {
            path = "animate/randomCycle/true," + wait_ms;
        } else {
            path = "animate/randomCycle/false," + wait_ms;
        }
        this.updateAllPixels(0, 0, 0);
        this.send(path, true);
    }

    setBrightness() {
        let brightness = document.getElementById("settings-brightness").value;
        let path = "settings/brightness=" + brightness;
        this.send(path, false);
    }

    reverseStrip() {
        let path = "reverse";
        this.send(path, false);
    }

    stopAnimation() {
        let path = "stopanimation";
        this.send(path, true);
    }

    off() {
        let path = "off";
        this.updateAllPixels(0, 0, 0);
        this.send(path, true);
    }




    // Debug

    printLog() {
        console.log("Printing Log ...");
        for (let i = 0; i < this.pathLog.length; i++) {
            console.log(i,this.pathLog[i]);
        }
    }

    // Send

    send(path) {
        console.log("Send Window:", this.currentSendWindow, "Sending:", path);
        this.sendWindow[this.currentSendWindow].src = path;
        this.currentSendWindow = (this.currentSendWindow + 1) % this.maxSendWindows;
	this.pathLog.push(path);
    }
}

class Pixel {
    constructor(id) {
        this.id = id;
        this.r = 0;
        this.g = 0;
        this.b = 0;
        this.display_div;
        this.setup();
    }

    setup() {
        let target = document.getElementById("pixel-holder");
        let div = document.createElement("div");
        div.className = "pixel-display";
        div.id = "pixel-display-"+this.id;
        let onoverfunc = "lights.setIndividual("+this.id+")";
        div.onmouseover = new Function(onoverfunc);
        target.appendChild(div);
        this.display_div = document.getElementById("pixel-display-"+this.id); 
    }

    setPixel(r, g, b) {
        this.r = r;
        this.g = g;
        this.b = b;
        this.display_div.style.backgroundColor = "rgb(" + r + "," + g + "," + b + ")";
    }
}
