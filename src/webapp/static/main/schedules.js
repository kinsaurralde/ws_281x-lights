/* exported Schedules */

class Schedules {
  constructor() {
    this.div = document.getElementById("scheduler-div");
    this.num_custom = 0;
    this.buttons = {};
    this.getSchedules();
  }

  setupEventListeners() {
    socket.on("active_schedules", (data) => {
      this.setActiveSchedules(data);
    });
  }

  getSchedules() {
    fetch("/getschedules")
        .then((response) => response.json())
        .then((data) => {
          console.log("Recieved Schedules", data.schedules);
          for (let i = 0; i < data.schedules.length; i++) {
            this.createSchedule(data.schedules[i]);
          }
          this.setupEventListeners();
        });
  }

  createSchedule(data) {
    console.debug("Create", data);
    const row_num = this.num_custom;
    this.num_custom += 1;
    const name = data.name;
    const id = "scheduler-" + row_num;
    const div = createSectionFlex();
    const title = createSecondTitle(`${id}-name`, name);
    const functions = createSectionFlexNoBorder();

    for (let i = 0; i < data.functions.length; i++) {
      const function_name = data.functions[i];
      const button = createButton(`schedule-function-${name}-${function_name}`, function_name);
      button.addEventListener("click", () => {
        const mode = document.getElementById(`${id}-mode`).value;
        this.send(mode, name, function_name);
      });
      this.buttons[`${name}-${function_name}`] = button;
      functions.appendChild(button);
    }

    const mode_title = createSecondTitle(null, "Mode");
    const mode_selector = createSelect(`${id}-mode`, ["start", "stop"], "start");

    div.appendChild(title);
    div.appendChild(createDivider());
    div.appendChild(functions);
    div.appendChild(createDivider());
    div.appendChild(mode_title);
    div.appendChild(createSpaceS2());
    div.appendChild(mode_selector);
    this.div.appendChild(div);
    return;
  }

  send(mode, schedule_name, function_name) {
    console.log(`Schedule Send: ${schedule_name} with function ${function_name}`);
    const parameters = `schedule=${schedule_name}&function=${function_name}`;
    console.log(`Sending Schedule: /schedule/${mode}?${parameters}`);
    fetch(`/schedule/${mode}?${parameters}`);
  }

  setActiveSchedules(data) {
    for (const key of Object.keys(this.buttons)) {
      this.buttons[key].style.border = "0.1vw solid var(--input-border)";
    }
    for (const key of Object.keys(data)) {
      for (let i = 0; i < data[key].length; i++) {
        const name = `${key}-${data[key][i]}`;
        const id = `schedule-function-${name}`;
        const button = document.getElementById(id);
        button.style.border = "0.1vw solid var(--highlight-color)";
      }
    }
  }

  startSchedule(name) {
    const id = `schedule-function-${name}`;
    const button = document.getElementById(id);
    button.style.border = "0.1vw solid var(--highlight-color)";
  }

  stopSchedule(name) {
    const id = `schedule-function-${name}`;
    const button = document.getElementById(id);
    button.style.border = "0.1vw solid var(--input-border)";
  }
}
