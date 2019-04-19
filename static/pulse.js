class Pulse {
    constructor(id) {
        this.id = id;
        this.target = document.getElementById("pulse-expanded");
    }

    create() {
        let section_flex = document.createElement("div");
        section_flex.className = "section-flex";
        section_flex.id = "pulse-slot-"+this.id;

        html.appendSetting(section_flex, "Color Save Number", html.createInputNumber(1, 3, this.id % 3 +  1, function () { return colorSaveCheck() }, "pulse-save-color-" + this.id));
        html.appendSetting(section_flex, "Direction", html.createInputSelect([{ "value": 1, "name": "Right" }, { "value": -1, "name": "Left" }], "pulse-direction-" + this.id));
        html.appendSetting(section_flex, "Wait ms", html.createInputNumber(1, 100, 20, null, "pulse-waitms-" + this.id));
        html.appendSetting(section_flex, "Length", html.createInputNumber(1, 60, 5, null, "pulse-length-" + this.id));
        html.appendSetting(section_flex, "Delay Between", html.createInputNumber(1, 10000, 50, null, "pulse-delay-" + this.id));
        html.appendSetting(section_flex, "Repeated", html.createInputCheckBox("none", "pulse-repeated-" + this.id));

        html.appendSend(section_flex, "pulse-send-" + this.id, "pulse[" + this.id + "].send()");

        this.target.appendChild(section_flex);
    }

    remove() {
        let remove_div = document.getElementById("pulse-slot-"+this.id);
        this.target.removeChild(remove_div);
    }

    send() {
        this.colorSave = document.getElementById("pulse-save-color-" + this.id).value;
        this.direction = document.getElementById("pulse-direction-" + this.id).value;
        this.waitms = document.getElementById("pulse-waitms-" + this.id).value;
        this.length = document.getElementById("pulse-length-" + this.id).value;
        this.delay = document.getElementById("pulse-delay-" + this.id).value;
        this.mode = "thread";
        if (document.getElementById("pulse-repeated-"+this.id).checked) {
            this.mode = "animate";
        }
        lights.pulse(this.mode, saves.data[this.colorSave - 1].r, saves.data[this.colorSave - 1].g, saves.data[this.colorSave - 1].b, this.direction, this.waitms, this.length, this.delay);
    }
}

function addPulse() {
    pulse.push(new Pulse(pulse.length))
    pulse[pulse.length - 1].create(); // -1 because length increased in previous command
}

function removePulse() {
    if (pulse.length > 1) {
        pulse[pulse.length - 1].remove();
        pulse.pop();
    }
}
