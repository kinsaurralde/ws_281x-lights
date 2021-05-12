const ARRAY_OFFSET_AMOUNT = 4;

class Pixels {
  constructor(num_pixels = 300, max_brightness = 127) {
    this.num_pixels = num_pixels;
    this.obj = _Pixels_new(num_pixels, max_brightness);
  }

  size() {
    return _Pixels_size(this.obj);
  }

  get() {
    const frame_pointer = _Pixels_get(this.obj);
    const frame = new Frame(this.num_pixels);
    for (let i = 0; i < this.num_pixels; i++) {
      frame.main[i] = getValue(frame_pointer + i * ARRAY_OFFSET_AMOUNT, "i32");
    }
    return frame;
  }

  getBrightness() {
    return _Pixels_getBrightness(this.obj);
  }

  setBrightness(value) {
    _Pixels_setBrightness(this.obj, value);
  }

  animation(args) {
    _Pixels_animation(this.obj, args);
  }

  increment() {
    _Pixels_increment(this.obj);
  }

  getCurrentState() {
    const state_pointer = _Pixels_getCurrentState(this.obj);
    const incArgs = new IncrementArgs();
    incArgs.incId = getValue(state_pointer + 0 * ARRAY_OFFSET_AMOUNT, "i32");
    incArgs.arg1 = getValue(state_pointer + 1 * ARRAY_OFFSET_AMOUNT, "i32");
    incArgs.arg2 = getValue(state_pointer + 2 * ARRAY_OFFSET_AMOUNT, "i32");
    incArgs.arg3 = getValue(state_pointer + 3 * ARRAY_OFFSET_AMOUNT, "i32");
    incArgs.arg4 = getValue(state_pointer + 4 * ARRAY_OFFSET_AMOUNT, "i32");
    incArgs.arg5 = getValue(state_pointer + 5 * ARRAY_OFFSET_AMOUNT, "i32");
    incArgs.arg6 = getValue(state_pointer + 6 * ARRAY_OFFSET_AMOUNT, "i32");
    incArgs.arg7 = getValue(state_pointer + 7 * ARRAY_OFFSET_AMOUNT, "i32");
    incArgs.arg8 = getValue(state_pointer + 8 * ARRAY_OFFSET_AMOUNT, "i32");
    const list_pointer = getValue(state_pointer + 9 * ARRAY_OFFSET_AMOUNT, "i32");
    incArgs.list = new List(list_pointer, false);
    return incArgs;
  }
}

class List {
  constructor(value, create = true) {
    if (create) {
      this.length = value;
      this.obj = _List_new(this.length);
    } else {
      this.obj = value;
      this.length = this.size();
    }
  }

  set(index, value) {
    _List_set(this.obj, index, value);
  }

  get(index) {
    return _List_get(this.obj, index);
  }

  size() {
    return _List_size(this.obj);
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
    this.arg6 = false;
    this.arg7 = false;
    this.arg8 = false;
  }

  get() {
    return _createAnimationArgs(
      this.animation,
      this.color,
      this.color_bg,
      this.colors.obj,
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

class IncrementArgs {
  constructor() {
    this.incId = 0;
    this.arg1 = 0;
    this.arg2 = 0;
    this.arg3 = 0;
    this.arg4 = 0;
    this.arg5 = 0;
    this.arg6 = false;
    this.arg7 = false;
    this.arg8 = false;
    this.list = new List(0);
  }
}
