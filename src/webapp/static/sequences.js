/* exported Sequences */

class Sequences {
  constructor() {
    socket.on('start_sequence', (data) => {
      console.log('Start Sequence', data);
      this.startSequence(data);
    });
    socket.on('stop_sequence', (data) => {
      console.log('Stop Sequence', data);
      this.stopSequence(data);
    });
    this.div = document.getElementById('sequences-div');
    this.status = createStatus();
    this.visible = 0;
    this.num_custom = 0;
    this.buttons = {};
    this.getSequences();
    this.setupEventListeners();
  }

  setupEventListeners() {
    document.getElementById('sequences-add').addEventListener('click', () => {
      this.addSequence();
    });
    document.getElementById('sequences-remove')
        .addEventListener('click', () => {
          this.removeSequence();
        });
    document.getElementById('sequences-stopall')
        .addEventListener('click', () => {
          fetch('/sequence/stopall');
        });
  }

  getSequences() {
    fetch('/getsequences').then((response) => response.json()).then((data) => {
      console.log('Recieved Sequences', data.sequences);
      for (let i = 0; i < data.sequences.length; i++) {
        this.createSequence(data.sequences[i]);
      }
    });
  }

  addSequence() {
    if (this.visible < this.num_custom) {
      document.getElementById(`sequences-div-${this.visible}`).style.display =
          'flex';
      this.visible += 1;
    } else {
      this.createSequence(`custom_${this.visible + 1}`, 255, 255, 255);
    }
  }

  removeSequence() {
    if (this.visible < 1) {
      return;
    }
    this.visible -= 1;
    document.getElementById(`sequences-div-${this.visible}`).style.display =
        'none';
  }

  createSequence(data) {
    console.log('Create', data);
    this.visible += 1;
    const row_num = this.num_custom;
    this.num_custom += 1;
    const name = data.name;
    const id = 'sequences-' + row_num;
    const div = createSectionFlex();
    const title = createSecondTitle(`${id}-name`, name);
    const functions = createSectionFlexNoBorder();

    for (let i = 0; i < data.functions.length; i++) {
      const function_name = data.functions[i];
      const button = createButton(
          `sequences-function-${name}-${function_name}`, function_name);
      button.addEventListener('click', () => {
        this.send(name, function_name);
      });
      this.buttons[name] = button;
      functions.appendChild(button);
    }

    div.appendChild(title);
    div.appendChild(createDivider());
    div.appendChild(functions);
    this.div.appendChild(div);
    return;
  }

  send(sequence_name, function_name, iterations = null) {
    console.log(
        `Sequence Send: ${sequence_name} with function ${function_name}`);
    let parameters = `sequence=${sequence_name}&function=${function_name}`;
    if (iterations != null) {
      parameters += `&iterations=${iterations}`;
    }
    fetch(`/sequence/start?${parameters}`);
  }

  startSequence(data) {
    const id = `sequences-function-${data.name}`;
    const button = document.getElementById(id);
    button.style.border = '0.1vw solid var(--highlight-color)';
  }

  stopSequence(data) {
    const id = `sequences-function-${data.name}`;
    const button = document.getElementById(id);
    button.style.border = '0.1vw solid var(--input-border)';
  }
}
