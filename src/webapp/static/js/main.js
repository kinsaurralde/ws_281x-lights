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
        console.debug('PWA Layout', layout);
        addColorTiles(layout['colors']);
        global_animations.addAnimationArgs(layout['animation_args']);
        global_animations.addAnimations(layout['animations']);
      });
  fetch('/controllers')
      .then((response) => response.json())
      .then((controllers) => {
        console.debug('Controllers', controllers);
        global_controllers.addControllers(controllers['controllers']);
      });
}

function ledInfo(values) {
  values['controllers'] = global_controllers.getSelectedControllers();
  console.debug('LED Info:', values);
  socket.emit('ledinfo', values);
}

function send(payload) {
  console.debug('Sending', payload);
  socket.emit('animation', payload);
}
