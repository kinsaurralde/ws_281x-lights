/* exported Sequences */

class Sequences {
  constructor() {
    this.div = document.getElementById('sequences-div');
    this.status = createStatus();
    this.visible = 0;
    this.num_custom = 0;
    this.colors = {};
    this.colors_list = {};
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
      document.getElementById(`colors-custom-${this.visible}`).style.display =
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
    document.getElementById(`colors-custom-${this.visible}`).style.display =
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
      const button = createButton(
          `${id}-function-${data.functions[i]}`, data.functions[i]);
      button.addEventListener('click', () => {
        this.send(name, data.functions[i]);
      });
      functions.appendChild(button);
    }

    div.appendChild(title);
    div.appendChild(createDivider());
    div.appendChild(functions);
    this.div.appendChild(div);
    return;
  }

  send(sequence_name, function_name) {
    console.log(
        `Sequence Send: ${sequence_name} with function ${function_name}`);
    fetch(`/sequence/start/${sequence_name}/${function_name}`);
  }
}
