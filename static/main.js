class LightStrip {
    constructor(numPixels) {
        this.numPixels = numPixels;
        this.direction = -1;
        this.strip_id = 0;
        this.controllers = [0];
        this.controller_data = [];
        this.key = 0;
        this.pixels = new Array(numPixels);
        this.pathLog = new Array();
        this.logPrintDiv = document.getElementById("info-log");
        this.logPrintDiv.innerHTML = "";
        this.hostname = location.hostname;
        this.port = location.port;
        this.sender = new Sender();

        this.createPixels();
        if (this.hostname != "kinsaurralde.com") {
            this.getInfo();
        }
    }

    // Setups

    createPixels() {
        for (let i = 0; i < this.numPixels; i++) {
            this.pixels[i] = new Pixel(null, null, i);
            this.pixels[i].setupIndividual();
        }
        let section_flex = document.createElement("div");
        section_flex.className = "section-flex";
        html.appendSetting(section_flex, "Color Save Number", html.createNumber(1, "individual-pixel-save-color", "checkSaveNumber('individual-pixel-save-color')"));
        html.appendSetting(section_flex, "Live", html.createInputCheckBox("Live", "individual-pixels-live-check"));
        html.appendSetting(section_flex, "Resend", html.createButton("Send", "individual-pixels-resend", "lights.resendIndividual()"));
        html.appendSetting(section_flex, "Multiple", [html.createNumber(0, "individual-pixels-multi-start"), html.createNumber(29, "individual-pixels-multi-end"), html.createButton("Send", "individual-pixels-multi-send", "lights.setMultiple()")], true);
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
        let path = "settings/" + this.controllers + "/brightness=" + brightness;
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
        document.getElementById("info-manual-urlbase").innerText = "http://" + this.hostname + ":" + this.port + "/" + this.key + ":" + this.controllers + ":" + this.strip_id + "/";
    }

    updateStripId() {
        this.strip_id = document.getElementById("settings-strip-id").value;
        this.updateHost();
    }

    updateKey() {
        this.key = document.getElementById("settings-key").value;
        this.updateHost();
    }

    updateControllers() {
        this.controllers = document.getElementById("settings-controllers").value;
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
        console.log("REMOVE updatePixels")
        this.pixels[id].setPixel(r, g, b);
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

    sendPixel(id, r, g, b, ids=null) {
        id = this.applyDirection(id);
        let path = "run/single/" + id + "," + r + "," + g + "," + b;
        this.send(path, ids);
    }

    colorAll(r, g, b, ids=null) {
        let path = "run/color/" + r + "," + g + "," + b;
        if (ids == null) {
            this.send(path, true);
        } else {
            this.send(ids + "/" + path, false);
        }
    }

    wipe(r, g, b, dir, wait_ms, mode="run", wait_mode=false, ids = null) {
        dir *= this.direction;
        let path = mode + "/wipe/" + r + "," + g + "," + b + "," + dir + "," + wait_ms + "," + wait_mode;
        this.send(path, ids);
    }

    chase(r, g, b, wait_ms, interval, dir, layer=false, ids=null) {
        dir *= this.direction;
        let path = "animate/chase/" + r + "," + g + "," + b + "," + wait_ms + "," + interval + "," + dir + "," + layer;
        this.send(path, ids);
    }

    pulse(type, r, g, b, dir, wait_ms, length, layer, wait_total, delay, ids=null) {
        dir *= this.direction;
        let path = type + "/pulse/" + r + "," + g + "," + b + "," + dir + "," + wait_ms + "," + length + "," + layer + "," + wait_total;
        if (type == "animate") {
            path += "/" + delay;
        }
        this.send(path, ids);
    }

    shift(amount, post_delay, type="run", ids=null) {
        amount *= this.direction;
        let path = type + "/shift/" + amount + "," + post_delay;
        this.send(path, ids);
    }

    switch(type, colors, wait_ms, instant, loop_start, ids=null) {
        if (loop_start == "True") {
            colors += ";" + colors.split(';')[0];
        }
        let path = type + "/mix/" + colors + "," + wait_ms + "," + instant;
        this.send(path, ids);
    }

    rainbowChase(type, wait_ms, direction=1, iterations=1, ids=null) {
        direction *= this.direction;
        let path = type + "/rainbowChase/" + wait_ms + "," + direction + "," + iterations;
        this.send(path, ids);
    }

    rainbowCycle(type, wait_ms, direction=1, wait_total=false, iterations=1,  ids=null) {
        direction *= this.direction;
        let path = type + "/rainbowCycle/" + wait_ms + "," + direction + "," + wait_total + "," + iterations;
        this.send(path, ids);
    }

    random(segment_size, wait_ms = 0, repeated = false, ids=null) {
        let path = "";
        if (repeated === true) {
            path = "animate/random/";
        } else if (repeated === false) {
            path = "run/random/"
        } else {
            path = repeated + "/random/"
        }
        this.send(path + segment_size + "," + wait_ms, ids);
    }

    bounce(type, colors, wait_ms, length, direction, layer, wait_mode, ids=null) {
        direction *= this.direction;
        let path = type + "/bounce/" + colors + "," + wait_ms + "," + length + "," + direction + "," + layer + "," + wait_mode;
        this.send(path, ids);
    }

    reverseStrip(ids=null) {
        let path = "run/reverse";
        this.send(path, ids);
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

    send(path, send_id_key = null, in_new_window = false) {
        let strip_id_key = "";
        if (send_id_key == null || send_id_key == true) {
            strip_id_key = this.key + ":" + this.controllers + ":" + this.strip_id + "/";
        } else if (send_id_key != false) {       
            strip_id_key = send_id_key + "/";
        }
        let send_url = "http://" + this.hostname + ":" + this.port + "/" + strip_id_key + path;
        if (in_new_window) {
            window.open(send_url, "_blank");
        } else {
            this.sender.send(send_url);
        }
        this.updateLog(path);
    }

    getInfo() {
        let url = "http://" + this.hostname + ":" + this.port + "/info/get";
        document.getElementById("settings-hostname").value = this.hostname;
        document.getElementById("settings-port").value = this.port;
        this.updateHost();
        this.sender.send(url, this.recieveData);
    }

    recieveData(data) {
        lights.controller_data = data;
        generic.recreateAll();
    }
}
