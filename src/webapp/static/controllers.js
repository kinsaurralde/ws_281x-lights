/* exported Controllers */
/* globals loadedControllers */

const TABLE_COLUMNS = 7;
const STATUS_COLUMNS = 6;

const BRIGHTNESS_DELAY_MS = 100;

const GOOD = 'GOOD';
const WARNING = 'WARNING';
const ERROR = 'ERROR';
const FALSE = 'FALSE';
const TRUE = 'TRUE';
const PLAIN = 'PLAIN';
const UNKNOWN = 'UNKNOWN';

class Controllers {
  constructor() {
    socket.on('update', (data) => {
      this.handleUpdate(data);
    });
    socket.on('brightness', (data) => {
      this.handleBrightness(data);
    });
    const table = document.getElementById('controller-table');
    const status_table = document.getElementById('status-table');
    this.table = table.getElementsByTagName('tbody')[0];
    this.status_table = status_table.getElementsByTagName('tbody')[0];
    this.status = {};
    this.urls = {};
    this.num_controllers = 0;
    this.num_strips = 0;
    this.controllers = {};
    this.brightness_link = {};
    this.brightness_values = {};
    this.fetchControllers();
    this.fetchInitialized();
    this.fetchVersionInfo();
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

  fetchInitialized() {
    fetch('/getinitialized')
        .then((response) => response.json())
        .then((initialized) => {
          console.log('Recieved Initialized', initialized);
          this.handleInitialzedResponse(initialized);
        });
  }

  handleUpdate(data) {
    console.debug(data);
    if ('ping' in data) {
      this.updatePing(data.ping);
    }
    if ('initialized' in data) {
      this.handleInitialzedResponse(data['initialized']);
    }
    if ('version' in data) {
      this.handleVersionInfoResponse(data['version']);
    }
  }

  handleInitialzedResponse(initialized) {
    for (const name in initialized.initialized) {
      if (name in initialized.initialized) {
        this.setStatusInitialized(
            name, initialized.initialized[name] ? TRUE : FALSE);
      }
    }
  }

  handleBrightness(data) {
    for (let i = 0; i < data.length; i++) {
      if (data[i].name in this.controllers) {
        this.setBrightness(data[i].name, parseInt(data[i].value));
      }
    }
  }

  fetchVersionInfo() {
    fetch('/getversioninfo')
        .then((response) => response.json())
        .then((version_info) => {
          console.log('Recieved Version Info', version_info);
          this.handleVersionInfoResponse(version_info);
        });
  }

  handleVersionInfoResponse(version_info) {
    const major = version_info.webapp.major;
    const minor = version_info.webapp.minor;
    const patch = version_info.webapp.patch;
    const label = version_info.webapp.label;
    const version = `${major}.${minor}.${patch}_${label}`;
    const esp_hash = version_info.webapp.esp_hash;
    const rpi_hash = version_info.webapp.rpi_hash;
    document.getElementById('status-webapp-version').textContent = version;
    document.getElementById('status-webapp-esphash').textContent = esp_hash;
    document.getElementById('status-webapp-rpihash').textContent = rpi_hash;
    for (const controller in version_info.versioninfo) {
      if (controller in version_info.versioninfo) {
        const data = version_info.versioninfo[controller];
        const version_string = `${data.major}.${data.minor}.${data.patch}`;
        const version_match = (major === data.major && minor === data.minor);
        const full_version_match = (version_match && patch === data.patch);
        const status =
            full_version_match ? GOOD : version_match ? WARNING : ERROR;
        this.setStatusVersion(controller, status, version_string);
        const hash_match =
            esp_hash === data.esp_hash && rpi_hash === data.rpi_hash;
        this.setStatusHashMatch(controller, hash_match ? TRUE : FALSE);
      }
    }
  }

  updatePing(data) {
    for (const controller in this.controllers) {
      if (controller in this.controllers) {
        const div =
            document.getElementById(`controllers-table-${controller}-ping`);
        const div_mode_select =
            document.getElementById(`status-table-${controller}-active`);
        if (controller in data) {
          if (data[controller] === null) {
            this.setStatus(div, FALSE, 'DISCONNECTED');
            this.setStatusConnected(controller, FALSE, 'DISCONNECTED');
          } else if (data[controller] === 'disabled') {
            div_mode_select.value = 'disabled';
            this.setStatus(div, FALSE, 'DISABLED');
            this.setStatusConnected(controller, FALSE, 'DISABLED');
          } else {
            this.setStatus(div, PLAIN, data[controller].toFixed(3));
            this.setStatusConnected(controller, TRUE);
          }
        } else {
          this.setStatus(div, FALSE, 'DISABLED');
          this.setStatusConnected(controller, FALSE, 'DISABLED');
        }
      }
    }
  }

  setStatus(div, type, text = null) {
    div.classList.remove(...div.classList);
    div.classList.add('section-title-secondary');
    if (text === null) {
      div.textContent = type;
    } else {
      div.textContent = text;
    }
    if (type === WARNING) {
      div.classList.add('yellow');
    } else if (type === GOOD || type === TRUE) {
      div.classList.add('green');
    } else if (type === PLAIN) {
      div.classList.add('white');
    } else {
      div.classList.add('red');
    }
  }

  setStatusInitialized(name, value) {
    if (name in this.status) {
      this.status[name].initialized = value;
      const div = document.getElementById(`status-table-${name}-initialized`);
      this.setStatus(div, value);
    }
  }

  setStatusVersion(name, value, text) {
    if (name in this.status) {
      this.status[name].version = value;
      const div = document.getElementById(`status-table-${name}-version`);
      this.setStatus(div, value, text);
    }
  }

  setStatusHashMatch(name, value) {
    if (name in this.status) {
      this.status[name].hash_match = value;
      const div = document.getElementById(`status-table-${name}-hashmatch`);
      this.setStatus(div, value);
      this.setOverallStatus(name);
    }
  }

  setStatusConnected(name, value, text) {
    if (name in this.status) {
      this.status[name].connected = value;
      const div = document.getElementById(`status-table-${name}-connected`);
      this.setStatus(div, value, text);
      this.setOverallStatus(name);
    }
  }

  setOverallStatus(name) {
    if (name in this.status) {
      let good = true;
      let warn = false;
      if (this.status[name].initialized === FALSE) {
        good = false;
      }
      if (this.status[name].version === ERROR) {
        good = false;
      }
      if (this.status[name].version === WARNING) {
        good = false;
        warn = true;
      }
      if (this.status[name].hash_match === FALSE) {
        good = false;
        warn = true;
      }
      if (this.status[name].connected === FALSE) {
        good = false;
      }
      const div = document.getElementById(`controllers-table-${name}-status`);
      this.setStatus(div, good ? GOOD : warn ? WARNING : ERROR);
    }
  }

  getNames() {
    return Object.keys(this.controllers);
  }

  getIsActive() {
    const result = {};
    Object.keys(this.controllers).forEach((controller) => {
      result[controller] = this.controllers[controller].active;
    });
    return result;
  }

  setBrightness(name, value) {
    const id = `controllers-table-${name}-brightness-`;
    if (document.getElementById(id + 'slider') != null) {
      document.getElementById(id + 'slider').value = value;
      document.getElementById(id + 'value').textContent = value;
    }
  }

  sendBrightness(name, value) {
    if (this.brightness_link[name].checked) {
      for (const controller in this.brightness_link) {
        if (controller in this.brightness_link) {
          if (this.brightness_link[controller].checked) {
            this.brightness_values[controller] = value;
            this.brightness_link[controller].slider.value = value;
            this.brightness_link[controller].text.textContent = value;
          }
        }
      }
    } else {
      this.brightness_link[name].text.textContent = value;
      this.brightness_values[name] = value;
    }
    if (!this.controllers[name].brightness_wait) {
      this.controllers[name].brightness_wait = true;
      setTimeout(() => {
        const values = [];
        for (const name in this.brightness_values) {
          if (name in this.brightness_values) {
            values.push({
              'name': name,
              'value': this.brightness_values[name],
            });
          }
        }
        this.brightness_values = {};
        this.controllers[name].brightness_wait = false;
        socket.emit('set_brightness', values);
      }, BRIGHTNESS_DELAY_MS);
    }
  }

  addRow(controller) {
    console.log('Adding controller', controller);
    this.controllers[controller.name].brightness_wait = false;
    if (!(controller.url in this.urls)) {
      this.urls[controller.url] = [];
    }
    this.urls[controller.url].push(controller.name);
    this.num_strips += 1;
    const id = 'controllers-table-' + controller.name;

    const box = createCheckBox(id + '-checkbox', false, null);

    const name = createSecondTitle(id + '-name', controller.name);
    const brightness_slider = createRange(
        id + '-brightness-slider', controller.init.brightness, 0, 255);
    const brightness_value = document.createElement('span');
    brightness_value.id = id + '-brightness-value';

    const ping = createSecondTitle(id + '-ping', '---');

    const status = document.createElement('div');
    status.id = id + '-status';
    this.setStatus(status, UNKNOWN);

    this.brightness_link[controller.name] = {
      'checked': box.checked,
      'name': controller.name,
      'slider': brightness_slider,
      'text': brightness_value,
    };
    box.addEventListener('input', () => {
      this.brightness_link[controller.name].checked = box.checked;
    });
    brightness_slider.addEventListener('input', () => {
      this.sendBrightness(controller.name, brightness_slider.value);
    });
    brightness_value.className = 'section-title-secondary';
    brightness_value.textContent = controller.init.brightness;

    const row = this.table.insertRow();
    const cells = [];
    for (let i = 0; i < TABLE_COLUMNS; i++) {
      cells.push(row.insertCell());
    }
    cells[0].appendChild(name);
    cells[1].appendChild(box);
    cells[1].appendChild(brightness_slider);
    cells[1].appendChild(brightness_value);
    cells[2].textContent = controller.init.num_leds;
    cells[3].textContent = controller.init.milliwatts;
    cells[4].textContent = this.num_strips - 1;
    cells[5].appendChild(ping);
    cells[6].appendChild(status);

    this.addStatusRow(controller.name, controller.active);
  }

  addStatusRow(name, initial_mode) {
    this.status[name] = {
      'initialized': UNKNOWN,
      'version': UNKNOWN,
      'hash_match': UNKNOWN,
      'connected': FALSE,
    };
    const row = this.status_table.insertRow();
    const cells = [];
    for (let i = 0; i < STATUS_COLUMNS; i++) {
      cells.push(row.insertCell());
    }
    const id = 'status-table-' + name;
    const display_name = createSecondTitle(id + '-name', name);
    const initialized = document.createElement('div');
    const connected = document.createElement('div');
    const version = document.createElement('div');
    const hash_match = document.createElement('div');
    const mode = createSelect(
        id + '-active',
        [
          'active',
          'disabled',
        ],
        initial_mode);
    mode.addEventListener('input', () => {
      this.changeMode(name, mode.value);
      const url = this.controllers[name].url;
      for (let i = 0; i < this.urls[url].length; i++) {
        document.getElementById(`status-table-${this.urls[url][i]}-active`)
            .value = mode.value;
      }
    });
    this.setStatus(initialized, UNKNOWN);
    this.setStatus(connected, UNKNOWN);
    this.setStatus(version, UNKNOWN);
    this.setStatus(hash_match, UNKNOWN);

    initialized.id = id + '-initialized';
    connected.id = id + '-connected';
    version.id = id + '-version';
    hash_match.id = id + '-hashmatch';

    cells[0].appendChild(display_name);
    cells[1].appendChild(initialized);
    cells[2].appendChild(connected);
    cells[3].appendChild(version);
    cells[4].appendChild(hash_match);
    cells[5].appendChild(mode);
  }

  changeMode(name, mode) {
    if (mode === 'active') {
      fetch(`/enable?name=${name}`);
    } else if (mode === 'noreconnect') {
      () => {};  // PASS
    } else if (mode === 'disabled') {
      fetch(`/disable?name=${name}`);
    }
  }
}
