DEBUG = true
DEBUG_HOST = "rpi0.kinsaurralde.com"

class Info {
    constructor() {
        this.display = new Display("controllers")
        this.display.setup(init_data());
        this.url = "http://" + location.host;

        if (DEBUG) {
            this.url = DEBUG_HOST;
        }
    }
}


function init_data(r = 0, g = 0, b = 0) {
    let data = new Array(3);
    for (let i = 0; i < 3; i++) {
        let strip = {
            "strip_id": i
        }
        if (i == 0) {
            strip["data"] = new Array(60);
        } else {
            strip["data"] = new Array(30);
        }
        for (let j = 0; j < strip["data"].length; j++) {
            strip["data"][j] = { "r": r, "g": g, "b": b };
        }
        data[i] = strip;
    }
    return [data]
}