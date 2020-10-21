/* exported PixelDisplay */
/* globals PixelStrip */

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
  }

  fetchSimulate() {
    console.log('POIPOI');
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

  addPixelStrip(name) {
    const div = document.createElement('div');

    const controller = this.controllers[name];
    this.pixel_strips[name] = new PixelStrip(div, name, controller);

    div.className = 'section-flex';


    this.div.appendChild(div);
  }
}
