class Simulator {
  constructor() {
    this.pixel_strips = {};
    this.intervalId = 0;
    this.frame_rate = 50;
  }

  init(controllers) {
    for (let i = 0; i < controllers.length; i++) {
      this.pixel_strips[controllers[i]] = new SimulatedPixels(controllers[i]);
    }
    this.start();
  }

  setArgs(values) {
    const args = new AnimationArgs();
    args.animation = parseInt(values.animation);
    args.color = parseInt(values.color);
    args.color_bg = parseInt(values.color_bg);
    args.wait_ms = parseInt(values.wait_ms);
    args.arg1 = parseInt(values.arg1);
    args.arg2 = parseInt(values.arg2);
    args.arg3 = parseInt(values.arg3);
    args.arg4 = parseInt(values.arg4);
    args.arg5 = parseInt(values.arg5);
    args.arg6 = values.arg6;
    args.arg7 = values.arg7;
    args.arg8 = values.arg8;
    const colors_list = new List(values.colors.length);
    for (let i = 0; i < values.colors.length; i++) {
      colors_list.set(i, values.colors[i]);
    }
    args.colors = colors_list;
    return args;
  }

  handleData(data) {
    for (let i = 0; i < data.length; i++) {
      const command = data[i];
      const id = command['id'];
      const inc_steps = parseInt(command.inc_steps);
      const args = this.setArgs(command);
      if (id in this.pixel_strips) {
        this.pixel_strips[id].setIncrementSteps(inc_steps);
        this.pixel_strips[id].animation(args);
      }
    }
  }

  getAll() {
    const data = {};
    for (const pixel_strip in this.pixel_strips) {
      if (this.pixel_strips.hasOwnProperty(pixel_strip)) {
        data[pixel_strip] = this.pixel_strips[pixel_strip].get();
      }
    }
    return data;
  }

  refresh() {
    const data = {};
    for (const pixel_strip in this.pixel_strips) {
      if (this.pixel_strips.hasOwnProperty(pixel_strip)) {
        data[pixel_strip] = this.pixel_strips[pixel_strip].get().main;
      }
    }
    pixel_display.set(data);
  }

  start() {
    const self = this;
    this.intervalId = setInterval(function() {
      self.refresh();
    }, 1000 / this.frame_rate);
  }

  stop() {
    clearInterval(this.intervalId);
  }

  setFrameRate(value) {
    if (value > 0 && value <= 100) {
      this.frame_rate = value;
      this.stop();
      this.start();
    }
  }
}

class SimulatedPixels {
  constructor(name) {
    this.name = name;
    this.pixels = new Pixels();
    this.intervalId = 0;
    this.increment_steps = 1;
    this.wait_ms = 40;
    this.start();
  }

  start() {
    const self = this;
    this.intervalId = setInterval(function() {
      self.increment();
    }, this.wait_ms);
  }

  stop() {
    clearInterval(this.intervalId);
    this.intervalId = 0;
  }

  setWaitMs(value) {
    this.wait_ms = value;
    this.stop();
    this.start();
  }

  setIncrementSteps(value) {
    if (value >= 0) {
      this.increment_steps = value;
    }
  }

  increment() {
    for (let i = 0; i < this.increment_steps; i++) {
      this.pixels.increment();
    }
    return this.pixels.get().main;
  }

  get() {
    return this.pixels.get();
  }

  animation(args) {
    const wait_ms = args.wait_ms;
    if (wait_ms >= 10 && this.wait_ms != wait_ms) {
      this.setWaitMs(wait_ms);
    }
    this.pixels.animation(args.get());
  }
}