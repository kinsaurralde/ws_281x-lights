/* exported PixelStrip */

class PixelStrip {
  constructor(div, name, length) {
    this.div = div;
    this.name = name;
    this.length = length;
    this.div = div;
    this.table;
    this.pixels = [];
    this.createDiv();
    console.log(`Created pixel strip ${this.name} of length ${this.length}`);
  }

  createDiv() {
    const id = `pixel-strip-${this.name}`;
    const title = createSecondTitle(`${id}-title-name`, this.name);
    const length =
        createSecondTitle(`${id}-title-length`, `${this.length} pixels`);

    for (let i = 0; i < this.length; i++) {
      this.pixels.push(new Pixel(i));
    }
    this.createPixelTable(30);

    title.classList.add('width-10');
    length.classList.add('width-10');
    this.div.appendChild(title);
    this.div.appendChild(createVDivider());
    this.div.appendChild(length);
    this.div.appendChild(createDivider());
    this.div.appendChild(this.table);
  }

  resizeTable(width) {
    this.table.remove();
    this.createPixelTable(width);
    this.div.appendChild(this.table);
  }

  createPixelTable(width) {
    const height = Math.ceil(this.pixels.length / width);
    this.table = document.createElement('table');
    this.table.className = 'pixel-table';
    for (let i = 0; i < height; i++) {
      const row = this.table.insertRow();
      for (let j = 0; j < width; j++) {
        const pixel_id = i * width + j;
        if (pixel_id < this.pixels.length) {
          const cell = row.insertCell();
          cell.appendChild(this.pixels[pixel_id].get());
        }
      }
    }
  }
}

class Pixel {
  constructor(id) {
    this.id = id;
    this.r = 0;
    this.g = 0;
    this.b = 0;
    this.div = this.createDiv();
    this.refresh();
  }

  createDiv() {
    const div = document.createElement('div');
    div.className = 'display-pixel';
    return div;
  }

  set(r, g, b) {
    this.r = r;
    this.g = g;
    this.b = b;
    this.refresh();
  }

  refresh() {
    this.div.style.backgroundColor = `rgb(${this.r}, ${this.g}, ${this.b})`;
  }

  get() {
    return this.div;
  }
}
