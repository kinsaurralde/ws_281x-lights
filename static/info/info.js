class Info {
    constructor() {
        this.display = new Display("controllers");
        this.display.setup(init_data());
        this.url = "http://" + location.host;
        this.s = io();
        this.rs = new Array();
        this.update = true;

        let self = this;
        this.s.on('connection_response', function() {
            console.log("Now Connected");
            self.refresh();
        });
        this.s.on('info_response', function(data) {
            self._updateDisplay(data);
        });
        this.s.on('info_renew', function() {
            console.debug("Renew Info");
            self.refresh();
        });
        this.s.on('controller_urls', function(data) {
            console.debug("Recieved controller URLS:", data);
            self._addControllers(data);
        });

        this.refresh();
    }

    _addControllers(data) {
        this.rs = new Array(0);
        for (let i = 0; i < data.length; i++) {
            let url = data[i]["url"];
            if (url == null) {
                continue;
            }
            this.rs.push(io(data[i]["url"]));
            let self = this;
            let index = this.rs.length - 1;
            this.rs[index].on('info_response', function(data) {
                self._updateDisplay(data);
            });
            this.rs[index].on('info_renew', function() {
                console.debug("Renew Info");
                self.refresh();
            });
        }
    }

    _updateDisplay(data) {
        if (this.update) {
            this.display.set(data)
        }
    }

    refresh() {
        console.debug("Refresh Info");
        if (this.update) {
            this.s.emit('info');
            for (let i = 0; i < this.rs.length; i++) {
                this.rs[i].emit('info');
            }
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