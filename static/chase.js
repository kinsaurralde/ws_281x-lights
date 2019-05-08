class Chase {
    constructor(id) {
        this.id = id;
        this.target = document.getElementById("chase-expanded");
    }

    create() {
        let section_flex = document.createElement("div");
        section_flex.className = "section-flex";
        section_flex.id = "chase-slot-"+this.id;
        html.appendSetting(section_flex, "Color Save Number", html.createInputNumber(0, 3, (this.id + 1) % saves.length,  "checkSaveNumber('chase-save-color-" + this.id + "')", "chase-save-color-" + this.id));
        html.appendSetting(section_flex, "Wait ms", html.createInputNumber(1, 100, 50, null, "chase-waitms-" + this.id));
        html.appendSetting(section_flex, "Interval", html.createInputNumber(1, 100, 5, null, "chase-interval-" + this.id));
        html.appendSetting(section_flex, "Direction", html.createInputSelect([{ "value": 1, "name": "Right" }, { "value": -1, "name": "Left" }], "chase-direction-" + this.id));

        html.appendSend(section_flex, "chase-send-" + this.id, "chase[" + this.id + "].send()");

        this.target.appendChild(section_flex);
    }

    remove() {
        let remove_div = document.getElementById("chase-slot-"+this.id);
        this.target.removeChild(remove_div);
    }

    send() {
        this.colorSave = document.getElementById("chase-save-color-" + this.id).value;
        this.waitms = document.getElementById("chase-waitms-" + this.id).value;
        this.interval = document.getElementById("chase-interval-" + this.id).value;
        this.direction = document.getElementById("chase-direction-" + this.id).value;
        let color = getSaveColor(this.colorSave, "chase-save-color-" + this.id);
        lights.chase(color.r, color.g, color.b, this.waitms, this.interval, this.direction);
    }
}

function addChase() {
    chase.push(new Chase(chase.length))
    chase[chase.length - 1].create(); // -1 because length increased in previous command
}

function removeChase() {
    if (chase.length > 1) {
        chase[chase.length - 1].remove();
        chase.pop();
    }
}
