/* exported BufferedCall */

class BufferedCall {
  constructor(callback, wait_ms) {
    this.waiting = false;
    this.values = {};
    this.callback = callback;
    this.wait_ms = wait_ms;
  }

  add(values) {
    for (const value in values) {
      if (values.hasOwnProperty(value)) {
        this.values[value] = values[value];
      }
    }
    if (!this.waiting) {
      this.waiting = true;
      setTimeout(() => {
        this.callback(this.values);
        this.waiting = false;
        this.values = {};
      }, this.wait_ms);
    }
  }
}
