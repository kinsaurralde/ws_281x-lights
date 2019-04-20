class Wipe {
    constructor(id) {
        this.id = id;
        this.target = document.getElementById("wipe-expanded");
        this.colorSave = this.id + 1;
        this.direction = 1;
        this.waitms = Math.floor(Math.random() * 15) + 5;
    }

    create() {
        let section_flex = document.createElement("div");
        section_flex.className = "section-flex";
        section_flex.id = "wipe-slot-"+this.id;

        html.appendSetting(section_flex, "Color Save Number", html.createInputNumber(0, 3, (this.id + 1) % saves.length, "checkSaveNumber('wipe-save-color-" + this.id + "')", "wipe-save-color-" + this.id));
        html.appendSetting(section_flex, "Direction", html.createInputSelect([{ "value": 1, "name": "Right" }, { "value": -1, "name": "Left" }], "wipe-direction-" + this.id));
        html.appendSetting(section_flex, "Wait ms", html.createInputNumber(1, 100, 20, null, "wipe-waitms-" + this.id));

        html.appendSend(section_flex, "wipe-send-" + this.id, "wipes[" + this.id + "].send()");

        this.target.appendChild(section_flex);
    }

    remove() {
        let remove_div = document.getElementById("wipe-slot-"+this.id);
        this.target.removeChild(remove_div);
    }

    send() {
        this.colorSave = document.getElementById("wipe-save-color-"+this.id).value;
        this.direction = document.getElementById("wipe-direction-"+this.id).value;
        this.waitms = document.getElementById("wipe-waitms-"+this.id).value;
        let color = getSaveColor(this.colorSave, "wipe-save-color-" + this.id);
        lights.wipe(color.r, color.g, color.b, this.direction, this.waitms);
    }
}

function addWipe() {
    wipes.push(new Wipe(wipes.length))
    wipes[wipes.length - 1].create(); // -1 because length increased in previous command
}

function removeWipe() {
    if (wipes.length > 1) {
        wipes[wipes.length - 1].remove();
        wipes.pop();
    }
}