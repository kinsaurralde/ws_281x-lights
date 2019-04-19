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
        this.target.innerHTML += 
        "<div class='section-flex'>" +
            "<div class='section-setting'>" +
                "<div class='section-title-secondary'>Amount</div>" +
                "<input type='number' min='-100' max='100' value='"+this.amount+"'id='operations-shift-amount-"+this.id+"'>" +
            "</div>" +
            "<div class='section-setting'>" +
                "<div class='section-title-secondary'>Delay ms</div>" +
                "<input type='number' min='1' max='100' value='25' id='operations-shift-delayms-"+this.id+"'>" +
            "</div>" +
            "<div class='space-s-1'></div>" +
            "<input type='button' value='Shift Left' onclick='shift["+this.id+"].send("+this.id+")'>" +
        "</div>";
    }

    send() {
        this.amount = document.getElementById("operations-shift-amount-"+this.id).value;
        this.delay = document.getElementById("operations-shift-delayms-"+this.id).value;
        lights.animateShift(this.amount, this.delay);
    }
}