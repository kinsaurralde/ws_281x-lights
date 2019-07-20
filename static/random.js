class Random {
    constructor(id) {
        this.id = id;
        this.target = document.getElementById("random-expanded");
    }

    create() {
        let section_flex = document.createElement("div");
        section_flex.className = "section-flex";
        section_flex.id = "random-slot-" + this.id;
        html.appendSetting(section_flex, "Segment Size", html.createInputNumber(1, 60, 60, "verify_number(0,60,60,'random-length-" + this.id + "')", "random-length-" + this.id));
        html.appendSetting(section_flex, "Wait ms", html.createInputNumber(1, 100, 100 + 100 * this.id, null, "random-waitms-" + this.id));
        html.appendSetting(section_flex, "Repeated", html.createInputCheckBox("none", "random-repeated-" + this.id));

        html.appendSend(section_flex, "random-send-" + this.id, "random[" + this.id + "].send()");

        this.target.appendChild(section_flex);
    }

    remove() {
        let remove_div = document.getElementById("random-slot-" + this.id);
        this.target.removeChild(remove_div);
    }

    send() {
        let waitms = document.getElementById("random-waitms-" + this.id).value;
        let length = document.getElementById("random-length-" + this.id).value;
        let repeated = document.getElementById("random-repeated-" + this.id).checked;
        lights.random(length, waitms, repeated);
    }

}

function addRandom() {
    random.push(new Random(random.length))
    random[random.length - 1].create(); // -1 because length increased in previous command
}

function removeRandom() {
    if (random.length > 1) {
        random[random.length - 1].remove();
        random.pop();
    }
}
