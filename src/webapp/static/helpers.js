/* eslint-disable no-unused-vars, no-redeclare */

function createButton(id, text, onclick = null) {
  const button = document.createElement('button');
  button.type = 'button';
  button.textContent = text;
  button.id = id;
  button.addEventListener('click', onclick);
  return button;
}

function createNumber(id, value, oninput = null) {
  const number = document.createElement('input');
  number.type = 'number';
  number.id = id;
  number.value = value;
  number.addEventListener('input', oninput);
  return number;
}

function createTextBox(id, value, is_placeholder = false, oninput = null) {
  const text = document.createElement('input');
  text.type = 'text';
  text.id = id;
  if (is_placeholder) {
    text.placeholder = value;
  } else {
    text.value = value;
  }
  text.addEventListener('input', oninput);
  return text;
}

function createSelect(id, values, initial, oninput = null) {
  const select = document.createElement('select');
  select.id = id;
  for (let i = 0; i < values.length; i++) {
    const option = document.createElement('option');
    option.textContent = values[i];
    option.value = values[i];
    select.appendChild(option);
  }
  select.value = initial;
  select.addEventListener('input', oninput);
  return select;
}

function createRange(id, value, min, max, oninput = null) {
  const range = document.createElement('input');
  range.type = 'range';
  range.id = id;
  range.min = min;
  range.max = max;
  range.value = value;
  range.addEventListener('input', oninput);
  return range;
}

function createCheckBox(id, checked, oninput = null) {
  const checkbox = document.createElement('input');
  checkbox.type = 'checkbox';
  checkbox.id = id;
  checkbox.checked = checked;
  checkbox.addEventListener('click', oninput);
  return checkbox;
}

function createSecondTitle(id, value) {
  const div = document.createElement('div');
  div.id = id;
  div.className = 'section-title-secondary';
  div.textContent = value;
  return div;
}

function createSpaceS2() {
  const div = document.createElement('div');
  div.className = 'space-s-2';
  return div;
}

function createDivider() {
  const div = document.createElement('div');
  div.className = 'divider';
  return div;
}

function createVDivider() {
  const div = document.createElement('div');
  div.className = 'v-divider';
  return div;
}

function createSectionFlex() {
  const div = document.createElement('div');
  div.className = 'section-flex';
  return div;
}

function createSectionFlexNoBorder() {
  const div = document.createElement('div');
  div.className = 'section-flex-no-border';
  return div;
}

function getInputValue(id, blank = null) {
  const div = document.getElementById(id);
  if (div == null) {
    return blank;
  }
  return div.value;
}

function stringToBool(string) {
  if (typeof string === 'boolean') {
    return string;
  }
  if (string.toLowerCase() == 'true') {
    return true;
  }
  return false;
}

function combineRGB(r, g, b) {
  return ((r & 0xff) << 16) | ((g & 0xff) << 8) | (b & 0xff);
}

function splitRGB(value) {
  return {
    r: value >> 16,
    g: (value >> 8) & 0xff,
    b: value & 0xff,
  };
}

function createStatus() {
  return {
    error: false,
    message: '',
  };
}

function showSection(id) {
  document.getElementById(id).style.display = 'block';
}

function hideSection(id) {
  document.getElementById(id).style.display = 'none';
}

/* eslint-enable no-unused-vars */
