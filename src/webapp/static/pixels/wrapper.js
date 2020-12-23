const ARRAY_OFFSET_AMOUNT = 4;

class Pixels {
  constructor(num_pixels = 300, max_brightness = 127) {
    self.num_pixels = num_pixels;
    self.obj = _Pixels_new(num_pixels, max_brightness);
  }

  size() {
    return _Pixels_size(self.obj);
  }

  get() {
    const frame_pointer = _Pixels_get(self.obj);
    const frame = new Frame(self.num_pixels);
    for (let i = 0; i < self.num_pixels; i++) {
      frame.main[i] = getValue(frame_pointer + i * ARRAY_OFFSET_AMOUNT, "i32");
    }
    return frame;
  }

  getBrightness() {
    return _Pixels_getBrightness(self.obj);
  }

  setBrightness(value) {
    _Pixels_setBrightness(self.obj, value);
  }

  animation(args) {
    _Pixels_animation(self.obj, args);
  }

  increment() {
    _Pixels_increment(self.obj);
  }
}

class List {
  constructor(length) {
    this.length = length;
    this.obj = _List_new(length);
  }

  set(index, value) {
    _List_set(this.obj, index, value);
  }
}

class Frame {
  constructor(size) {
    this.main = new Array(size);
    this.second = new Array(size);
  }
}

class AnimationArgs {
  constructor() {
    this.animation = 0;
    this.color = 0;
    this.color_bg = 0;
    this.colors = new List(0);
    this.wait_ms = 0;
    this.arg1 = 0;
    this.arg2 = 0;
    this.arg3 = 0;
    this.arg4 = 0;
    this.arg5 = 0;
    this.arg6 = 0;
    this.arg7 = 0;
    this.arg8 = 0;
  }

  get() {
    return _createAnimationArgs(
      this.animation,
      this.color,
      this.color_bg,
      this.colors,
      this.wait_ms,
      this.arg1,
      this.arg2,
      this.arg3,
      this.arg4,
      this.arg5,
      this.arg6,
      this.arg7,
      this.arg8
    );
  }
}
