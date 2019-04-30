class Preset {
    constructor() {
        this.web_create_custom();
    }

    run(num) {
        console.log(num)
        switch (num) {
            case 0:
                this.red_cyan_green_magenta_blue_yellow()
                break;
            case 1:
                this.red_green_blue();
                break;
            default:
                lights.off();
        }
    }

    red_cyan_green_magenta_blue_yellow() {
        let lights_multiple = [{   
                start: 0, end: 9,
                r: 255, g: 0, b: 0,
            }, {   
                start: 10, end: 19,
                r: 0, g: 255, b: 255,
            }, {   
                start: 20, end: 29,
                r: 0, g: 255, b: 0,
            }, {   
                start: 30, end: 39,
                r: 255, g: 0, b: 255,
            }, {   
                start: 40, end: 49,
                r: 0, g: 0, b: 255,
            }, {   
                start: 50, end: 59,
                r: 255, g: 255, b: 0,
            }
        ]
        lights.sendMultiple(lights_multiple);
    }

    red_green_blue() {
        let lights_multiple = [{   
                start: 0, end: 29,
                r: 255, g: 0, b: 0,
            }, {   
                start: 20, end: 39,
                r: 0, g: 255, b: 0,
            }, {   
                start: 40, end: 59,
                r: 0, g: 0, b: 255,
            }
        ]
        lights.sendMultiple(lights_multiple);
    }

    getWebTheme(name) {
        document.getElementById("settings-web-theme-expanded").style.display = "none";
        if (name == "light" || name == "dark") {
            return this.web_full_theme(name);
        }
        if (name == "high_contrast") {
            return this.web_high_contrast();
        }
        if (name == "high_contrast_colored") {
            return this.web_high_contrast_colored();
        }
        if (name == "dark_rgb") {
            return this.web_dark_rgb();
        }
        if (name == "custom") {
            document.getElementById("settings-web-theme-expanded").style.display = "block";
            return this.web_full_theme("light");
        }
    }

    web_full_theme(name) {
        let theme_data = {
            "body-background" : name+"-body-background",
            "text-color" : name+"-text-color",
            "input-border" : name+"-input-border",
            "input-background" : name+"-input-background",
            "border-color" : name+"-border-color",
        };
        return theme_data;
    }

    web_high_contrast() {
        let theme_data = {
            "body-background" : "dark-body-background",
            "text-color" : "light-body-background",
            "input-border" : "light-body-background",
            "input-background" : "dark-body-background",
            "border-color" : "light-body-background",
        };
        return theme_data;
    }

    web_high_contrast_colored() {
        let theme_data = {
            "body-background" : "dark-body-background",
            "text-color" : "color-yellow",
            "input-border" : "color-magenta",
            "input-background" : "dark-body-background",
            "border-color" : "color-cyan",
        };
        return theme_data;
    }

    web_dark_rgb() {
        let theme_data = {
            "body-background" : "dark-body-background",
            "text-color" : "color-red",
            "input-border" : "color-blue",
            "input-background" : "dark-body-background",
            "border-color" : "color-green",
        };
        return theme_data;
    }

    web_create_custom() {
        let target = document.getElementById("settings-web-custom-container");
        html.appendSetting(target, "Background Color", html.createInputNumber(0, 6, 3,  "checkSaveNumber('settings-web-custom-color-background')", "settings-web-custom-color-background"));
        html.appendSetting(target, "Text Color", html.createInputNumber(0, 6, 5,  "checkSaveNumber('settings-web-custom-color-text')", "settings-web-custom-color-text"));
        html.appendSetting(target, "Input Borders", html.createInputNumber(0, 6, 1,  "checkSaveNumber('settings-web-custom-color-input-border')", "settings-web-custom-color-input-border"));
        html.appendSetting(target, "Input Backgrounds", html.createInputNumber(0, 6, 4,  "checkSaveNumber('settings-web-custom-color-input-background')", "settings-web-custom-color-input-background"));
        html.appendSetting(target, "Section Border Colors", html.createInputNumber(0, 6, 6,  "checkSaveNumber('settings-web-custom-color-border')", "settings-web-custom-color-border"));
        target.appendChild(html.createButton("Apply", "settings-web-custom-apply", "preset.webApplyCustom()"));
    }

    webApplyCustom() {
        let css_vars = document.getElementsByTagName("html")[0].style;
        let div_ids = [
            "settings-web-custom-color-background",
            "settings-web-custom-color-text",
            "settings-web-custom-color-input-border",
            "settings-web-custom-color-input-background",
            "settings-web-custom-color-border",
        ]
        let colors = [];
        for (let i = 0; i < div_ids.length; i++) {
            let current = document.getElementById(div_ids[i]).value;
            colors.push(getSaveColor(current));
        }
        css_vars.setProperty("--body-background", "rgb("+colors[0].r+","+colors[0].g+","+colors[0].b+")");
        css_vars.setProperty("--text-color", "rgb("+colors[1].r+","+colors[1].g+","+colors[1].b+")");
        css_vars.setProperty("--input-border", "rgb("+colors[2].r+","+colors[2].g+","+colors[2].b+")");
        css_vars.setProperty("--input-background", "rgb("+colors[3].r+","+colors[3].g+","+colors[3].b+")");
        css_vars.setProperty("--border-color", "rgb("+colors[4].r+","+colors[4].g+","+colors[4].b+")");
    }
}

function colorTheme() {
    let theme_name = document.getElementById("settings-web-theme").value;
    let css_vars = document.getElementsByTagName("html")[0].style;
    let new_theme = preset.getWebTheme(theme_name);
    css_vars.setProperty("--body-background", "var(--"+new_theme["body-background"]);
    css_vars.setProperty("--text-color", "var(--"+new_theme["text-color"]);
    css_vars.setProperty("--input-border", "var(--"+new_theme["input-border"]);
    css_vars.setProperty("--input-background", "var(--"+new_theme["input-background"]);
    css_vars.setProperty("--border-color", "var(--"+new_theme["border-color"]);
}
