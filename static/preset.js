class Preset {
    run(num) {
        console.log(num)
        switch (num) {
            case 0:
                console.log("sd")
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
}