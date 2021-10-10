const controllers_tile_container = document.getElementById('Controllers-container');
const controllers_row_container = document.getElementById('expanded-controllers-area');

class Controllers {
  constructor() {
    socket.on('rtt', (data) => {
      console.log(data);
      for (const controller in data) {
        if (data.hasOwnProperty(controller)) {
          if (controller in this.controllers) {
            this.controllers[controller].setPing(data[controller]);
          }
        }
      }
    });
    this.controllers = {};
  }

  getSelectedControllers() {
    const selected = [];
    for (const controller in this.controllers) {
      if (this.controllers.hasOwnProperty(controller)) {
        if (this.controllers[controller].selected) {
          selected.push(controller);
        }
      }
    }
    return selected;
  }

  addControllers(controllers) {
    for (const controller in controllers) {
      if (controllers.hasOwnProperty(controller)) {
        this.controllers[controller] = new Controller(controller, controllers[controller]);
      }
    }
  }
}

class Controller {
  constructor(name, properties) {
    this.name = name;
    this.url = properties['url'];
    this.ping = '---';
    this.status = 'ERROR';
    this.selected = false;
    this.debug_row = document.createElement('div');
    this.debug_row.className = 'controller-debug-row';
    this.tile = this.createTile();
    this.row = this.createRow();
    this.setPing('---');
    this.setSelected(properties['start_enabled']);
    controllers_tile_container.appendChild(this.tile);
    controllers_row_container.appendChild(this.row);
  }

  setPing(value) {
    this.ping = value;
    if (value == '---') {
      this.status = 'ERROR';
      this.tile.style.color = 'red';
    } else {
      this.status = 'GOOD';
      this.tile.style.color = 'green';
    }
    this.tile.innerText = `${this.name}\n${this.ping} ms\n${this.status}`;
  }

  setSelected(value) {
    this.selected = value;
    if (this.selected) {
      this.tile.style.borderColor = 'yellow';
    } else {
      this.tile.style.borderColor = 'white';
    }
  }

  createTile() {
    const button = document.createElement('button');
    button.id = `controller-tile-${this.name}`;
    button.className = 'mobile-button-box';
    button.addEventListener('click', () => {
      this.setSelected(!this.selected);
    });
    return button;
  }

  createRow() {
    const spacer = document.createElement('div');
    const v_divider = document.createElement('div');
    const divider = document.createElement('div');
    spacer.className = 'space-s-1';
    v_divider.className = 'v-divider';
    divider.className = 'divider';

    const container = document.createElement('div');
    const name = document.createElement('div');
    const rtt = document.createElement('div');
    const rtt_value = document.createElement('span');
    const brightness = document.createElement('div');
    const brightness_value = document.createElement('span');
    const brightness_slider = document.createElement('input');
    const debug_button = document.createElement('button');
    const debug_button_close = document.createElement('button');
    container.className = 'controller-container';
    name.textContent = this.name;
    container.appendChild(name);
    container.appendChild(v_divider.cloneNode());
    rtt.textContent = 'RTT (ms): ';
    rtt_value.textContent = '---';
    rtt.appendChild(rtt_value);
    container.appendChild(rtt);
    container.appendChild(v_divider.cloneNode());
    brightness.textContent = 'Brightness: ';
    brightness_value.textContent = 0;
    brightness.appendChild(brightness_value);
    container.appendChild(brightness);
    container.appendChild(spacer.cloneNode());
    brightness_slider.type = 'range';
    brightness_slider.min = 0;
    brightness_slider.max = 255;
    container.appendChild(brightness_slider);
    container.appendChild(v_divider.cloneNode());
    debug_button.textContent = 'Show/Refresh Debug Info';
    debug_button.addEventListener('click', () => {
      this.showDebugInfo();
    });
    container.appendChild(debug_button);
    debug_button_close.textContent = 'Hide Debug Info';
    debug_button_close.addEventListener('click', () => {
      this.hideDebugInfo();
    })
    container.appendChild(debug_button_close);
    container.appendChild(divider);
    container.appendChild(this.debug_row);
    return container;
  }

  showDebugInfo() {
    fetch(`http://${this.url}/`).then((response) => response.text()).then((data) => {
      const v_divider = document.createElement('div');
      v_divider.className = 'v-divider';
      this.hideDebugInfo();
      const rows = data.split('<br>');
      let debug_box = document.createElement('div');
      debug_box.className = 'controller-debug-box';
      for (let i = 0; i < rows.length; i++) {
        let row_text = rows[i];
        if (row_text.includes('<b>')) {
          if (debug_box.innerHTML.length > 0) {
            this.debug_row.appendChild(debug_box.cloneNode(true));
            this.debug_row.appendChild(v_divider.cloneNode());
            debug_box.innerHTML = '';
          }
          row_text = row_text.replace(/<\/*b>/g, '');
          // console.log("New Box", content, debug_box.cloneNode());
          // debug_box.textContent = content;
        }
        const row = document.createElement('div');
        row.textContent = row_text;
        debug_box.appendChild(row);
      }
      this.debug_row.appendChild(debug_box.cloneNode(true));
    });
  }

  hideDebugInfo() {
    this.debug_row.innerHTML = '';
  }
}


