/* exported PixelDisplay */
/* globals PixelStrip */

const MAX_PIXEL_VW = 70;

class PixelDisplay {
  constructor() {
    socket.on('pixels', (data) => {
      console.debug(data);
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
          this.controllers = data['controllers'];
          this.num_controllers = Object.keys(this.controllers).length;
          for (let i = 0; i < this.num_controllers; i++) {
            this.addPixelStrip(Object.keys(this.controllers)[i]);
          }
        });
  }

  setupEventListeners() {
    this.pixel_per_row = document.getElementById('pixel-display-pixel-per-row');
    this.pixel_per_row.addEventListener('input', () => {
      const value = this.pixel_per_row.value;
      if (value != 'auto' && value >= 10 && value <= 150) {
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
    });
  }

  addPixelStrip(name) {
    const div = document.createElement('div');

    const controller = this.controllers[name];
    this.pixel_strips[name] = new PixelStrip(div, name, controller);

    div.className = 'section-flex';


    this.div.appendChild(div);
  }

  resizeTables(width) {
    Object.keys(this.pixel_strips).forEach((strip) => {
      this.pixel_strips[strip].resizeTable(width);
    });
  }

  resizePixel(width) {
    document.documentElement.style.setProperty('--pixel-width', `${width}vw`);
  }
}
