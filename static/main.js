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
        this.setup();
    }

    // Setups

    createPixels() {
        for (let i = 0; i < this.numPixels; i++) {
            this.pixels[i] = new Pixel(i);
        }
    }

    createSendWindows() {
        for (let i = 0; i < this.maxSendWindows; i++) {
            this.sendWindow[i] = document.getElementById("send-data-" + i);
        }
    }

    setup() {
        let target = document.getElementById("pixel-holder");
        for (let i = 0; i < this.numPixels; i++) {
            target.innerHTML += "<div class='pixel-display' id='pixel-display-" + i + "' onmouseover='lights.setIndividual(" + i + ")'>";
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
        //this.pixels[id].setPixel(r, g, b);
    }

    updateAllPixels(r, g, b) {
        for (let i = 0; i < this.numPixels; i++) {
            this.updatePixel(i, r, g, b);
        }
    }

    setIndividual(id) {
        let update_individual = document.getElementById("individual-pixels-live-check").checked;
        if (update_individual) {
            let color = saves.data[this.currentColor - 1];
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
            let color = saves.data[this.currentColor - 1];
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
        this.updatePixel(id, r, g, b);
        let path = "run/single/" + id + "," + r + "," + g + "," + b;
        this.send(path, true);
    }

    colorAll(r, g, b) {
        let path = "run/color/" + r + "," + g + "," + b;
        this.updateAllPixels(r, g, b);
        this.send(path, true);
    }

    wipe(r, g, b, dir, wait_ms) {
        dir *= this.direction;
        let path = "run/wipe/" + r + "," + g + "," + b + "," + dir + "," + wait_ms;
        this.updateAllPixels(r, g, b);
        this.send(path, false);
    }

    chase(r, g, b, wait_ms) {
        let path = "animate/chase/" + r + "," + g + "," + b + "," + wait_ms;
        this.updateAllPixels(r, g, b);
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
            console.log(this.pathLog[i]);
        }
    }

    // Send

    send(path) {
        console.log("Send Window:", this.currentSendWindow, "Sending:", path);
        this.sendWindow[this.currentSendWindow].src = path;
        this.pathLog.push(path);
    }
}

class Pixel {
    constructor(id) {
        this.id = id;
        this.r = 0;
        this.g = 0;
        this.b = 0;
    }

    setPixel(r, g, b) {
        this.r = r;
        this.g = g;
        this.b = b;
        let displayPixel = document.getElementById("main-pixel-display-" + this.id);
        displayPixel.style.backgroundColor = "rgb(" + r + "," + g + "," + b + ")";
    }
}

// class Saves {
//     constructor() {
//         this.num = 0;
//         this.numVisible = 0;
//         this.data = new Array();
//         this.location = document.getElementById("full-color-expanded");
//     }

//     addSave(preset, r, g, b) {
//         if (this.num == this.numVisible) {
//             if (this.num < 10) {
//                 if (!preset) {
//                     r = 100;
//                     g = 100;
//                     b = 100;
//                 }
//                 let added = {
//                     "stauts": "show",
//                     "id": this.num,
//                     "r": r,
//                     "g": g,
//                     "b": b,
//                 };
//                 this.data.push(added);
//                 this.num += 1;
//                 this.numVisible += 1;
//                 this.addSaveHTML(this.num, r, g, b);
//             } else {
//                 console.log("Too Many Saves!");
//             }
//         } else {
//             this.show(this.numVisible);
//         }
//     }

//     deleteSave() {
//         this.hide(this.numVisible - 1);
//     }

//     addSaveHTML(num, r, g, b) {
//         //this.location.innerHTML +=
//             "<div class='section-flex' id='full-color-save-" + num + "'>" +
//             "<div class='section-title-secondary'>Save " + num + "</div>" +
//             "<div class='space-s-1'></div>" +
//             "<input type='range' value='" + r + "' min='0' max='255' id='full-color-" + num + "-r' oninput='fullColor(" + num + ",false)'>" +
//             "<input type='range' value='" + g + "' min='0' max='255' id='full-color-" + num + "-g' oninput='fullColor(" + num + ",false)'>" +
//             "<input type='range' value='" + b + "' min='0' max='255' id='full-color-" + num + "-b' oninput='fullColor(" + num + ",false)'>" +
//             "<div class='space-s-1'></div>" +
//             "<div class='color-sample-display' id='full-color-sample-" + num + "'></div>" +
//             "<div class='space-s-1'></div>" +
//             "<input type='button' value='Send Color' onclick='fullColor(" + num + ",true)'>" +
//             "<div class='space-s-5'></div>" +
//             "<div class='section-title-secondary'>" +
//             "    Color Values:" +
//             "    <span class='space-s-1'></span>" +
//             "    <span id='full-color-" + num + "-values-r'>" + r + "</span>" +
//             "   <span class='space-s-1'></span>" +
//             "    <span id='full-color-" + num + "-values-g'>" + g + "</span>" +
//             "    <span class='space-s-1'></span>" +
//             "    <span id='full-color-" + num + "-values-b'>" + b + "</span>" +
//             "</div>" +
//             "</div>";

//         //fullColor(num, false);
//     }

//     show(num) {
//         let target = document.getElementById("full-color-save-" + num);
//         if (target.style.display == "none") {
//             target.style.display = "flex";
//             this.numVisible += 1;
//         }
//         console.log(this.num, this.numVisible);
//     }

//     hide(num) {
//         let target = document.getElementById("full-color-save-" + num);
//         if (target.style.display == "flex") {
//             target.style.display = "none";
//             this.numVisible -= 1;
//         }
//     }

//     set(num, r, g, b) {
//         this.data[num] = {
//             "stauts": "show",
//             "id": this.num,
//             "r": r,
//             "g": g,
//             "b": b,
//         }
//     }
// }
