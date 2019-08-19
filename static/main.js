class LightStrip {
    constructor(numPixels) {
        this.currentSendWindow = 0;
        this.maxSendWindows = 4;
        this.numPixels = numPixels;
        this.direction = -1;
        this.currentColor = 1;
        this.strip_id = 0;
        this.controllers = [0];
        this.controller_data = [];
        this.key = 0;
        this.pixels = new Array(numPixels);
        this.sendWindow = new Array(numPixels);
        this.pathLog = new Array();
        this.logPrintDiv = document.getElementById("info-log");
        this.logPrintDiv.innerHTML = "";
        this.hostname = location.hostname;
        this.port = location.port;
        this.sender = new Sender();

        //this.updateHostname();
        //this.updatePort();
        this.createPixels();
        this.getInfo();
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

    chase(r, g, b, wait_ms, interval, dir, ids=null) {
        dir *= this.direction;
        let path = "animate/chase/" + r + "," + g + "," + b + "," + wait_ms + "," + interval + "," + dir;
        this.send(path, ids);
    }

    pulse(type, r, g, b, dir, wait_ms, length, delay, ids=null) {
        dir *= this.direction;
        let path = type + "/pulse/" + r + "," + g + "," + b + "," + dir + "," + wait_ms + "," + length;
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

    animateShift(amount, post_delay, ids=null) {
        amount *= this.direction;
        let path = "animate/shift/" + amount + "," + post_delay;
        this.send(path, ids);
    }

    switch(wait_ms, instant, id, max_num, loop_start, ids=null) {
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
        this.send(path, ids);
    }

    _switch(type, colors, wait_ms, instant, loop_start, ids=null) {
        if (loop_start == "True") {
            colors += ";" + colors.split(';')[0];
        }
        let path = type + "/mix/" + colors + "," + wait_ms + "," + instant;
        this.send(path, ids);
    }

    rainbowChase(wait_ms, ids=null) {
        let path = "animate/rainbowChase/" + wait_ms;
        this.send(path, ids);
    }

    rainbowCycle(wait_ms, ids=null) {
        let path = "animate/rainbowCycle/" + wait_ms;
        this.send(path, ids);
    }

    random(segment_size, wait_ms = 0, repeated = false, ids=null) {
        let path = "";
        console.log(repeated);
        if (repeated === true) {
            console.log("true");
            path = "animate/random/";
        } else if (repeated === false) {
            console.log("false");
            path = "run/random/"
        } else {
            path = repeated + "/random/"
        }
        this.send(path + segment_size + "," + wait_ms, ids);
    }

    bounce(type, colors, wait_ms, length, direction, wait_mode, ids=null) {
        direction *= this.direction;
        let path = type + "/bounce/" + colors + "," + wait_ms + "," + length + "," + direction + "," + wait_mode;
        this.send(path, ids);
    }

    randomCycle(each, wait_ms, ids=null) {
        let path = "";
        if (each) {
            path = "animate/randomCycle/true," + wait_ms;
        } else {
            path = "animate/randomCycle/false," + wait_ms;
        }
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
        let request = new XMLHttpRequest();
        request.open('GET', url, true);
        request.onload = function () {
            console.log("Status code: ", this.status);
            if (this.status >= 200 && this.status < 400) {
                let data = JSON.parse(this.response);
                console.log("Recieved Data:", data);
                lights.recieveData(data);
            } else {
                console.log("There was an error");
            }
        };
        request.onerror = function () {
            console.log("Connection Error: ", this.status, request);
        };
        request.send();
    }

    recieveData(data) {
        this.controller_data = data;
        generic.recreateAll();
    }
}
