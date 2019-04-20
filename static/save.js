class Save {
    constructor(id) {
        this.id = id;
        this.live = false;
        this.live_checked = false;
        this.color = {"r": 100, "g" : 100, "b" : 100};
        this.target = document.getElementById("full-color-expanded");
    }

    getColor() {
        return this.color;
    }

    create(r, g, b) {
        this.color.r = r;
        this.color.g = g;
        this.color.g = b;

        let section_flex = document.createElement("div");
        section_flex.className = "section-flex";
        section_flex.id = "save-slot-"+this.id;

        this.appendColorSaveSliders(section_flex, this.id, r, g, b);

        html.appendSend(section_flex, "full-color-send-" + this.id, "saves[" + this.id + "].send()");

        section_flex.appendChild(html.createSpacerS1());
        section_flex.appendChild(html.createSecondaryTitle("Color Values: "));
        section_flex.appendChild(html.createSpacerS1());
        section_flex.appendChild(html.createWritableTitle(this.color.r, "full-color-" + this.id + "-values-r"));
        section_flex.appendChild(html.createSpacerS1());
        section_flex.appendChild(html.createWritableTitle(this.color.g, "full-color-" + this.id + "-values-g"));
        section_flex.appendChild(html.createSpacerS1());
        section_flex.appendChild(html.createWritableTitle(this.color.b, "full-color-" + this.id + "-values-b"));

        this.target.appendChild(section_flex);

        this.updateColor();
    }

    createLive() {
        this.color.r = 100;
        this.color.g = 100;
        this.color.g = 100;

        let section_flex = document.createElement("div");
        section_flex.className = "section-flex";
        section_flex.id = "save-slot-"+this.id;

        this.appendColorSaveSliders(section_flex, this.id, this.color.r, this.color.g, this.color.b);

        section_flex.appendChild(html.createSecondaryTitle("Live"));
        section_flex.appendChild(html.createSpacerS1());
        section_flex.appendChild(html.createInputCheckBox("Live", "full-color-live-check"));
        section_flex.appendChild(html.createSpacerS5());
        section_flex.appendChild(html.createSpacerS2());

        section_flex.appendChild(html.createSpacerS1());
        section_flex.appendChild(html.createSecondaryTitle("Color Values: "));
        section_flex.appendChild(html.createSpacerS1());
        section_flex.appendChild(html.createWritableTitle(this.color.r, "full-color-" + this.id + "-values-r"));
        section_flex.appendChild(html.createSpacerS1());
        section_flex.appendChild(html.createWritableTitle(this.color.g, "full-color-" + this.id + "-values-g"));
        section_flex.appendChild(html.createSpacerS1());
        section_flex.appendChild(html.createWritableTitle(this.color.b, "full-color-" + this.id + "-values-b"));

        this.target.appendChild(section_flex);

        this.updateColor();

        this.live = true;
    }

    remove() {
        let remove_div = document.getElementById("save-slot-"+this.id);
        this.target.removeChild(remove_div);
    }

    updateColor() {
        this.color.r = document.getElementById("full-color-" + this.id + "-r").value;
        this.color.g = document.getElementById("full-color-" + this.id + "-g").value;
        this.color.b = document.getElementById("full-color-" + this.id + "-b").value;
        let sample = document.getElementById("full-color-sample-" + this.id);
        sample.style.backgroundColor = "rgb(" + this.color.r + "," + this.color.g + "," + this.color.b + ")";
        let display_r = document.getElementById("full-color-"+this.id+"-values-r");
        let display_g = document.getElementById("full-color-"+this.id+"-values-g");
        let display_b = document.getElementById("full-color-"+this.id+"-values-b");
        display_r.innerText = pad(this.color.r, 3);
        display_g.innerText = pad(this.color.g, 3);
        display_b.innerText = pad(this.color.b, 3);
        if (this.live) {
            let checked = document.getElementById("full-color-live-check").checked;
            if (checked) {
                lights.colorAll(this.color.r, this.color.g, this.color.b);
            }
        }
    }

    send() {
        this.updateColor();
        lights.colorAll(this.color.r, this.color.g, this.color.b);
    }

    
    appendColorSaveSliders(target, num, r,g,b) {
        let title = document.createElement("div");
        title.className = "section-title-secondary";
        title.innerText = "Save "+num;
        target.appendChild(title);
        target.appendChild(html.createSpacerS1());
        target.appendChild(html.createSlider(r, 0, 255, "full-color-"+num+"-r", "saves["+num+"].updateColor()"));
        target.appendChild(html.createSlider(g, 0, 255, "full-color-"+num+"-g", "saves["+num+"].updateColor()"));
        target.appendChild(html.createSlider(b, 0, 255, "full-color-"+num+"-b", "saves["+num+"].updateColor()"));
        target.appendChild(html.createSpacerS1());
        html.appendColorDisplay(target, num);
        target.appendChild(html.createSpacerS1());
    }
}

function getSaveColor(id, div_id) {
    if (id >= 0 && id < saves.length) {
        return saves[id].getColor();
    } else {
        console.log("Save color id does not exist:", id);
        checkSaveNumber(div_id);
        return saves[0].getColor();
    }
}

function checkSaveNumber(div_id) {
    let div = document.getElementById(div_id);
    let value = div.value;
    div.max = saves.length;
    if (value < 0 || value >= saves.length) {
       div.value = 0; 
    }
}

function addSaveLive() {
    saves.push(new Save(saves.length))
    saves[saves.length - 1].createLive(); // -1 because length increased in previous command
}

function addSave(r = 100, g = 100, b = 100) {
    saves.push(new Save(saves.length))
    saves[saves.length - 1].create(r, g, b); // -1 because length increased in previous command
}

function removeSave() {
    if (saves.length > 2) {
        saves[saves.length - 1].remove();
        saves.pop();
    }
}

var pad = function(n, length) {
    length++;
    var str = "" + n;
    if(str.length < length) {
        str = new Array(length - str.length).join("0") + str;
    }
    return str;
};

