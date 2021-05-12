/* globals simpleColor */

const BUFFERED_WAIT_MS = 20;

const rcss = document.documentElement.style;

const color_display = document.getElementById("expanded-color-display");
const color_text = document.getElementById("expanded-color-text");
const color_live = document.getElementById("expanded-color-live");
const color_send_text = document.getElementById("expanded-color-send-text");

const r_slider = document.getElementById("expanded-color-r-slider");
const g_slider = document.getElementById("expanded-color-g-slider");
const b_slider = document.getElementById("expanded-color-b-slider");

const current_color = {
  r: 0,
  g: 0,
  b: 0,
};
let buffer_waiting = false;

setStartColor();
updateLiveCheck();

color_live.addEventListener("input", () => {
  updateLiveCheck();
});

color_display.addEventListener("click", () => {
  simpleColor(current_color.r, current_color.g, current_color.b);
});

r_slider.addEventListener("input", () => {
  const value = parseInt(r_slider.value);
  if (value >= 0 && value <= 255) {
    current_color.r = value;
  }
  updateColor();
});

g_slider.addEventListener("input", () => {
  const value = parseInt(g_slider.value);
  if (value >= 0 && value <= 255) {
    current_color.g = value;
  }
  updateColor();
});

b_slider.addEventListener("input", () => {
  const value = parseInt(b_slider.value);
  if (value >= 0 && value <= 255) {
    current_color.b = value;
  }
  updateColor();
});

function updateLiveCheck() {
  if (color_live.checked) {
    color_send_text.style.display = "none";
  } else {
    color_send_text.style.display = "block";
  }
}

function bufferedColor(r, g, b) {
  if (!buffer_waiting) {
    buffer_waiting = true;
    console.log("Start buffer");
    setTimeout(function () {
      simpleColor(r, g, b);
      buffer_waiting = false;
    }, BUFFERED_WAIT_MS);
  } else {
    console.log("Buffer already started");
  }
}

function updateColor(nosend = false) {
  const r = current_color.r;
  const g = current_color.g;
  const b = current_color.b;
  const color_rgb_text = `${r}, ${g}, ${b}`;
  const color_css = `rgb(${color_rgb_text})`;
  const color_css_invert = `rgb(${255 - r}, ${255 - g}, ${255 - b})`;
  if (color_live.checked && !nosend) {
    bufferedColor(r, g, b);
  }
  color_text.textContent = color_rgb_text;
  rcss.setProperty("--expanded-color-value", color_css);
  rcss.setProperty("--expanded-color-value-inverted", color_css_invert);
  rcss.setProperty("--expanded-color-r-percent", `${Math.floor((r / 255) * 100)}%`);
  rcss.setProperty("--expanded-color-g-percent", `${Math.floor((g / 255) * 100)}%`);
  rcss.setProperty("--expanded-color-b-percent", `${Math.floor((b / 255) * 100)}%`);
}

function getRandomInt(min, max) {
  return min + Math.floor(Math.random() * (max - min));
}

function setStartColor() {
  const ignore = getRandomInt(0, 3);
  let r_value = getRandomInt(100, 256);
  let g_value = getRandomInt(100, 256);
  let b_value = getRandomInt(100, 256);
  switch (ignore) {
    case 0:
      r_value = 0;
      break;
    case 1:
      g_value = 0;
      break;
    case 2:
      b_value = 0;
  }
  current_color.r = r_value;
  current_color.g = g_value;
  current_color.b = b_value;
  r_slider.value = r_value;
  g_slider.value = g_value;
  b_slider.value = b_value;
  updateColor(true);
}
