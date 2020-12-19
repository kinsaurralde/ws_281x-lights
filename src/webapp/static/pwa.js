/* exported simpleColor simpleAnimation */

function createAnimationArgs() {
  return {
    'animation': 0,
    'color': 0,
    'color_bg': 0,
    'colors': [],
    'arg1': 0,
    'arg2': 0,
    'arg3': 0,
    'arg4': 0,
    'arg5': 0,
    'arg6': false,
    'arg7': false,
    'arg8': false,
    'wait_ms': 40,
    'inc_steps': 1,
    'id': 'a',
  };
}

function send(payload) {
  console.log('Sending', payload);
  fetch('/data', {method: 'post', body: JSON.stringify(payload)});
}

function simpleColor(r, g, b) {
  const payload = [createAnimationArgs()];
  payload[0].color = combineRGB(r, g, b);
  send(payload);
}

function simpleAnimation(args) {
  console.log('SIMPLE', args);
  const payload = createAnimationArgs();
  for (const arg of Object.keys(args)) {
    console.log('A', arg, arg in payload);
    if (arg in payload) {
      payload[arg] = args[arg];
    }
  }
  send([payload]);
}
