class Simulator {
    constructor() {
        this.pixels = new Pixels();
        this.intervalId = 0;
        this.start();
    }

    setArgs(values) {
        const args = new AnimationArgs();
        args.animation =  parseInt(values.animation);
        args.color =  parseInt(values.color);
        args.color_bg =  parseInt(values.color_bg);
        args.wait_ms =  parseInt(values.wait_ms);
        args.arg1 =  parseInt(values.arg1);
        args.arg2 =  parseInt(values.arg2);
        args.arg3 =  parseInt(values.arg3);
        args.arg4 =  parseInt(values.arg4);
        args.arg5 =  parseInt(values.arg5);
        args.arg6 =  values.arg6;
        args.arg7 =  values.arg7;
        args.arg8 =  values.arg8;
        const colors_list = new List(values.colors.length);
        args.colors = colors_list;
        return args;
    }

    handleData(data) {
        const command = data[0];
        console.log("Handle", command);
        const args = this.setArgs(command);
        console.log("ARGS", args);
        this.pixels.animation(args.get());
    }

    getAll() {
        return this.pixels.get().main;
    }

    increment() {
        this.pixels.increment();
        pixel_display.set({
            'tester_a_0': this.pixels.get().main
        });
    }

    start() {
        const self = this;
        this.intervalId = setInterval(function() {
            self.increment();
        }, 40);
    }

    stop() {
        clearInterval(this.intervalId);
    }
}