class HTMLWriter {
    createSpacerS1() {
        let spacer = document.createElement("div");
        spacer.className = "space-s-1";
        return spacer;
    }

    createSpacerS2() {
        let spacer = document.createElement("div");
        spacer.className = "space-s-2";
        return spacer;
    }

    createSpacerS5() {
        let spacer = document.createElement("div");
        spacer.className = "space-s-5";
        return spacer;
    }

    createDivider() {
        let div = document.createElement("div");
        div.className = "divider";
        return div
    }

    createVDivider() {
        let div = document.createElement("div");
        div.className = "v-divider";
        return div
    }

    appendSetting(parent, title, input, multiple = false) {
        let final_div = document.createElement("div");
        final_div.className = "section-setting";
        let title_div = document.createElement("div");
        title_div.className = "section-title-secondary";
        title_div.innerText = title;
        final_div.appendChild(title_div);
        if (multiple) {
            for (let i = 0; i < input.length; i++) {
                final_div.appendChild(input[i]);
            }
        } else {
            final_div.appendChild(input);
        }
        parent.appendChild(final_div);
        parent.appendChild(html.createSpacerS1());
    }

    appendSend(parent, id, onclick) {
        let send_div = document.createElement("div");
        send_div.className = "section-send";
        let send = document.createElement("input");
        send.type = "button";
        send.value = "Send";
        send.id = id;
        send.className = "section-send-button";
        send.onclick = new Function(onclick);
        send_div.appendChild(send);
        parent.appendChild(send_div);
    }

    createInputCheckBox(value, id, precheck = false, oninput=null) {
        let check_box = document.createElement("input");
        check_box.type = "checkbox";
        check_box.value = value;
        check_box.id = id;
        check_box.checked = precheck;
        check_box.onclick = new Function(oninput);
        return check_box;
    }

    createButton(value, id, onclick) {
        let input_div = document.createElement("input");
        input_div.type = "button";
        input_div.value = value;
        input_div.id = id;
        if (typeof onclick == "string") {
            input_div.onclick = new Function(onclick);
        } else {
            input_div.onclick = onclick;
        }
        return input_div;
    }

    createSlider(value, min, max, id, oninput) {
        let slider = document.createElement("input");
        slider.type = "range";
        slider.min = min;
        slider.max = max;
        slider.value = value;
        slider.id = id;
        slider.oninput = new Function(oninput);
        return slider;
    }

    create125Text(text, id=null) {
        let div = document.createElement('div');
        div.className = "text-1-25";
        div.innerText = text;
        div.id = id;
        return div;
    }

    createText5(value, id, oninput) {
        let text = document.createElement("input");
        text.type = "text";
        text.value = value;
        text.id = id;
        text.className = "width-5";
        text.oninput = new Function(oninput);
        return text;
    }

    createNumber(value, id, oninput) {
        let text = document.createElement("input");
        text.type = "number";
        text.value = value;
        text.id = id;
        text.oninput = new Function(oninput);
        return text;
    }

    createSelect(value, id, options, onchange) {
        let select = document.createElement("select");
        select.id = id;
        for (let i = 0; i < options.length; i++) {
            let text = options[i];
            let value = options[i];
            if (typeof(options[i]) == "object" && options[i] != null) {
                text = options[i]["name"];
                value = options[i]["value"];
            }
            let opt = document.createElement("option");
            opt.appendChild(document.createTextNode(text));
            opt.value = value;
            select.appendChild(opt);
        }
        select.value = value;
        select.onchange = new Function(onchange);
        return select;
    }

    createNONE(id) {
        let div = document.createElement("div");
        div.id = id;
        div.innerHTML = "---";
        return div;
    }

    createWritableTitle(title, id) {
        let title_div = this.createSecondaryTitle(title);
        title_div.id = id;
        return title_div;
    }

    appendColorDisplay(target, num) {
        let display = document.createElement("div");
        display.className = "color-sample-display";
        display.id = "full-color-sample-" + num;
        target.appendChild(display);
    }

    createSecondaryTitle(title) {
        let title_div = document.createElement("div");
        title_div.className = "section-title-secondary";
        title_div.innerText = title;
        return title_div;
    }
};

function verify_number(min, max, d_value, div_id) {
    let div = document.getElementById(div_id);
    let value = div.value;
    if (value < min || value > max || value == "") {
        div.value = d_value;
    }
}
