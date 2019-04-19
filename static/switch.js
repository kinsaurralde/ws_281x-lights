class LSwitch {
    constructor() {
        this.target = document.getElementById("switch-expanded");
        this.colorslots;
        this.count = 0;
    }

    create() {
        let section_flex = document.createElement("div");
        section_flex.className = "section-flex";

        html.appendSetting(section_flex, "Transition ms", html.createInputNumber(1, 100, 20, null, "switch-waitms"));
        html.appendSetting(section_flex, "Instant", html.createInputCheckBox("none", "switch-instant"));
        html.appendSetting(section_flex, "Loop to start", html.createInputCheckBox("none", "switch-loop-start", true));

        html.appendSetting(section_flex, "Add Color", html.createButton("+", "switch-add-color", "lswitch.addColor()"));
        html.appendSetting(section_flex, "Remove Color", html.createButton("-", "switch-remove-color", "lswitch.removeColor()"));

        html.appendSend(section_flex, "switch-send", "lswitch.send()");

        this.target.appendChild(section_flex);

        let section = document.createElement("div");
        section.className = "section-flex";
        section.id = "switch-colorslots";

        this.target.appendChild(section);

        this.colorslots = document.getElementById("switch-colorslots");

        this.addColor();
        this.addColor();
        this.addColor();
    }

    addColor() {
        html.appendSettingID(this.colorslots, "Color Save Number", html.createInputNumber(1, 3, this.count % 3 + 1, function () { return colorSaveCheck() }, "switch-save-color-" + this.count), "switch-slot-"+this.count);
        this.count++;
    }

    removeColor() {
        if (this.count > 1) {
            this.count--;
            let remove_div = document.getElementById("switch-slot-"+this.count);
            this.colorslots.removeChild(remove_div);
            this.colorslots.removeChild(this.colorslots.getElementsByClassName("space-s-1")[this.count]);
        }
    }

    send() {
        let waitms = document.getElementById("switch-waitms").value;
        let instant = document.getElementById("switch-instant").checked;
        let loop_start = document.getElementById("switch-loop-start").checked;
        lights.switch(waitms, instant, "switch-save-color-", this.count, loop_start);
    }
}
