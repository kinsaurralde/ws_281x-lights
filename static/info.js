class Info {
    constructor() {
        this.location = document.getElementById("info-section");
        this.table = document.getElementById("info-table");
        this.data = [];
        this.refresh();
    }

    refresh() {
        this.send("/info");
    }

    recieveData(data) {
        this.data = data;
        this.clearTable();
        for (let i = 0; i < this.data.length; i++) {
            this.appendRow(data[i]);
        }
    }

    appendRow(data) {
        let row = this.table.insertRow();
        for (let j = 0; j < 5; j++) {
            row.insertCell();   
        }
        this.table.rows[this.table.rows.length - 1].cells[0].innerHTML = data["controller_id"];
        this.table.rows[this.table.rows.length - 1].cells[1].innerHTML = data["power"]["now_milliamps"];
        this.table.rows[this.table.rows.length - 1].cells[2].innerHTML = data["settings"]["brightness"];
        this.table.rows[this.table.rows.length - 1].cells[3].innerHTML = data["settings"]["num_pixels"];
        this.table.rows[this.table.rows.length - 1].cells[4].innerHTML = data["strip_info"].length;
    }

    clearTable() {
        let table_size = this.table.rows.length;
        for (let i = 1; i < table_size; i++) {
            this.table.deleteRow(1);
        }
    }

    send(path) {
        //let url = this.href + path;
        let url = "http://pilaptop.kinsaurralde.com:200" + path;
        let request = new XMLHttpRequest();
        request.open('GET', url, true);
        request.onload = function() {
            console.log("Status code: ", this.status);
            if (this.status >= 200 && this.status < 400) {
                let data = JSON.parse(this.response);
                console.log("Recieved Data:",data);
                info.recieveData(data);
            } else {
                console.log("There was an error");
            }
        };
        request.onerror = function() {
            console.log("Connection Error: ", this.status, request);
        };
        request.send();
    }
}

