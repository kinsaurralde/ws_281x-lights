/* exported Controllers */
/* globals socket */

class Controllers {
  constructor() {
    const table = document.getElementById('controller-table');
    this.table = table.getElementsByTagName('tbody')[0];
    this.num_controllers = 0;
    this.num_strips = 0;
    this.controllers = {};
    this.brightness_link = [];
    this.fetchControllers();
  }

  fetchControllers() {
    fetch('/getcontrollers')
        .then((response) => response.json())
        .then((controllers) => {
          console.log('Recieved Controllers', controllers);
          this.controllers = controllers;
          this.num_controllers = Object.keys(this.controllers).length;
          for (let i = 0; i < this.num_controllers; i++) {
            this.addRow(this.controllers[Object.keys(this.controllers)[i]]);
          }
          loadedControllers();
        });
  }

  getNames() {
    return Object.keys(this.controllers);
  }

  sendBrightness(name, value, index) {
    if (this.brightness_link[index].checked) {
      const values = [];
      for (let i = 0; i < this.brightness_link.length; i++) {
        if (this.brightness_link[i].checked) {
          values.push({
            'name': this.brightness_link[i].name,
            'value': value,
          });
          this.brightness_link[i].slider.value = value;
          this.brightness_link[i].text.textContent = value;
        }
      }
      socket.emit('set_brightness', values);
    } else {
      socket.emit('set_brightness', [{'name': name, 'value': value}]);
    }
  }

  addRow(controller) {
    console.log('Adding', controller);
    this.num_strips += 1;
    const id = 'controllers-table-' + controller.id;

    this.brightness_link.push(false);
    const box = createCheckBox(id + '-checkbox', false, null);

    const name = createSecondTitle(id + '-name', controller.name);
    const brightness_slider = createRange(
        id + '-brightness-slider', controller.init.brightness, 0, 255);
    const brightness_value = document.createElement('span');

    const index = this.num_strips - 1;
    box.addEventListener('input', () => {
      this.brightness_link[index] = {
        'checked': box.checked,
        'name': controller.name,
        'slider': brightness_slider,
        'text': brightness_value,
      };
    });
    brightness_slider.addEventListener('input', () => {
      brightness_value.textContent = brightness_slider.value;
      this.sendBrightness(controller.name, brightness_slider.value, index);
    });
    brightness_value.className = 'section-title-secondary';
    brightness_value.textContent = controller.init.brightness;

    const row = this.table.insertRow();
    const cells = [];
    for (let i = 0; i < 5; i++) {
      cells.push(row.insertCell());
    }
    cells[0].appendChild(name);
    cells[1].appendChild(box);
    cells[1].appendChild(brightness_slider);
    cells[1].appendChild(brightness_value);
    cells[2].textContent = controller.init.num_leds;
    cells[3].textContent = controller.init.milliwatts;
    cells[4].textContent = this.num_strips - 1;
  }
}
