/* exported Colors */
/* globals groups */

class Colors {
  constructor() {
    this.noedit = document.getElementById('colors-noedit');
    this.edit = document.getElementById('colors-edit');
    this.status = createStatus();
    this.visible = 0;
    this.num_custom = 0;
    this.colors = {};
    this.colors_list = {};
    this.getColors();
    this.setupEventListeners();
  }

  setupEventListeners() {
    document.getElementById('colors-add').addEventListener('click', () => {
      this.addColor();
    });
    document.getElementById('colors-remove').addEventListener('click', () => {
      this.removeColor();
    });
  }

  getColors() {
    fetch('/getcolors').then((response) => response.json()).then((colors) => {
      this.colors_data = colors.colors;
      const num_noedit = Object.keys(this.colors_data.noedit).length;
      for (let i = 0; i < num_noedit; i++) {
        const color = this.colors_data.noedit[i];
        this.addNoedit(color);
        this.addColorFromConfig(color.name, () => {
          return color.value;
        });
      }
      const num_edit = Object.keys(this.colors_data.edit).length;
      for (let i = 0; i < num_edit; i++) {
        const color = this.colors_data.edit[i];
        const ranges = this.addEditable(
            color.name, color.value[0], color.value[1], color.value[2],
            color.visible);
        this.addColorFromConfig(color.name, () => {
          return [ranges[0].value, ranges[1].value, ranges[2].value];
        });
      }
      for (let i = 0; i < num_edit / 2; i++) {
        this.removeColor();
      }
    });
  }

  addColorFromConfig(color, getValue) {
    this.colors[color] = getValue;
  }

  addColor() {
    if (this.visible < this.num_custom) {
      document.getElementById(`colors-custom-${this.visible}`).style.display =
          'flex';
      this.visible += 1;
    } else {
      this.addEditable(`custom_${this.visible + 1}`, 255, 255, 255);
    }
  }

  removeColor() {
    if (this.visible < 1) {
      return;
    }
    this.visible -= 1;
    document.getElementById(`colors-custom-${this.visible}`).style.display =
        'none';
  }

  addNoedit(color) {
    const button = createButton(null, color.name, () => {
      this.send(
          'colors-noedit-target',
          combineRGB(color.value[0], color.value[1], color.value[2]));
    });
    button.className = 'width-7-5';
    this.noedit.appendChild(button);
  }

  getColorValue(color) {
    if (color === 'none') {
      return -1;
    }
    if (!isNaN(color)) {
      return parseInt(color);
    }
    if (color in this.colors) {
      const color_list = this.colors[color]();
      if (color_list === undefined) {
        this.status.error = true;
        this.status.message = `Invalid color ${color}`;
        return 0;
      }
      return combineRGB(color_list[0], color_list[1], color_list[2]);
    } else {
      this.status.error = true;
      this.status.message = `Invalid color ${color}`;
    }
  }

  generateBackground(r_range, g_range, b_range) {
    return `rgb(${r_range.value}, ${g_range.value}, ${b_range.value})`;
  }

  addEditable(name, r, g, b, visible = true) {
    this.visible += 1;
    const row_num = this.num_custom;
    this.num_custom += 1;
    const id = 'colors-custom-' + row_num;
    const div = document.createElement('div');
    const name_title = createSecondTitle(id + '-name', name);
    const r_range = createRange(id + '-r', r, 0, 255);
    const g_range = createRange(id + '-g', g, 0, 255);
    const b_range = createRange(id + '-b', b, 0, 255);
    const r_text = createSecondTitle(id + '-r-text', r);
    const g_text = createSecondTitle(id + '-g-text', g);
    const b_text = createSecondTitle(id + '-b-text', b);
    const color_display = document.createElement('div');
    const target = createSecondTitle(null, 'Target:');
    const send = createButton(id + '-send', 'Send');

    name_title.classList.add('width-10');
    r_range.addEventListener('input', () => {
      r_text.textContent = r_range.value;
      color_display.style.backgroundColor =
          this.generateBackground(r_range, g_range, b_range);
    });
    g_range.addEventListener('input', () => {
      g_text.textContent = g_range.value;
      color_display.style.backgroundColor =
          this.generateBackground(r_range, g_range, b_range);
    });
    b_range.addEventListener('input', () => {
      b_text.textContent = b_range.value;
      color_display.style.backgroundColor =
          this.generateBackground(r_range, g_range, b_range);
    });
    r_text.classList.add('width-3');
    g_text.classList.add('width-3');
    b_text.classList.add('width-3');
    color_display.className = 'color-sample-display';
    color_display.id = id + '-color-display';
    color_display.style.backgroundColor =
        this.generateBackground(r_range, g_range, b_range);
    target.classList.add('width-5');
    div.className = 'section-flex';
    div.id = id;
    send.addEventListener('click', () => {
      this.send(
          id + '-target',
          combineRGB(r_range.value, g_range.value, b_range.value));
    });

    div.appendChild(name_title);
    div.appendChild(r_range);
    div.appendChild(g_range);
    div.appendChild(b_range);
    div.appendChild(createSpaceS2());
    div.appendChild(r_text);
    div.appendChild(g_text);
    div.appendChild(b_text);
    div.appendChild(createSpaceS2());
    div.appendChild(color_display);
    div.appendChild(createSpaceS2());
    div.appendChild(target);
    div.appendChild(createNumber(id + '-target', -1));
    div.appendChild(createSpaceS2());
    div.appendChild(send);
    this.edit.appendChild(div);

    return [r_range, g_range, b_range];
  }

  send(id, color) {
    const ids = groups.getStripsFromGroup(getInputValue(id, 0));
    const payload = [];
    for (let i = 0; i < ids.length; i++) {
      payload.push({
        'animation': 0,
        'color': color,
        'color_bg': 0,
        'colors': [],
        'arg1': 0,
        'arg2': 0,
        'arg3': 0,
        'arg4': 0,
        'arg5': 0,
        'arg6': false,
        'arg7': false,
        'arg8': false,
        'wait_ms': 40,
        'inc_steps': 1,
        'id': ids[i],
      });
    }
    console.log('Sending', payload);
    fetch('/data', {method: 'post', body: JSON.stringify(payload)});
  }
}
