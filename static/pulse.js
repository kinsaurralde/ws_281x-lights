class Pulse {
    constructor(id) {
        this.id = id;
        this.target = document.getElementById("pulse-expanded");
    }

    create() {
        let section_flex = document.createElement("div");
        section_flex.className = "section-flex";
        section_flex.id = "pulse-slot-"+this.id;
        html.appendSetting(section_flex, "Color Save Number", html.createInputNumber(0, 3, (this.id + 1) % saves.length,  "checkSaveNumber('pulse-save-color-" + this.id + "')", "pulse-save-color-" + this.id));
        html.appendSetting(section_flex, "Direction", html.createInputSelect([{ "value": 1, "name": "Right" }, { "value": -1, "name": "Left" }], "pulse-direction-" + this.id));
        html.appendSetting(section_flex, "Wait ms", html.createInputNumber(1, 100, 10, null, "pulse-waitms-" + this.id));
        html.appendSetting(section_flex, "Length", html.createInputNumber(1, 60, 5, null, "pulse-length-" + this.id));
        html.appendSetting(section_flex, "Delay Between", html.createInputNumber(1, 10000, 100, null, "pulse-delay-" + this.id));
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
        let color = getSaveColor(this.colorSave, "pulse-save-color-" + this.id);
        lights.pulse(this.mode, color.r, color.g, color.b, this.direction, this.waitms, this.length, this.delay);
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
