/* exported addColorTiles addAnimationTiles */
/* globals simpleColor */

function addColorTiles(colors) {
  const color_tile_div = document.getElementById('Colors-container');
  for (const color in colors) {
    if (colors.hasOwnProperty(color)) {
      const value = colors[color]['value'];
      global_colors.addColorRGB(color, value[0], value[1], value[2]);
      if (!colors[color].tile) {
        continue;
      }
      color_tile_div.appendChild(generateColorTile(value));
    }
  }
}

function generateColorTile(color) {
  const div = document.createElement('div');
  div.className = 'mobile-color-box';
  const r = color[0];
  const g = color[1];
  const b = color[2];
  div.style.backgroundColor = `rgb(${r}, ${g}, ${b})`;
  div.addEventListener('click', () => {
    simpleColor(r, g, b);
  });
  return div;
}
