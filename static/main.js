class LightStrip {
    constructor(numPixels) {
        this.currentSendWindow = 0;
        this.maxSendWindows = 4;
        this.numPixels = numPixels;
        this.direction = -1;
        this.currentColor = 1;
        this.strip_id = 0;
        this.key = 0;
        this.pixels = new Array(numPixels);
        this.sendWindow = new Array(numPixels);
        this.pathLog = new Array();
        this.logPrintDiv = document.getElementById("info-log");
        this.logPrintDiv.innerHTML = "";
        this.hostname = location.hostname;
        this.port = location.port;
        this.sender = new Sender();

        this.createPixels();
    }

    // Setups

    createPixels() {
        for (let i = 0; i < this.numPixels; i++) {
            this.pixels[i] = new Pixel(null, null, i);
            this.pixels[i].setupIndividual();
        }
        let section_flex = document.createElement("div");
        section_flex.className = "section-flex";
        html.appendSetting(section_flex, "Color Save Number", html.createInputNumber(0, 3, 1, "checkSaveNumber('individual-pixel-save-color')", "individual-pixel-save-color"));
        html.appendSetting(section_flex, "Live", html.createInputCheckBox("Live", "individual-pixels-live-check"));
        html.appendSetting(section_flex, "Resend", html.createButton("Send", "individual-pixels-resend", "lights.resendIndividual()"));
        html.appendSetting(section_flex, "Multiple", [html.createInputNumber(0, 60, 0, null, "individual-pixels-multi-start"), html.createInputNumber(0, 60, 29, null, "individual-pixels-multi-end"), html.createButton("Send", "individual-pixels-multi-send", "lights.setMultiple()")], true);
        document.getElementById("individual-pixels-settings").appendChild(section_flex);
    }

    // Settings

    settingReversed() {
        if (document.getElementById("settings-reversed").checked) {
            lights.direction = -1;
        } else {
            lights.direction = 1;
        }
        lights.reverseStrip();
    }

    setBrightness() {
        let brightness = document.getElementById("settings-brightness").value;
        let path = "settings/brightness=" + brightness;
        this.send(path, false);
    }

    updateHostname() {
        this.hostname = document.getElementById("settings-hostname").value;
        this.updateHost();
    }

    updatePort() {
        this.port = document.getElementById("settings-port").value;
        this.updateHost();
    }

    updateHost() {
        document.getElementById("info-manual-urlbase").innerText = "http://" + this.hostname + ":" + this.port + "/" + this.strip_id + "/" + this.key + "/";
    }

    updateStripId() {
        this.strip_id = document.getElementById("settings-strip-id").value;
        this.updateHost();
    }

    updateKey() {
        this.key = document.getElementById("settings-key").value;
        this.updateHost();
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
        let start_num = parseInt(document.getElementById("individual-pixels-multi-start").value);
        let end_num = parseInt(document.getElementById("individual-pixels-multi-end").value);
        if (start_num >= 0 && end_num < parseInt(this.numPixels) && start_num <= end_num) {
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
            this.send(path, true);
        } else {
            console.log("Error on set multiple start num or end num")
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
        this.send(path, true);
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
            params += this.applyDirection(i) + "." + this.pixels[i].r + "." + this.pixels[i].g + "." + this.pixels[i].b;
            if (i != this.numPixels - 1) {
                params += ",";
            }
        }
        let path = "run/specific/" + params;
        this.send(path, true);
    }

    manual(id, new_window) {
        let path = document.getElementById(id).value;
        if (new_window) {
            this.send(path, true, true);
        } else {
            this.send(path, true);
        }
    }


    // Set Paths

    sendPixel(id, r, g, b) {
        id = this.applyDirection(id);
        let path = "run/single/" + id + "," + r + "," + g + "," + b;
        this.send(path, true);
    }

    colorAll(r, g, b) {
        let path = "run/color/" + r + "," + g + "," + b;
        this.send(path, true);
    }

    wipe(r, g, b, dir, wait_ms) {
        dir *= this.direction;
        let path = "run/wipe/" + r + "," + g + "," + b + "," + dir + "," + wait_ms;
        this.send(path, true);
    }

    chase(r, g, b, wait_ms, interval, dir) {
        dir *= this.direction;
        let path = "animate/chase/" + r + "," + g + "," + b + "," + wait_ms + "," + interval + "," + dir;
        this.send(path, true);
    }

    pulse(type, r, g, b, dir, wait_ms, length, delay) {
        dir *= this.direction;
        let path = type + "/pulse/" + r + "," + g + "," + b + "," + dir + "," + wait_ms + "," + length;
        if (type == "animate") {
            path += "/" + delay;
        }
        this.send(path, true);
    }

    shift(amount, post_delay) {
        amount *= this.direction;
        let path = "run/shift/" + amount + "," + post_delay;
        this.send(path, true);
    }

    animateShift(amount, post_delay) {
        amount *= this.direction;
        let path = "animate/shift/" + amount + "," + post_delay;
        this.send(path, true);
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
        this.send(path, true);
    }

    rainbowChase(wait_ms) {
        let path = "animate/rainbowChase/" + wait_ms;
        this.send(path, true);
    }

    rainbowCycle(wait_ms) {
        let path = "animate/rainbowCycle/" + wait_ms;
        this.send(path, true);
    }

    random(segment_size, wait_ms = 0, repeated = false) {
        let path = "";
        if (repeated) {
            path = "animate/random/" + segment_size + "," + wait_ms;
        } else {
            path = "run/random/" + segment_size + "," + wait_ms;
        }
        this.send(path, true);
    }

    randomCycle(each, wait_ms) {
        let path = "";
        if (each) {
            path = "animate/randomCycle/true," + wait_ms;
        } else {
            path = "animate/randomCycle/false," + wait_ms;
        }
        this.send(path, true);
    }

    reverseStrip() {
        let path = "run/reverse";
        this.send(path, true);
    }

    stopAnimation() {
        let path = "stopanimation";
        this.send(path, true);
    }

    off() {
        let path = "off";
        this.send(path, true);
    }


    // Debug

    printLog() {
        console.log("Printing Log ...");
        for (let i = 0; i < this.pathLog.length; i++) {
            console.log(i, this.pathLog[i]);
        }
    }

    updateLog(text) {
        this.pathLog.push(text);
        this.writeTopLog();
    }

    writeTopLog() {
        let div = document.getElementById("info-log");
        div.innerHTML += this.pathLog[this.pathLog.length - 1] + "\n";
        div.scrollTop = div.scrollHeight;
    }

    // Send

    send(path, send_id_key = true, in_new_window = false) {
        let strip_id_key = "";
        if (send_id_key) {
            strip_id_key = this.key + "/" + this.strip_id + "/";
        }
        let send_url = "http://" + this.hostname + ":" + this.port + "/" + strip_id_key + path;
        if (in_new_window) {
            window.open(send_url, "_blank");
        } else {
            this.sender.send(send_url);
        }
        this.updateLog(path);
    }
}
