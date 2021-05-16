/* exported Sequences */

class Sequences {
  constructor() {
    this.div = document.getElementById("sequences-div");
    this.status = createStatus();
    this.num_custom = 0;
    this.buttons = {};
    this.getSequences();
  }

  setupEventListeners() {
    document.getElementById("sequences-stopall").addEventListener("click", () => {
      fetch("/sequence/stopall");
    });
    socket.on("start_sequence", (data) => {
      console.log("Start Sequence", data);
      this.startSequence(data);
    });
    socket.on("stop_sequence", (data) => {
      console.log("Stop Sequence", data);
      this.stopSequence(data);
    });
  }

  getSequences() {
    fetch("/getsequences")
        .then((response) => response.json())
        .then((data) => {
          console.log("Recieved Sequences", data.sequences);
          for (let i = 0; i < data.sequences.length; i++) {
            this.createSequence(data.sequences[i]);
          }
          this.setupEventListeners();
        });
  }

  createSequence(data) {
    console.debug("Create", data);
    const row_num = this.num_custom;
    this.num_custom += 1;
    const name = data.name;
    const id = "sequences-" + row_num;
    const div = createSectionFlex();
    const title = createSecondTitle(`${id}-name`, name);
    const functions = createSectionFlexNoBorder();

    for (let i = 0; i < data.functions.length; i++) {
      const function_name = data.functions[i];
      const button = createButton(`sequences-function-${name}-${function_name}`, function_name);
      button.addEventListener("click", () => {
        const mode = document.getElementById(`${id}-mode`).value;
        const checked = document.getElementById(`${id}-infinite`).checked;
        let iterations = parseInt(document.getElementById(`${id}-iter`).value);
        if (isNaN(iterations)) {
          iterations = 1;
        }
        if (checked) {
          iterations = null;
        }
        this.send(mode, name, function_name, iterations);
      });
      this.buttons[name] = button;
      functions.appendChild(button);
    }

    const mode_title = createSecondTitle(null, "Mode");
    const mode_selector = createSelect(`${id}-mode`, ["start", "stop"], "start");
    const iter_title = createSecondTitle(null, "Iterations");
    const iter_selector = createNumber(`${id}-iter`, 1);
    const or_title = createSecondTitle(null, " OR ");
    const infinite_title = createSecondTitle(null, "Infinite: ");
    const infinite_selector = createCheckBox(`${id}-infinite`, false);
    iter_selector.className = "iter-selector";
    iter_selector.addEventListener("input", () => {
      if (iter_selector.value <= 0 && iter_selector.value != "") {
        iter_selector.value = 1;
      }
    });
    infinite_selector.addEventListener("click", () => {
      if (infinite_selector.checked) {
        iter_selector.disabled = true;
      } else {
        iter_selector.disabled = false;
      }
    });

    div.appendChild(title);
    div.appendChild(createDivider());
    div.appendChild(functions);
    div.appendChild(createDivider());
    div.appendChild(mode_title);
    div.appendChild(createSpaceS2());
    div.appendChild(mode_selector);
    div.appendChild(createVDivider());
    div.appendChild(iter_title);
    div.appendChild(createSpaceS2());
    div.appendChild(iter_selector);
    div.appendChild(createSpaceS2());
    div.appendChild(or_title);
    div.appendChild(createSpaceS2());
    div.appendChild(infinite_title);
    div.appendChild(createSpaceS2());
    div.appendChild(infinite_selector);
    this.div.appendChild(div);
    return;
  }

  send(mode, sequence_name, function_name, iterations = null) {
    console.log(`Sequence Send: ${sequence_name} with function ${function_name}`);
    let parameters = `sequence=${sequence_name}&function=${function_name}`;
    if (iterations != null) {
      parameters += `&iterations=${iterations}`;
    }
    console.log("Sedning Sequence", parameters);
    fetch(`/sequence/${mode}?${parameters}`);
  }

  startSequence(data) {
    const id = `sequences-function-${data.name}`;
    const button = document.getElementById(id);
    button.style.border = "0.1vw solid var(--highlight-color)";
  }

  stopSequence(data) {
    const id = `sequences-function-${data.name}`;
    const button = document.getElementById(id);
    button.style.border = "0.1vw solid var(--input-border)";
  }
}
