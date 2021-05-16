/* globals socket */

const controllers_container = document.getElementById("controllers-container");

class Controllers {
  constructor() {
    this.num_controllers = 0;
    this.controllers = {};
    socket.on("update", (data) => {
      this.handleUpdate(data);
    });
    this.fetchControllers();
  }

  handleUpdate(data) {
    console.debug("Update", data);
    if ("ping" in data) {
      this.updatePing(data.ping);
    }
  }

  fetchControllers() {
    fetch("/getcontrollers")
      .then((response) => response.json())
      .then((controllers) => {
        console.log("Recieved Controllers", controllers);
        const keys = Object.keys(controllers);
        this.num_controllers = Object.keys(controllers).length;
        this.controllers = {};
        for (let i = 0; i < this.num_controllers; i++) {
          this.controllers[keys[i]] = new Controller(controllers[keys[i]]);
        }
      });
  }

  updatePing(data) {
    for (const controller in data) {
      if (controller in this.controllers) {
        this.controllers[controller].updatePing(data[controller]);
      }
    }
  }
}

class Controller {
  constructor(data) {
    console.log("Create", data);
    this.active = true;
    this.name = data["name"];
    this.num_leds = data["init"]["num_leds"];
    this.brightness = data["init"]["brightness"];
    this.box = document.createElement("button");
    this.box.id = `controller-box-${this.name}`;
    this.box.className = "mobile-button-box";
    this.box.addEventListener("click", () => {
      this.active = !this.active;
      this.updateActive();
    });
    this.updateActive();
    this.updatePing("---");
    controllers_container.appendChild(this.box);
  }

  updatePing(ping) {
    if (ping == null || ping == undefined) {
      this.box.innerText = `${this.name}\nERROR`;
      this.box.style.color = "red";
    } else if (ping == false) {
      this.box.innerText = `${this.name}\nDISABLED`;
      this.box.style.color = "red";
      this.active = false;
      this.updateActive();
    } else {
      this.box.innerText = `${this.name}\n${ping} ms`;
      this.box.style.color = "green";
    }
  }

  updateActive() {
    if (this.active) {
      this.box.style.borderColor = "yellow";
    } else {
      this.box.style.borderColor = "var(--input-border-color)";
    }
  }

  isActive() {
    return this.active;
  }
}
