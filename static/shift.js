class Shift {
    constructor(id) {
        this.id = id;
        this.target = document.getElementById("operations-expanded");
        if (this.id == 0) {
            this.amount = 1;
        } else {
            this.amount = -1;
        }
    }

    create() {
        let section_flex = document.createElement("div");
        section_flex.className = "section-flex";
        section_flex.id = "operations-shift-slot-" + this.id;

        html.appendSetting(section_flex, "Amount", html.createInputNumber(1, 3, this.id % 3 + 1, null, "operations-shift-amount-" + this.id));
        html.appendSetting(section_flex, "Delay ms", html.createInputNumber(1, 100, 20, null, "operations-shift-delayms-" + this.id));

        html.appendSend(section_flex, "operations-shift-send-" + this.id, "shift[" + this.id + "].send()");

        this.target.appendChild(section_flex);
    }

    remove() {
        let remove_div = document.getElementById("operations-shift-slot-" + this.id);
        this.target.removeChild(remove_div);
    }

    send() {
        this.amount = document.getElementById("operations-shift-amount-" + this.id).value;
        this.delay = document.getElementById("operations-shift-delayms-" + this.id).value;
        lights.animateShift(this.amount, this.delay);
    }
}

function addShift() {
    shift.push(new Shift(shift.length))
    shift[shift.length - 1].create(); // -1 because length increased in previous command
}

function removeShift() {
    if (shift.length > 1) {
        shift[shift.length - 1].remove();
        shift.pop();
    }
}
