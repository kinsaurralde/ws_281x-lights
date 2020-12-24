/* exported PixelDisplay */
/* globals PixelStrip controllers */

const MAX_PIXEL_VW = 70;
const MIN_PIXEL_COLS = 10;   // If changed, also change HTML
const MAX_PIXEL_COLS = 150;  // If changed, also change HTML

class PixelDisplay {
  constructor() {
    socket.on('pixels', (data) => {
      this.set(data);
    });
    this.div = document.getElementById('pixel-display');
    this.num_controllers = 0;
    this.controllers = {};
    this.pixel_strips = {};
    this.fetchSimulate();
    this.setupEventListeners();
  }

  fetchSimulate() {
    fetch('/getpixelsimulate')
        .then((response) => response.json())
        .then((data) => {
          // if (!data.active) {
          //   hideSection('section-display-wrapper');
          // }
          this.controllers = data['controllers'];
          this.num_controllers = Object.keys(this.controllers).length;
          for (let i = 0; i < this.num_controllers; i++) {
            this.addPixelStrip(Object.keys(this.controllers)[i]);
          }
          const activeControllers = controllers.getIsActive();
          Object.keys(activeControllers).forEach((controller) => {
            if (activeControllers[controller] != 'active') {
              this.pixel_strips[controller].hide();
            }
          });
          this.resize();
        });
  }

  setupEventListeners() {
    this.pixel_per_row = document.getElementById('pixel-display-pixel-per-row');
    this.pixel_per_row.addEventListener('input', () => {
      this.resize();
    });
  }

  addPixelStrip(name) {
    const div = document.createElement('div');
    const controller = this.controllers[name];
    this.pixel_strips[name] = new PixelStrip(div, name, controller);
    div.className = 'section-flex';
    this.div.appendChild(div);
  }

  resize() {
    const value = this.pixel_per_row.value;
    if (value != 'auto' && value >= MIN_PIXEL_COLS && value <= MAX_PIXEL_COLS) {
      const pixel_width = MAX_PIXEL_VW / value;
      if (value >= 120) {
        document.documentElement.style.setProperty('--pixel-margin', '0');
      } else {
        document.documentElement.style.setProperty(
            '--pixel-margin', 'var(--pixel-margin-normal)');
      }
      this.resizeTables(this.pixel_per_row.value);
      this.resizePixel(pixel_width);
    }
  }

  resizeTables(width) {
    Object.keys(this.pixel_strips).forEach((strip) => {
      this.pixel_strips[strip].resizeTable(width);
    });
  }

  resizePixel(width) {
    document.documentElement.style.setProperty('--pixel-width', `${width}vw`);
  }

  set(data) {
    Object.keys(data).forEach((strip) => {
      if (strip in this.controllers) {
        this.pixel_strips[strip].set(data[strip]);
      }
    });
  }
}
