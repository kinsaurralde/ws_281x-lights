/* exported Groups */

class Groups {
  constructor() {
    this.table = document.getElementById("groups-table");
    this.num_strips = 0;
    this.num_groups = 0;
    this.names = [];
  }

  init(names) {
    this.names = names;
    this.num_strips = names.length;
    const row = this.table.insertRow();
    const row2 = this.table.insertRow();
    let cell = row.insertCell();
    let cell2 = row2.insertCell();
    cell.textContent = "Target Group ID";
    cell2.textContent = "-1";
    for (let i = 0; i < this.num_strips; i++) {
      cell = row.insertCell();
      cell.textContent = this.names[i];
      cell2 = row2.insertCell();
      cell2.textContent = "✓";
    }
    this.addRow();
  }

  addRow() {
    const row = this.table.insertRow();
    const id = createSecondTitle(null, this.num_strips + this.num_groups);
    const cell = row.insertCell();
    cell.appendChild(id);
    const group_id = this.num_groups + this.num_strips;
    for (let i = 0; i < this.num_strips; i++) {
      const cell = row.insertCell();
      cell.appendChild(createCheckBox("target-group-" + group_id + "-" + this.names[i], true));
    }
    this.num_groups += 1;
  }

  getStripsFromGroup(group_id) {
    if (group_id == -1) {
      return this.names;
    }
    if (group_id >= this.num_strips + this.num_groups || group_id < 0) {
      return [];
    }
    if (group_id < this.num_strips) {
      return [this.names[group_id]];
    }
    const strips = [];
    for (let i = 0; i < this.num_strips; i++) {
      const id = "target-group-" + group_id + "-" + this.names[i];
      if (document.getElementById(id).checked) {
        strips.push(this.names[i]);
      }
    }
    return strips;
  }
}
