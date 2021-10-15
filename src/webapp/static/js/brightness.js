/* globals BufferedCall ledInfo */
/* exported startSliderAnimations stopSliderAnimations handleLEDInfo */

const ledinfo_send = new BufferedCall((values) => {
  console.log(values);
  ledInfo(values);
}, 50);

const expanded_brightness_slider = document.getElementById('expanded-brightness-slider');
const frame_ms_slider = document.getElementById('frame-ms-brightness-slider');
const frame_multiplier_slider = document.getElementById('frame-multiplier-brightness-slider');

const expanded_brightness_text = document.getElementById('expanded-brightness-value');
const frame_ms_text = document.getElementById('frame-ms-value');
const frame_multiplier_text = document.getElementById('frame-multiplier-value');
const animation_fps_text = document.getElementById('animation-fps-value');

expanded_brightness_slider.addEventListener('input', () => {
  updateValueText();
  ledinfo_send.add({brightness: expanded_brightness_slider.value});
});

frame_ms_slider.addEventListener('input', () => {
  updateValueText();
  ledinfo_send.add({frame_ms: getScaledFrameMs()});
});

frame_multiplier_slider.addEventListener('input', () => {
  updateValueText();
  ledinfo_send.add({frame_multiplier: frame_multiplier_slider.value});
});

const FRAME_MS_SCALING = [
  {upto: 0, amount: 0, base: 0},
  {upto: 180, amount: 1, base: 20}, // 20 < frame_ms < 200
  {upto: 190, amount: 5, base: 200}, // 200 < frame_ms < 250
  {upto: 215, amount: 10, base: 250}, // 250 < frame_ms < 500
  {upto: 240, amount: 20, base: 500}, // 500 < frame_ms < 1000
  {upto: 260, amount: 50, base: 1000}, // 1000 < frame_ms < 2000
  {upto: 290, amount: 100, base: 2000}, // 2000 < frame_ms < 5000
  {upto: 315, amount: 1000, base: 5000}, // 5000 < frame_ms < 10000
  {upto: 325, amount: 5000, base: 30000}, // 30000 < frame_ms < 60000
];

function getScaledFrameMs() {
  const value = frame_ms_slider.value;
  for (let i = 0; i < FRAME_MS_SCALING.length; i++) {
    if (value < FRAME_MS_SCALING[i].upto) {
      return FRAME_MS_SCALING[i].base + (value - FRAME_MS_SCALING[i - 1].upto) * FRAME_MS_SCALING[i].amount;
    }
  }
  return 60000;
}

function updateValueText() {
  const brightness = expanded_brightness_slider.value;
  const frame_ms = getScaledFrameMs();
  const frame_multiplier = frame_multiplier_slider.value;
  const animation_fps = (1000 / frame_ms) * frame_multiplier;
  expanded_brightness_text.textContent = brightness;
  frame_ms_text.textContent = frame_ms;
  frame_multiplier_text.textContent = frame_multiplier;
  let decimal_places = 0;
  if (animation_fps < 10) {
    decimal_places = 3;
  }
  frame_ms_diff = ((224 - frame_ms_slider.value) / 224) * 15;
  frame_multiplier_diff = (frame_multiplier / 20) * 15;
  animation_fps_text.textContent = animation_fps.toFixed(decimal_places);
  rcss.setProperty('--expanded-brightness-percent', `${Math.floor((brightness / 255) * 100)}%`);
}

function handleLEDInfo(values) {
  if ('frame_ms' in values) {
    // frame_ms_slider.value = values['frame_ms'];
  }
}

let frame_ms_base = 0;
let frame_multiplier_base = 0;
let frame_ms_diff = 1;
let frame_multiplier_diff = 1;
let frame_ms_animation = null;

function startSliderAnimations() {
  frame_ms_animation = setInterval(() => {
    rcss.setProperty('--frame-ms-base', `${frame_ms_base % 120}px`);
    rcss.setProperty('--frame-multiplier-base', `${frame_multiplier_base % 120}px`);
    frame_ms_base += frame_ms_diff;
    frame_multiplier_base += frame_multiplier_diff;
  }, 40);
}

function stopSliderAnimations() {
  if (frame_ms_animation) {
    clearInterval(frame_ms_animation);
  }
}

updateValueText();
