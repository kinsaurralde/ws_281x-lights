/* globals addColorTiles */
/* exported loadPWALayout send */

const main_brightness_slider = document.getElementById('main-brightness-slider');
main_brightness_slider.addEventListener('input', () => {
  ledInfo({brightness: main_brightness_slider.value});
});

function loadPWALayout() {
  fetch('/pwalayout')
      .then((response) => response.json())
      .then((layout) => {
        addColorTiles(layout['colors']);
        global_animations.addAnimationArgs(layout['animation_args']);
        global_animations.addAnimations(layout['animations']);
      });
  fetch('/controllers')
      .then((response) => response.json())
      .then((controllers) => {
        console.log('Controllers', controllers);
        window.global_controllers.addControllers(controllers['controllers']);
      });
}

function ledInfo(values) {
  values['controllers'] = ['all'];
  socket.emit('ledinfo', values);
}

function send(payload) {
  console.log('Sending', payload);
  socket.emit('animation', payload);
}
