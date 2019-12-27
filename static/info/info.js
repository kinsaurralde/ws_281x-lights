class Info {
    constructor() {
        this.display = new Display("controllers")
        this.display.setup(init_data());
        this.url = "http://" + location.host;
        this.s = io();
        this.update = true;

        let self = this;
        this.s.on('connection_response', function() {
            console.log("Now Connected");
        });
        this.s.on('info_response', function(data) {
            self.updateDisplay(data);
        });
        this.s.on('info_renew', function() {
            self.refresh();
        });

        this.refresh();
    }

    updateDisplay(data) {
        if (this.update) {
            this.display.set(data)
        }
    }

    refresh() {
        if (this.update) {
            console.debug("Refreshing info");
            this.s.emit('info');
        }
    }

    setUpdate(val) {
        this.update = val;
    }
}


function init_data(r = 0, g = 0, b = 0) {
    let data = {
        "controller_id": 0,
        "strip_info": [
            {"id": 0, "start": 0, "end": 59},
            {"id": 1, "start": 0, "end": 29},
            {"id": 2, "start": 30, "end": 59},
        ],
        "pixels": new Array(60)
    };
    for (let i = 0; i < 60; i++) {
        data["pixels"][i] = {"r": 0, "g": 0, "b": 0};
    }
    return data
}