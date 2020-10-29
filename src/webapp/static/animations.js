/* exported Animations */
/* globals groups colors */

class Animations {
  constructor() {
    this.column_args = [
      'animation',
      'color',
      'color_bg',
      'colors',
      'arg1',
      'arg2',
      'arg3',
      'arg4',
      'arg5',
      'arg6',
      'arg7',
      'arg8',
    ];
    const table = document.getElementById('animations-table');
    this.table = table.getElementsByTagName('tbody')[0];
    this.animations = [];
    this.args = {};
    this.getAnimations();
  }

  getAnimations() {
    fetch('/getanimations')
        .then((response) => response.json())
        .then((animations) => {
          this.animations = animations['animations'];
          this.args = animations['args'];
          const num_animations = Object.keys(this.animations).length;
          for (let i = 0; i < num_animations; i++) {
            this.addRow(Object.keys(this.animations)[i]);
          }
        });
  }

  createAnimationSelector(row_id, animation) {
    const id = row_id + '-animation';
    const animations = Object.keys(this.animations);
    return createSelect(id, animations, animation);
  }

  createArg(arg, row_id, value) {
    const id = row_id + '-' + arg;
    let input;
    if (this.args[arg] == 'unsigned_int') {
      input = createNumber(id, value);
      input.min = 0;
    } else if (this.args[arg] === 'int') {
      input = createNumber(id, value);
    } else if (this.args[arg] === 'bool') {
      input = createSelect(id, [true, false], value);
    } else if (this.args[arg] == 'color_list') {
      input = createTextBox(id, value);
      input.className = 'width-8';
    } else if (this.args[arg] == 'color') {
      input = createTextBox(id, value);
      input.className = 'width-5';
    } else {
      console.log('Invalid arg type:', this.args[arg]);
    }
    return input;
  }

  addRow(animation) {
    if (!(animation in this.animations)) {
      return;
    }
    const row_id = 'animation-table-item-' + this.table.rows.length;
    const label_row = this.table.insertRow();
    const input_row = this.table.insertRow();
    for (let i = 0; i < 16; i++) {
      const label_cell = label_row.insertCell();
      const input_cell = input_row.insertCell();
      label_cell.className = 'text-0-75';
      if (i == 0) {
        label_cell.textContent = '';
        label_cell.textContent = 'Animation';
        input_cell.textContent = '';
        input_cell.appendChild(this.createAnimationSelector(row_id, animation));
      } else if (i == 12) {
        input_cell.appendChild(createNumber(row_id + '-waitms', 40));
      } else if (i == 13) {
        input_cell.appendChild(createNumber(row_id + '-steps', 1));
      } else if (i == 14) {
        input_cell.appendChild(createNumber(row_id + '-target', -1));
      } else if (i == 15) {
        input_cell.textContent = '';
        const send = createButton(row_id, 'Send', () => {
          this.send(row_id);
        });
        send.className = 'width-5';
        input_cell.appendChild(send);
      } else {
        if (this.column_args[i] in this.animations[animation]) {
          const arg = this.animations[animation][this.column_args[i]];
          label_cell.textContent = arg['label'];
          input_cell.appendChild(
              this.createArg(this.column_args[i], row_id, arg['default']));
        }
      }
    }
  }

  getAnimationNum(id) {
    const div = document.getElementById(id);
    console.log(div.value);
    return Object.keys(this.animations).indexOf(div.value);
  }

  getColorsList(colors_value) {
    const color_list = [];
    for (let i = 0; i < colors_value.length; i++) {
      const color = colors_value[i].trim();
      color_list.push(colors.getColorValue(color));
    }
    return color_list;
  }

  send(id) {
    colors.status = createStatus();
    const color_input = getInputValue(id + '-color', 'black');
    const color_list = this.getColorsList(color_input.split(','));
    console.log(color_list);
    const colors_input = getInputValue(id + '-colors', 'red, green, blue');
    const colors_list = this.getColorsList(colors_input.split(','));
    const ids = groups.getStripsFromGroup(getInputValue(id + '-target', 0));
    const payload = [];
    for (let i = 0; i < ids.length; i++) {
      payload.push({
        'animation': this.getAnimationNum(id + '-animation'),
        'color': color_list[0],
        'color_bg':
            colors.getColorValue(getInputValue(id + '-color_bg', 'none')),
        'colors': colors_list,
        'arg1': getInputValue(id + '-arg1', 0),
        'arg2': getInputValue(id + '-arg2', 0),
        'arg3': getInputValue(id + '-arg3', 0),
        'arg4': getInputValue(id + '-arg4', 0),
        'arg5': getInputValue(id + '-arg5', 0),
        'arg6': stringToBool(getInputValue(id + '-arg6', false)),
        'arg7': stringToBool(getInputValue(id + '-arg7', false)),
        'arg8': stringToBool(getInputValue(id + '-arg8', false)),
        'wait_ms': getInputValue(id + '-waitms', 0),
        'inc_steps': getInputValue(id + '-steps', 0),
        'id': ids[i],
      });
    }
    if (colors.status.error) {
      alert(colors.status.message);
      return;
    }
    console.log('Sending', payload);
    fetch('/data', {
      method: 'post',
      body: JSON.stringify(payload),
    })
        .then((response) => response.json())
        .then((response) => {
          console.debug('Animations Recieved', response);
          if (response.error) {
            // alert(`Failed to send to ${JSON.stringify(response.message)}`);
          }
        });
  }
}
