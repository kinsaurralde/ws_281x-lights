let a;

WebAssembly.instantiateStreaming(fetch("../static/square.wasm"), {
  main: {
    sayHello() {
      console.log("Hello from WebAssembly!");
    }
  },
  env: {
    abort(_msg, _file, line, column) {
      console.error("abort called at main.ts:" + line + ":" + column);
    }
  },
}).then(result => {
  const exports = result.instance.exports;
  a = exports;
  // document.getElementById("container").textContent = "Result: " + exports.add(19, 23);
}).catch(console.error);