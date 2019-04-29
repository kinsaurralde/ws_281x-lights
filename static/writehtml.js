class HTMLWriter {
    constructor() {

    }

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

    appendSettingID(parent, title, input, id) {
        let final_div = document.createElement("div");
        final_div.className = "section-setting";
        let title_div = document.createElement("div");
        title_div.className = "section-title-secondary";
        title_div.innerText = title;
        final_div.appendChild(title_div);
        final_div.appendChild(input);
        final_div.id = id;
        let spacer = document.createElement("div");
        spacer.className = "space-s-1";
        parent.appendChild(final_div);
        parent.appendChild(spacer);
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

    createInputNumber(min, max, value, oninput, id) {
        let input = document.createElement("input");
        input.type = "number";
        input.min = min;
        input.max = max;
        input.value = value; 
        input.oninput = new Function(oninput);
        input.id = id;
        return input;
    }

    createInputSelect(values, id) {
        let select = document.createElement("select");
        select.id = id;
        select.value = values[0]["value"];
        for (let i = 0; i < values.length; i++) {
            let option = document.createElement("option");
            option.value = values[i]["value"];
            option.innerText = values[i]["name"];
            select.appendChild(option);
        }
        return select;
    }

    createInputCheckBox(value, id, precheck = false) {
        let check_box = document.createElement("input");
        check_box.type = "checkbox";
        check_box.value = value;
        check_box.id = id;
        check_box.checked = precheck;
        return check_box;
    }

    createButton(value, id, onclick) {
        let input_div = document.createElement("input");
        input_div.type = "button";
        input_div.value = value;
        input_div.id = id;
        input_div.onclick = new Function(onclick);
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

    createWritableTitle(title, id) {
        let title_div = this.createSecondaryTitle(title);
        title_div.id = id;
        return title_div;
    }

    appendColorDisplay(target, num) {
        let display = document.createElement("div");
        display.className = "color-sample-display";
        display.id = "full-color-sample-"+num;
        target.appendChild(display);
    }

    createSecondaryTitle(title) {
        let title_div = document.createElement("div");
        title_div.className = "section-title-secondary";
        title_div.innerText = title;
        return title_div;
    }
}