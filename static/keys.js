class Keys {
    constructor() {
        this.table = document.getElementById("keys-table");
        this.href = location.href;
        this.href = this.href.split('/');
        this.href.pop();
        this.href = this.href.join('/');
        this.data = [];
        document.getElementById("keys-host").innerText = this.href;
    }

    clearTable() {
        let table_size = this.table.rows.length;
        for (let i = 1; i < table_size; i++) {
            this.table.deleteRow(1);
        }
    }

    appendRow(row_num, key, strips) {
        console.log(key, strips);
        let row = this.table.insertRow();
        let cells = [];
        for (let i = 0; i < 9; i++) {
            cells.push(row.insertCell(-1));
        }
        cells[0].innerText = key;
        cells[0].id = "key-"+row_num;
        cells[1].innerText = strips;
        cells[2].appendChild(this.appendInputNumber("change-num-"+row_num));
        cells[3].appendChild(this.appendInputButton("change-send-"+row_num, "keys.changeKey('" + row_num + "')", "Send Change Key"));
        cells[4].appendChild(this.appendInputNumber("add-strip-num-"+row_num));
        cells[5].appendChild(this.appendInputButton("add-strip-send-"+row_num, "keys.addStrip('" + row_num + "')", "Send Add Strip"));
        cells[6].appendChild(this.appendInputNumber("remove-strip-num-"+row_num));
        cells[7].appendChild(this.appendInputButton("remove-strip-send-"+row_num, "keys.removeStrip('" + row_num + "')", "Send Remove Strip"));
        cells[8].appendChild(this.appendInputButton("remove-key-send-"+row_num, "keys.removeKey('" + row_num + "')", "Remove Key"));
    }

    appendInputNumber(id) {
        let input = document.createElement("input");
        input.type = "number";
        input.min = 0;
        input.value = "";
        input.id = id;
        return input;
    }

    appendInputButton(id, onclick, value) {
        let input = document.createElement("input");
        input.type = "button";
        input.value = value;
        input.id = id;
        input.onclick = new Function(onclick);
        return input;
    }

    buildTable() {
        this.clearTable();
        let _keys = Object.keys(this.data);
        let i = 0;
        for (let key of _keys) {
            this.appendRow(i, key, this.data[key]);
            i++;
        }
    }

    refresh() {
        this.send("/get");
    }

    checkInt(num) {
        if (isNaN(parseInt(num))) {
            return false;
        } else {
            return true;
        }
    }

    changeKey(row_num) {
        let old_key = document.getElementById("key-"+row_num).innerText;
        let new_key = document.getElementById("change-num-"+row_num).value;
        if (!this.checkInt(new_key)) {
            return;
        }
        let path = "/change/"+old_key+","+new_key;
        this.send(path);
    }

    addStrip(row_num) {
        let key = document.getElementById("key-"+row_num).innerText;
        let strip = document.getElementById("add-strip-num-"+row_num).value;
        if (!this.checkInt(strip)) {
            return;
        }
        let path = "/addstrip/"+key+","+strip;
        this.send(path);
    }

    removeStrip(row_num) {
        let key = document.getElementById("key-"+row_num).innerText;
        let strip = document.getElementById("remove-strip-num-"+row_num).value;
        if (!this.checkInt(strip)) {
            return;
        }
        let path = "/removestrip/"+key+","+strip;
        this.send(path);
    }

    addKey() {
        let key = document.getElementById("add-key-num").value;
        if (!this.checkInt(key)) {
            return;
        }
        let path = "/addkey/"+key;
        this.send(path);
    }

    removeKey(row_num) {
        let key = document.getElementById("key-"+row_num).innerText;
        if (!this.checkInt(key)) {
            return;
        }
        let path = "/removekey/"+key;
        this.send(path);
    }

    send(path) {
        let url = this.href + path;
        let request = new XMLHttpRequest();
        request.open('GET', url, true);
        request.onload = function() {
            console.log("Status code: ", this.status);
            if (this.status >= 200 && this.status < 400) {
                let data = JSON.parse(this.response);
                console.log("Recieved Data:",data);
                keys.data = data;
                keys.buildTable();
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

