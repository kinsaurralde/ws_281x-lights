/* globals send */
/* exported Animations */

class Animations {
  constructor() {
    this.animations = {};
    this.animation_args = {};
    this.large_tiles = [];
  }

  addAnimationArgs(args) {
    console.log(args);
    this.animation_args = args;
  }

  addAnimations(animations) {
    const animations_tile_div = document.getElementById('Animations-container');
    const expanded_animations_div = document.getElementById('expanded-animations-area');
    for (const animation in animations) {
      if (animations.hasOwnProperty(animation)) {
        const defaults = animations[animation];
        this.animations[animation] = defaults;
        if (defaults.web_options.tile) {
          animations_tile_div.appendChild(this.createAnimationTile(animation, defaults));
        }
        if (!(defaults.web_options.large_tile == false)) {
          expanded_animations_div.appendChild(this.createLargeAnimationTile(animation, defaults));
        }
      }
    }
  }

  createAnimationTile(animation, defaults) {
    const div = document.createElement('div');
    div.className = 'mobile-button-box';
    let display_name = animation;
    if ('tile_name' in defaults.web_options) {
      display_name = defaults.web_options['tile_name'];
    }
    div.textContent = display_name;
    div.addEventListener('click', () => {
      global_animations.runAnimation(animation);
    });
    return div;
  }

  createLargeAnimationTile(animation, defaults) {
    console.log(animation, defaults);
    const tile_index = this.large_tiles.length;
    this.large_tiles.push({
      type: animation,
    });

    const tile = document.createElement('div');
    tile.className = 'animation-container';

    const title = document.createElement('div');
    title.className = 'animation-title';
    title.textContent = animation;
    tile.appendChild(title);

    const args_container = document.createElement('div');
    args_container.className = 'animation-args-container';
    for (const arg in defaults) {
      if (defaults.hasOwnProperty(arg)) {
        args_container.appendChild(this.createAnimationArg(tile_index, arg, defaults[arg]));
      }
    }
    tile.appendChild(args_container);

    const send = document.createElement('div');
    send.className = 'animation-send color-button';
    send.textContent = 'Send';
    send.addEventListener('click', () => {
      this.runAnimation(animation, this.large_tiles[tile_index]);
    });
    tile.appendChild(send);

    return tile;
  }

  createAnimationArg(tile_index, arg, default_value) {
    const arg_container = document.createElement('div');
    arg_container.className = 'animation-arg';
    if (!(arg in this.animation_args) || arg === 'frame_multiplier') {
      return document.createElement('div');
    }
    const title = document.createElement('div');
    title.className = 'animation-arg-name';
    title.textContent = arg.charAt(0).toUpperCase() + arg.slice(1).replace('_', ' ');
    arg_container.appendChild(title);
    switch (this.animation_args[arg]['type']) {
      case 'color':
        arg_container.appendChild(this.createColorSelector(tile_index, arg, default_value));
        break;
      case 'int':
        if (arg == 'frame_ms') {
          arg_container.appendChild(this.createFrameMsSlider(tile_index, arg, default_value));
        } else {
          arg_container.appendChild(
              this.createSlider(
                  tile_index,
                  arg,
                  default_value,
                  this.animation_args[arg]['min'],
                  this.animation_args[arg]['max'],
              ),
          );
        }
        break;
      case 'bool':
        title.className = 'animation-arg-name-shortened';
        arg_container.appendChild(this.createToggle(tile_index, arg, default_value));
        break;
    }
    return arg_container;
  }

  runAnimation(animation, args = {}) {
    if (!(animation in this.animations)) {
      return;
    }
    for (const property in this.animations[animation]) {
      if (property in this.animations[animation]) {
        if (!(property in args)) {
          args[property] = this.animations[animation][property];
        }
      }
    }
    args = this.processArgs(args);
    args['type'] = animation;
    send([{controllers: ['all'], animation_args: args}]);
  }

  processArgs(args) {
    const processed_args = {};
    for (const arg in args) {
      if (arg in args) {
        switch (arg) {
          case 'color': {
            processed_args['color'] = global_colors.getColorValue(args['color']);
            break;
          }
          case 'colors': {
            processed_args['colors'] = this.getValuesOfColorList(args['colors'].split(','));
            break;
          }
          case 'tile':
          case 'tile_name':
            break;
          default:
            processed_args[arg] = args[arg];
        }
      }
    }
    return processed_args;
  }

  getValuesOfColorList(colors) {
    const values = [];
    for (let i = 0; i < colors.length; i++) {
      const value = global_colors.getColorValue(colors[i].trim());
      if (value) {
        values.push(value);
      }
    }
    return values;
  }

  createColorSelector(tile_index, arg_name, value) {
    const select = document.createElement('select');
    const colors = global_colors.getColorList();
    colors.unshift('random');
    colors.unshift('none');
    for (let i = 0; i < colors.length; i++) {
      const option = document.createElement('option');
      option.value = colors[i];
      option.textContent = colors[i];
      select.appendChild(option);
    }
    select.value = value;
    this.updateTileValue(tile_index, arg_name, select.value);
    select.addEventListener('input', () => {
      this.updateTileValue(tile_index, arg_name, select.value);
    });
    return select;
  }

  createSlider(tile_index, arg_name, value, min, max) {
    const container = document.createElement('div');
    const slider = document.createElement('input');
    const display = document.createElement('span');
    slider.addEventListener('input', () => {
      display.textContent = slider.value;
    });
    container.style.width = '100%';
    slider.type = 'range';
    slider.value = value;
    slider.min = min;
    slider.max = max;
    display.className = 'animation-arg-value';
    display.textContent = slider.value;
    container.appendChild(slider);
    container.appendChild(display);
    this.updateTileValue(tile_index, arg_name, slider.value);
    slider.addEventListener('input', () => {
      this.updateTileValue(tile_index, arg_name, slider.value);
    });
    return container;
  }

  createFrameMsSlider(tile_index, arg_name, value) {
    const container = document.createElement('div');
    const slider = document.createElement('input');
    const display = document.createElement('span');
    slider.addEventListener('input', () => {
      display.textContent = scaleFrameMs(slider.value);
    });
    container.style.width = '100%';
    slider.type = 'range';
    slider.value = value;
    slider.min = 0;
    slider.max = 100;
    display.className = 'animation-arg-value';
    display.textContent = slider.value;
    container.appendChild(slider);
    container.appendChild(display);
    this.updateTileValue(tile_index, arg_name, scaleFrameMs(slider.value));
    slider.addEventListener('input', () => {
      this.updateTileValue(tile_index, arg_name, scaleFrameMs(slider.value));
    });
    return container;
  }

  createToggle(tile_index, arg_name, value) {
    const toggle = document.createElement('input');
    toggle.type = 'checkbox';
    toggle.checked = value;
    this.updateTileValue(tile_index, arg_name, toggle.checked);
    toggle.addEventListener('input', () => {
      this.updateTileValue(tile_index, arg_name, toggle.checked);
    });
    return toggle;
  }

  updateTileValue(tile_index, arg_name, value) {
    if (tile_index < this.large_tiles.length) {
      this.large_tiles[tile_index][arg_name] = value;
    }
  }
}

function scaleFrameMs(value) {
  if (value <= 30) {
    return 20 + (value - 0);
  }
  if (value <= 50) {
    return 50 + (value - 30) * 5;
  }
  if (value <= 85) {
    return 150 + (value - 50) * 10;
  }
  if (value <= 95) {
    return 500 + (value - 85) * 25;
  }
  return 750 + (value - 95) * 50;
}
