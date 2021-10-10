var key;
var Module = void 0 !== Module ? Module : {};
var moduleOverrides = {};
for (key in Module) Module.hasOwnProperty(key) && (moduleOverrides[key] = Module[key]);
var arguments_ = [];
var thisProgram = './this.program';
var quit_ = function (status, toThrow) {
  throw toThrow;
};
var ENVIRONMENT_IS_WEB = !1;
var ENVIRONMENT_IS_WORKER = !1;
var ENVIRONMENT_IS_NODE = !1;
var ENVIRONMENT_IS_SHELL = !1;
var ENVIRONMENT_IS_WEB = 'object' == typeof window;
var ENVIRONMENT_IS_WORKER = 'function' == typeof importScripts;
var ENVIRONMENT_IS_NODE =
  'object' == typeof process && 'object' == typeof process.versions && 'string' == typeof process.versions.node;
var ENVIRONMENT_IS_SHELL = !ENVIRONMENT_IS_WEB && !ENVIRONMENT_IS_NODE && !ENVIRONMENT_IS_WORKER;
if (Module.ENVIRONMENT) {
  throw new Error(
    'Module.ENVIRONMENT has been deprecated. To force the environment, use the ENVIRONMENT compile-time option (for example, -s ENVIRONMENT=web or -s ENVIRONMENT=node)'
  );
}
var read_;
var readAsync;
var readBinary;
var setWindowTitle;
var nodeFS;
var nodePath;
var scriptDirectory = '';
function locateFile(path) {
  return Module.locateFile ? Module.locateFile(path, scriptDirectory) : scriptDirectory + path;
}
if (ENVIRONMENT_IS_NODE) {
  (scriptDirectory = ENVIRONMENT_IS_WORKER ? require('path').dirname(scriptDirectory) + '/' : __dirname + '/'),
    (read_ = function (filename, binary) {
      return (
        (nodeFS = nodeFS || require('fs')),
        (filename = (nodePath = nodePath || require('path')).normalize(filename)),
        nodeFS.readFileSync(filename, binary ? null : 'utf8')
      );
    }),
    (readBinary = function (ret) {
      return (ret = read_(ret, !0)).buffer || (ret = new Uint8Array(ret)), assert(ret.buffer), ret;
    }),
    1 < process.argv.length && (thisProgram = process.argv[1].replace(/\\/g, '/')),
    (arguments_ = process.argv.slice(2)),
    'undefined' != typeof module && (module.exports = Module),
    process.on('uncaughtException', function (ex) {
      if (!(ex instanceof ExitStatus)) throw ex;
    }),
    process.on('unhandledRejection', abort),
    (quit_ = function (status) {
      process.exit(status);
    }),
    (Module.inspect = function () {
      return '[Emscripten Module object]';
    });
} else if (ENVIRONMENT_IS_SHELL) {
  'undefined' != typeof read &&
    (read_ = function (f) {
      return read(f);
    }),
    (readBinary = function (data) {
      return 'function' == typeof readbuffer
        ? new Uint8Array(readbuffer(data))
        : (assert('object' == typeof (data = read(data, 'binary'))), data);
    }),
    'undefined' != typeof scriptArgs
      ? (arguments_ = scriptArgs)
      : 'undefined' != typeof arguments && (arguments_ = arguments),
    'function' == typeof quit &&
      (quit_ = function (status) {
        quit(status);
      }),
    'undefined' != typeof print &&
      ('undefined' == typeof console && (console = {}),
      (console.log = print),
      (console.warn = console.error = 'undefined' != typeof printErr ? printErr : print));
} else {
  if (!ENVIRONMENT_IS_WEB && !ENVIRONMENT_IS_WORKER) throw new Error('environment detection error');
  ENVIRONMENT_IS_WORKER
    ? (scriptDirectory = self.location.href)
    : 'undefined' != typeof document && document.currentScript && (scriptDirectory = document.currentScript.src),
    (scriptDirectory =
      0 !== scriptDirectory.indexOf('blob:') ? scriptDirectory.substr(0, scriptDirectory.lastIndexOf('/') + 1) : ''),
    (read_ = function (url) {
      const xhr = new XMLHttpRequest();
      return xhr.open('GET', url, !1), xhr.send(null), xhr.responseText;
    }),
    ENVIRONMENT_IS_WORKER &&
      (readBinary = function (url) {
        const xhr = new XMLHttpRequest();
        return (
          xhr.open('GET', url, !1), (xhr.responseType = 'arraybuffer'), xhr.send(null), new Uint8Array(xhr.response)
        );
      }),
    (readAsync = function (url, onload, onerror) {
      const xhr = new XMLHttpRequest();
      xhr.open('GET', url, !0),
        (xhr.responseType = 'arraybuffer'),
        (xhr.onload = function () {
          200 == xhr.status || (0 == xhr.status && xhr.response) ? onload(xhr.response) : onerror();
        }),
        (xhr.onerror = onerror),
        xhr.send(null);
    }),
    (setWindowTitle = function (title) {
      document.title = title;
    });
}
var out = Module.print || console.log.bind(console);
var err = Module.printErr || console.warn.bind(console);
for (key in moduleOverrides) moduleOverrides.hasOwnProperty(key) && (Module[key] = moduleOverrides[key]);
(moduleOverrides = null),
  Module.arguments && (arguments_ = Module.arguments),
  Object.getOwnPropertyDescriptor(Module, 'arguments') ||
    Object.defineProperty(Module, 'arguments', {
      configurable: !0,
      get: function () {
        abort(
          'Module.arguments has been replaced with plain arguments_ (the initial value can be provided on Module, but after startup the value is only looked for on a local variable of that name)'
        );
      },
    }),
  Module.thisProgram && (thisProgram = Module.thisProgram),
  Object.getOwnPropertyDescriptor(Module, 'thisProgram') ||
    Object.defineProperty(Module, 'thisProgram', {
      configurable: !0,
      get: function () {
        abort(
          'Module.thisProgram has been replaced with plain thisProgram (the initial value can be provided on Module, but after startup the value is only looked for on a local variable of that name)'
        );
      },
    }),
  Module.quit && (quit_ = Module.quit),
  Object.getOwnPropertyDescriptor(Module, 'quit') ||
    Object.defineProperty(Module, 'quit', {
      configurable: !0,
      get: function () {
        abort(
          'Module.quit has been replaced with plain quit_ (the initial value can be provided on Module, but after startup the value is only looked for on a local variable of that name)'
        );
      },
    }),
  assert(
    void 0 === Module.memoryInitializerPrefixURL,
    'Module.memoryInitializerPrefixURL option was removed, use Module.locateFile instead'
  ),
  assert(
    void 0 === Module.pthreadMainPrefixURL,
    'Module.pthreadMainPrefixURL option was removed, use Module.locateFile instead'
  ),
  assert(
    void 0 === Module.cdInitializerPrefixURL,
    'Module.cdInitializerPrefixURL option was removed, use Module.locateFile instead'
  ),
  assert(
    void 0 === Module.filePackagePrefixURL,
    'Module.filePackagePrefixURL option was removed, use Module.locateFile instead'
  ),
  assert(void 0 === Module.read, 'Module.read option was removed (modify read_ in JS)'),
  assert(void 0 === Module.readAsync, 'Module.readAsync option was removed (modify readAsync in JS)'),
  assert(void 0 === Module.readBinary, 'Module.readBinary option was removed (modify readBinary in JS)'),
  assert(void 0 === Module.setWindowTitle, 'Module.setWindowTitle option was removed (modify setWindowTitle in JS)'),
  assert(void 0 === Module.TOTAL_MEMORY, 'Module.TOTAL_MEMORY has been renamed Module.INITIAL_MEMORY'),
  Object.getOwnPropertyDescriptor(Module, 'read') ||
    Object.defineProperty(Module, 'read', {
      configurable: !0,
      get: function () {
        abort(
          'Module.read has been replaced with plain read_ (the initial value can be provided on Module, but after startup the value is only looked for on a local variable of that name)'
        );
      },
    }),
  Object.getOwnPropertyDescriptor(Module, 'readAsync') ||
    Object.defineProperty(Module, 'readAsync', {
      configurable: !0,
      get: function () {
        abort(
          'Module.readAsync has been replaced with plain readAsync (the initial value can be provided on Module, but after startup the value is only looked for on a local variable of that name)'
        );
      },
    }),
  Object.getOwnPropertyDescriptor(Module, 'readBinary') ||
    Object.defineProperty(Module, 'readBinary', {
      configurable: !0,
      get: function () {
        abort(
          'Module.readBinary has been replaced with plain readBinary (the initial value can be provided on Module, but after startup the value is only looked for on a local variable of that name)'
        );
      },
    }),
  Object.getOwnPropertyDescriptor(Module, 'setWindowTitle') ||
    Object.defineProperty(Module, 'setWindowTitle', {
      configurable: !0,
      get: function () {
        abort(
          'Module.setWindowTitle has been replaced with plain setWindowTitle (the initial value can be provided on Module, but after startup the value is only looked for on a local variable of that name)'
        );
      },
    });
var STACK_ALIGN = 16;
function warnOnce(text) {
  warnOnce.shown || (warnOnce.shown = {}), warnOnce.shown[text] || ((warnOnce.shown[text] = 1), err(text));
}
function convertJsFunctionToWasm(func, sig) {
  if ('function' == typeof WebAssembly.Function) {
    for (
      var typeNames = { i: 'i32', j: 'i64', f: 'f32', d: 'f64' },
        type = { parameters: [], results: 'v' == sig[0] ? [] : [typeNames[sig[0]]] },
        i = 1;
      i < sig.length;
      ++i
    ) {
      type.parameters.push(typeNames[sig[i]]);
    }
    return new WebAssembly.Function(type, func);
  }
  let typeSection = [1, 0, 1, 96];
  let module = sig.slice(0, 1);
  const sigParam = sig.slice(1);
  const typeCodes = { i: 127, j: 126, f: 125, d: 124 };
  for (typeSection.push(sigParam.length), i = 0; i < sigParam.length; ++i) typeSection.push(typeCodes[sigParam[i]]);
  return (
    'v' == module ? typeSection.push(0) : (typeSection = typeSection.concat([1, typeCodes[module]])),
    (typeSection[1] = typeSection.length - 2),
    (module = new Uint8Array(
      [0, 97, 115, 109, 1, 0, 0, 0].concat(typeSection, [2, 7, 1, 1, 101, 1, 102, 0, 0, 7, 5, 1, 1, 102, 0, 0])
    )),
    (module = new WebAssembly.Module(module)),
    new WebAssembly.Instance(module, { e: { f: func } }).exports.f
  );
}
var functionsInTableMap;
var freeTableIndexes = [];
function getEmptyTableSlot() {
  if (freeTableIndexes.length) return freeTableIndexes.pop();
  try {
    wasmTable.grow(1);
  } catch (err) {
    if (!(err instanceof RangeError)) throw err;
    throw 'Unable to grow wasm table. Set ALLOW_TABLE_GROWTH.';
  }
  return wasmTable.length - 1;
}
function addFunctionWasm(func, wrapped) {
  if (!functionsInTableMap) {
    functionsInTableMap = new WeakMap();
    for (let i = 0; i < wasmTable.length; i++) {
      const item = wasmTable.get(i);
      item && functionsInTableMap.set(item, i);
    }
  }
  if (functionsInTableMap.has(func)) return functionsInTableMap.get(func);
  const ret = getEmptyTableSlot();
  try {
    wasmTable.set(ret, func);
  } catch (err) {
    if (!(err instanceof TypeError)) throw err;
    assert(void 0 !== wrapped, 'Missing signature argument to addFunction: ' + func),
      (wrapped = convertJsFunctionToWasm(func, wrapped)),
      wasmTable.set(ret, wrapped);
  }
  return functionsInTableMap.set(func, ret), ret;
}
var wasmBinary;
var noExitRuntime;
var wasmMemory;
var tempRet0 = 0;
function getValue(ptr, type, noSafe) {
  switch (('*' === (type = type || 'i8').charAt(type.length - 1) && (type = 'i32'), type)) {
    case 'i1':
    case 'i8':
      return HEAP8[ptr >> 0];
    case 'i16':
      return HEAP16[ptr >> 1];
    case 'i32':
    case 'i64':
      return HEAP32[ptr >> 2];
    case 'float':
      return HEAPF32[ptr >> 2];
    case 'double':
      return HEAPF64[ptr >> 3];
    default:
      abort('invalid type for getValue: ' + type);
  }
  return null;
}
Module.wasmBinary && (wasmBinary = Module.wasmBinary),
  Object.getOwnPropertyDescriptor(Module, 'wasmBinary') ||
    Object.defineProperty(Module, 'wasmBinary', {
      configurable: !0,
      get: function () {
        abort(
          'Module.wasmBinary has been replaced with plain wasmBinary (the initial value can be provided on Module, but after startup the value is only looked for on a local variable of that name)'
        );
      },
    }),
  Module.noExitRuntime && (noExitRuntime = Module.noExitRuntime),
  Object.getOwnPropertyDescriptor(Module, 'noExitRuntime') ||
    Object.defineProperty(Module, 'noExitRuntime', {
      configurable: !0,
      get: function () {
        abort(
          'Module.noExitRuntime has been replaced with plain noExitRuntime (the initial value can be provided on Module, but after startup the value is only looked for on a local variable of that name)'
        );
      },
    }),
  'object' != typeof WebAssembly && abort('no native wasm support detected');
var EXITSTATUS;
var ABORT = !1;
function assert(condition, text) {
  condition || abort('Assertion failed: ' + text);
}
function getCFunc(ident) {
  const func = Module['_' + ident];
  return assert(func, 'Cannot call unknown function ' + ident + ', make sure it is exported'), func;
}
function ccall(ret, returnType, argTypes, args, opts) {
  const toC = {
    string: function (str) {
      let len;
      let ret = 0;
      return (
        null != str && 0 !== str && ((len = 1 + (str.length << 2)), stringToUTF8(str, (ret = stackAlloc(len)), len)),
        ret
      );
    },
    array: function (arr) {
      const ret = stackAlloc(arr.length);
      return writeArrayToMemory(arr, ret), ret;
    },
  };
  var ret = getCFunc(ret);
  const cArgs = [];
  let stack = 0;
  if ((assert('array' !== returnType, 'Return type should not be "array".'), args)) {
    for (let i = 0; i < args.length; i++) {
      const converter = toC[argTypes[i]];
      converter ? (0 === stack && (stack = stackSave()), (cArgs[i] = converter(args[i]))) : (cArgs[i] = args[i]);
    }
  }
  return (
    (ret = (function (ret) {
      return 'string' === returnType ? UTF8ToString(ret) : 'boolean' === returnType ? Boolean(ret) : ret;
    })((ret = ret.apply(null, cArgs)))),
    0 !== stack && stackRestore(stack),
    ret
  );
}
var ALLOC_STACK = 1;
var UTF8Decoder = 'undefined' != typeof TextDecoder ? new TextDecoder('utf8') : void 0;
function UTF8ArrayToString(heap, idx, maxBytesToRead) {
  for (var endIdx = idx + maxBytesToRead, endPtr = idx; heap[endPtr] && !(endIdx <= endPtr); ) ++endPtr;
  if (16 < endPtr - idx && heap.subarray && UTF8Decoder) return UTF8Decoder.decode(heap.subarray(idx, endPtr));
  for (var str = ''; idx < endPtr; ) {
    var u1;
    var ch;
    let u0 = heap[idx++];
    128 & u0
      ? ((u1 = 63 & heap[idx++]),
        192 != (224 & u0)
          ? ((ch = 63 & heap[idx++]),
            (u0 =
              224 == (240 & u0)
                ? ((15 & u0) << 12) | (u1 << 6) | ch
                : (240 != (248 & u0) &&
                    warnOnce(
                      'Invalid UTF-8 leading byte 0x' +
                        u0.toString(16) +
                        ' encountered when deserializing a UTF-8 string on the asm.js/wasm heap to a JS string!'
                    ),
                  ((7 & u0) << 18) | (u1 << 12) | (ch << 6) | (63 & heap[idx++]))) < 65536
              ? (str += String.fromCharCode(u0))
              : ((ch = u0 - 65536), (str += String.fromCharCode(55296 | (ch >> 10), 56320 | (1023 & ch)))))
          : (str += String.fromCharCode(((31 & u0) << 6) | u1)))
      : (str += String.fromCharCode(u0));
  }
  return str;
}
function UTF8ToString(ptr, maxBytesToRead) {
  return ptr ? UTF8ArrayToString(HEAPU8, ptr, maxBytesToRead) : '';
}
function stringToUTF8Array(str, heap, outIdx, maxBytesToWrite) {
  if (!(0 < maxBytesToWrite)) return 0;
  for (var startIdx = outIdx, endIdx = outIdx + maxBytesToWrite - 1, i = 0; i < str.length; ++i) {
    let u = str.charCodeAt(i);
    if ((55296 <= u && u <= 57343 && (u = (65536 + ((1023 & u) << 10)) | (1023 & str.charCodeAt(++i))), u <= 127)) {
      if (endIdx <= outIdx) break;
      heap[outIdx++] = u;
    } else if (u <= 2047) {
      if (endIdx <= outIdx + 1) break;
      (heap[outIdx++] = 192 | (u >> 6)), (heap[outIdx++] = 128 | (63 & u));
    } else if (u <= 65535) {
      if (endIdx <= outIdx + 2) break;
      (heap[outIdx++] = 224 | (u >> 12)), (heap[outIdx++] = 128 | ((u >> 6) & 63)), (heap[outIdx++] = 128 | (63 & u));
    } else {
      if (endIdx <= outIdx + 3) break;
      2097152 <= u &&
        warnOnce(
          'Invalid Unicode code point 0x' +
            u.toString(16) +
            ' encountered when serializing a JS string to an UTF-8 string on the asm.js/wasm heap! (Valid unicode code points should be in range 0-0x1FFFFF).'
        ),
        (heap[outIdx++] = 240 | (u >> 18)),
        (heap[outIdx++] = 128 | ((u >> 12) & 63)),
        (heap[outIdx++] = 128 | ((u >> 6) & 63)),
        (heap[outIdx++] = 128 | (63 & u));
    }
  }
  return (heap[outIdx] = 0), outIdx - startIdx;
}
function stringToUTF8(str, outPtr, maxBytesToWrite) {
  return (
    assert(
      'number' == typeof maxBytesToWrite,
      'stringToUTF8(str, outPtr, maxBytesToWrite) is missing the third parameter that specifies the length of the output buffer!'
    ),
    stringToUTF8Array(str, HEAPU8, outPtr, maxBytesToWrite)
  );
}
function lengthBytesUTF8(str) {
  for (var len = 0, i = 0; i < str.length; ++i) {
    let u = str.charCodeAt(i);
    55296 <= u && u <= 57343 && (u = (65536 + ((1023 & u) << 10)) | (1023 & str.charCodeAt(++i))),
      u <= 127 ? ++len : (len += u <= 2047 ? 2 : u <= 65535 ? 3 : 4);
  }
  return len;
}
var buffer;
var HEAP8;
var HEAPU8;
var HEAP16;
var HEAPU16;
var HEAP32;
var HEAPU32;
var HEAPF32;
var HEAPF64;
var UTF16Decoder = 'undefined' != typeof TextDecoder ? new TextDecoder('utf-16le') : void 0;
function writeArrayToMemory(array, buffer) {
  assert(0 <= array.length, 'writeArrayToMemory array must have a length (should be an array or typed array)'),
    HEAP8.set(array, buffer);
}
function writeAsciiToMemory(str, buffer, dontAddNull) {
  for (let i = 0; i < str.length; ++i) {
    assert((str.charCodeAt(i) === str.charCodeAt(i)) & 255), (HEAP8[buffer++ >> 0] = str.charCodeAt(i));
  }
  dontAddNull || (HEAP8[buffer >> 0] = 0);
}
function updateGlobalBufferAndViews(buf) {
  (buffer = buf),
    (Module.HEAP8 = HEAP8 = new Int8Array(buf)),
    (Module.HEAP16 = HEAP16 = new Int16Array(buf)),
    (Module.HEAP32 = HEAP32 = new Int32Array(buf)),
    (Module.HEAPU8 = HEAPU8 = new Uint8Array(buf)),
    (Module.HEAPU16 = HEAPU16 = new Uint16Array(buf)),
    (Module.HEAPU32 = HEAPU32 = new Uint32Array(buf)),
    (Module.HEAPF32 = HEAPF32 = new Float32Array(buf)),
    (Module.HEAPF64 = HEAPF64 = new Float64Array(buf));
}
var TOTAL_STACK = 5242880;
Module.TOTAL_STACK &&
  assert(TOTAL_STACK === Module.TOTAL_STACK, 'the stack size can no longer be determined at runtime');
var wasmTable;
var INITIAL_MEMORY = Module.INITIAL_MEMORY || 16777216;
function writeStackCookie() {
  const max = _emscripten_stack_get_end();
  assert(0 == (3 & max)),
    (HEAPU32[1 + (max >> 2)] = 34821223),
    (HEAPU32[2 + (max >> 2)] = 2310721022),
    (HEAP32[0] = 1668509029);
}
function checkStackCookie() {
  let cookie1;
  let cookie2;
  ABORT ||
    ((cookie2 = _emscripten_stack_get_end()),
    (cookie1 = HEAPU32[1 + (cookie2 >> 2)]),
    (cookie2 = HEAPU32[2 + (cookie2 >> 2)]),
    (34821223 == cookie1 && 2310721022 == cookie2) ||
      abort(
        'Stack overflow! Stack cookie has been overwritten, expected hex dwords 0x89BACDFE and 0x2135467, but received 0x' +
          cookie2.toString(16) +
          ' ' +
          cookie1.toString(16)
      ),
    1668509029 !== HEAP32[0] &&
      abort('Runtime error: The application has corrupted its heap memory area (address zero)!'));
}
Object.getOwnPropertyDescriptor(Module, 'INITIAL_MEMORY') ||
  Object.defineProperty(Module, 'INITIAL_MEMORY', {
    configurable: !0,
    get: function () {
      abort(
        'Module.INITIAL_MEMORY has been replaced with plain INITIAL_MEMORY (the initial value can be provided on Module, but after startup the value is only looked for on a local variable of that name)'
      );
    },
  }),
  assert(
    TOTAL_STACK <= INITIAL_MEMORY,
    'INITIAL_MEMORY should be larger than TOTAL_STACK, was ' + INITIAL_MEMORY + '! (TOTAL_STACK=' + TOTAL_STACK + ')'
  ),
  assert(
    'undefined' != typeof Int32Array &&
      'undefined' != typeof Float64Array &&
      void 0 !== Int32Array.prototype.subarray &&
      void 0 !== Int32Array.prototype.set,
    'JS engine does not provide full typed array support'
  ),
  assert(!Module.wasmMemory, 'Use of `wasmMemory` detected.  Use -s IMPORTED_MEMORY to define wasmMemory externally'),
  assert(
    16777216 == INITIAL_MEMORY,
    'Detected runtime INITIAL_MEMORY setting.  Use -s IMPORTED_MEMORY to define wasmMemory dynamically'
  ),
  (function () {
    const h16 = new Int16Array(1);
    const h8 = new Int8Array(h16.buffer);
    if (((h16[0] = 25459), 115 !== h8[0] || 99 !== h8[1])) {
      throw 'Runtime error: expected the system to be little-endian!';
    }
  })();
var __ATPRERUN__ = [];
var __ATINIT__ = [];
var __ATMAIN__ = [];
var __ATPOSTRUN__ = [];
var runtimeInitialized = !1;
var runtimeExited = !1;
function preRun() {
  if (Module.preRun) {
    for ('function' == typeof Module.preRun && (Module.preRun = [Module.preRun]); Module.preRun.length; ) {
      addOnPreRun(Module.preRun.shift());
    }
  }
  callRuntimeCallbacks(__ATPRERUN__);
}
function initRuntime() {
  checkStackCookie(), assert(!runtimeInitialized), (runtimeInitialized = !0), callRuntimeCallbacks(__ATINIT__);
}
function preMain() {
  checkStackCookie(), callRuntimeCallbacks(__ATMAIN__);
}
function exitRuntime() {
  checkStackCookie(), (runtimeExited = !0);
}
function postRun() {
  if ((checkStackCookie(), Module.postRun)) {
    for ('function' == typeof Module.postRun && (Module.postRun = [Module.postRun]); Module.postRun.length; ) {
      addOnPostRun(Module.postRun.shift());
    }
  }
  callRuntimeCallbacks(__ATPOSTRUN__);
}
function addOnPreRun(cb) {
  __ATPRERUN__.unshift(cb);
}
function addOnPostRun(cb) {
  __ATPOSTRUN__.unshift(cb);
}
assert(
  Math.imul,
  'This browser does not support Math.imul(), build with LEGACY_VM_SUPPORT or POLYFILL_OLD_MATH_FUNCTIONS to add in a polyfill'
),
  assert(
    Math.fround,
    'This browser does not support Math.fround(), build with LEGACY_VM_SUPPORT or POLYFILL_OLD_MATH_FUNCTIONS to add in a polyfill'
  ),
  assert(
    Math.clz32,
    'This browser does not support Math.clz32(), build with LEGACY_VM_SUPPORT or POLYFILL_OLD_MATH_FUNCTIONS to add in a polyfill'
  ),
  assert(
    Math.trunc,
    'This browser does not support Math.trunc(), build with LEGACY_VM_SUPPORT or POLYFILL_OLD_MATH_FUNCTIONS to add in a polyfill'
  );
var runDependencies = 0;
var runDependencyWatcher = null;
var dependenciesFulfilled = null;
var runDependencyTracking = {};
function addRunDependency(id) {
  runDependencies++,
    Module.monitorRunDependencies && Module.monitorRunDependencies(runDependencies),
    id
      ? (assert(!runDependencyTracking[id]),
        (runDependencyTracking[id] = 1),
        null === runDependencyWatcher &&
          'undefined' != typeof setInterval &&
          (runDependencyWatcher = setInterval(function () {
            if (ABORT) return clearInterval(runDependencyWatcher), void (runDependencyWatcher = null);
            let dep;
            let shown = !1;
            for (dep in runDependencyTracking) {
              shown || ((shown = !0), err('still waiting on run dependencies:')), err('dependency: ' + dep);
            }
            shown && err('(end of list)');
          }, 1e4)))
      : err('warning: run dependency added without ID');
}
function removeRunDependency(callback) {
  runDependencies--,
    Module.monitorRunDependencies && Module.monitorRunDependencies(runDependencies),
    callback
      ? (assert(runDependencyTracking[callback]), delete runDependencyTracking[callback])
      : err('warning: run dependency removed without ID'),
    0 == runDependencies &&
      (null !== runDependencyWatcher && (clearInterval(runDependencyWatcher), (runDependencyWatcher = null)),
      dependenciesFulfilled && ((callback = dependenciesFulfilled), (dependenciesFulfilled = null), callback()));
}
function abort(what) {
  throw (
    (Module.onAbort && Module.onAbort(what),
    err((what += '')),
    (ABORT = !0),
    (EXITSTATUS = 1),
    (what = 'abort(' + what + ') at ' + stackTrace()),
    new WebAssembly.RuntimeError(what))
  );
}
(Module.preloadedImages = {}), (Module.preloadedAudios = {});
var FS = {
  error: function () {
    abort(
      'Filesystem support (FS) was not included. The problem is that you are using files from JS, but files were not used from C/C++, so filesystem support was not auto-included. You can force-include filesystem support with  -s FORCE_FILESYSTEM=1'
    );
  },
  init: function () {
    FS.error();
  },
  createDataFile: function () {
    FS.error();
  },
  createPreloadedFile: function () {
    FS.error();
  },
  createLazyFile: function () {
    FS.error();
  },
  open: function () {
    FS.error();
  },
  mkdev: function () {
    FS.error();
  },
  registerDevice: function () {
    FS.error();
  },
  analyzePath: function () {
    FS.error();
  },
  loadFilesFromDB: function () {
    FS.error();
  },
  ErrnoError: function () {
    FS.error();
  },
};
function hasPrefix(str, prefix) {
  return String.prototype.startsWith ? str.startsWith(prefix) : 0 === str.indexOf(prefix);
}
(Module.FS_createDataFile = FS.createDataFile), (Module.FS_createPreloadedFile = FS.createPreloadedFile);
var dataURIPrefix = 'data:application/octet-stream;base64,';
function isDataURI(filename) {
  return hasPrefix(filename, dataURIPrefix);
}
var fileURIPrefix = 'file://';
function isFileURI(filename) {
  return hasPrefix(filename, fileURIPrefix);
}
function createExportWrapper(name, fixedasm) {
  return function () {
    const displayName = name;
    let asm = fixedasm;
    return (
      fixedasm || (asm = Module.asm),
      assert(runtimeInitialized, 'native function `' + displayName + '` called before runtime initialization'),
      assert(
        !runtimeExited,
        'native function `' +
          displayName +
          '` called after runtime exit (use NO_EXIT_RUNTIME to keep it alive after main() exits)'
      ),
      asm[name] || assert(asm[name], 'exported native function `' + displayName + '` not found'),
      asm[name].apply(null, arguments)
    );
  };
}
var tempDouble;
var tempI64;
var wasmBinaryFile = 'pixels.wasm';
function getBinary() {
  try {
    if (wasmBinary) return new Uint8Array(wasmBinary);
    if (readBinary) return readBinary(wasmBinaryFile);
    throw 'both async and sync fetching of the wasm failed';
  } catch (err) {
    abort(err);
  }
}
function getBinaryPromise() {
  return wasmBinary ||
    (!ENVIRONMENT_IS_WEB && !ENVIRONMENT_IS_WORKER) ||
    'function' != typeof fetch ||
    isFileURI(wasmBinaryFile)
    ? Promise.resolve().then(getBinary)
    : fetch(wasmBinaryFile, { credentials: 'same-origin' })
        .then(function (response) {
          if (!response.ok) throw "failed to load wasm binary file at '" + wasmBinaryFile + "'";
          return response.arrayBuffer();
        })
        .catch(function () {
          return getBinary();
        });
}
function createWasm() {
  const info = { env: asmLibraryArg, wasi_snapshot_preview1: asmLibraryArg };
  function receiveInstance(exports, module) {
    (exports = exports.exports),
      (Module.asm = exports),
      assert((wasmMemory = Module.asm.memory), 'memory not found in wasm exports'),
      updateGlobalBufferAndViews(wasmMemory.buffer),
      assert((wasmTable = Module.asm.__indirect_function_table), 'table not found in wasm exports'),
      removeRunDependency('wasm-instantiate');
  }
  addRunDependency('wasm-instantiate');
  let trueModule = Module;
  function receiveInstantiatedSource(output) {
    assert(
      Module === trueModule,
      'the Module object should not be replaced during async compilation - perhaps the order of HTML elements is wrong?'
    ),
      (trueModule = null),
      receiveInstance(output.instance);
  }
  function instantiateArrayBuffer(receiver) {
    return getBinaryPromise()
      .then(function (binary) {
        return WebAssembly.instantiate(binary, info);
      })
      .then(receiver, function (reason) {
        err('failed to asynchronously prepare wasm: ' + reason), abort(reason);
      });
  }
  if (Module.instantiateWasm) {
    try {
      return Module.instantiateWasm(info, receiveInstance);
    } catch (e) {
      return err('Module.instantiateWasm callback failed with error: ' + e), !1;
    }
  }
  return (
    wasmBinary ||
    'function' != typeof WebAssembly.instantiateStreaming ||
    isDataURI(wasmBinaryFile) ||
    isFileURI(wasmBinaryFile) ||
    'function' != typeof fetch
      ? instantiateArrayBuffer(receiveInstantiatedSource)
      : fetch(wasmBinaryFile, { credentials: 'same-origin' }).then(function (response) {
          return WebAssembly.instantiateStreaming(response, info).then(receiveInstantiatedSource, function (reason) {
            return (
              err('wasm streaming compile failed: ' + reason),
              err('falling back to ArrayBuffer instantiation'),
              instantiateArrayBuffer(receiveInstantiatedSource)
            );
          });
        }),
    {}
  );
}
function callRuntimeCallbacks(callbacks) {
  for (; 0 < callbacks.length; ) {
    var func;
    const callback = callbacks.shift();
    'function' != typeof callback
      ? 'number' == typeof (func = callback.func)
        ? void 0 === callback.arg
          ? wasmTable.get(func)()
          : wasmTable.get(func)(callback.arg)
        : func(void 0 === callback.arg ? null : callback.arg)
      : callback(Module);
  }
}
function demangle(func) {
  return warnOnce('warning: build with  -s DEMANGLE_SUPPORT=1  to link in libcxxabi demangling'), func;
}
function demangleAll(text) {
  return text.replace(/\b_Z[\w\d_]+/g, function (x) {
    const y = demangle(x);
    return x === y ? x : y + ' [' + x + ']';
  });
}
function jsStackTrace() {
  let error = new Error();
  if (!error.stack) {
    try {
      throw new Error();
    } catch (e) {
      error = e;
    }
    if (!error.stack) return '(no stack trace available)';
  }
  return error.stack.toString();
}
function stackTrace() {
  let js = jsStackTrace();
  return Module.extraStackTrace && (js += '\n' + Module.extraStackTrace()), demangleAll(js);
}
function _abort() {
  abort();
}
function _emscripten_memcpy_big(dest, src, num) {
  HEAPU8.copyWithin(dest, src, src + num);
}
function abortOnCannotGrowMemory(requestedSize) {
  abort(
    'Cannot enlarge memory arrays to size ' +
      requestedSize +
      ' bytes (OOM). Either (1) compile with  -s INITIAL_MEMORY=X  with X higher than the current value ' +
      HEAP8.length +
      ', (2) compile with  -s ALLOW_MEMORY_GROWTH=1  which allows increasing the size at runtime, or (3) if you want malloc to return NULL (0) instead of this abort, compile with  -s ABORTING_MALLOC=0 '
  );
}
function _emscripten_resize_heap(requestedSize) {
  abortOnCannotGrowMemory((requestedSize >>>= 0));
}
isDataURI(wasmBinaryFile) || (wasmBinaryFile = locateFile(wasmBinaryFile));
var ASSERTIONS = !0;
__ATINIT__.push({
  func: function () {
    ___wasm_call_ctors();
  },
});
var calledRun;
var asmLibraryArg = {
  abort: _abort,
  emscripten_memcpy_big: _emscripten_memcpy_big,
  emscripten_resize_heap: _emscripten_resize_heap,
};
var asm = createWasm();
var ___wasm_call_ctors = (Module.___wasm_call_ctors = createExportWrapper('__wasm_call_ctors'));
var _maxLEDPerStrip = (Module._maxLEDPerStrip = createExportWrapper('maxLEDPerStrip'));
var _ledStripCount = (Module._ledStripCount = createExportWrapper('ledStripCount'));
var _List_new = (Module._List_new = createExportWrapper('List_new'));
var _List_get = (Module._List_get = createExportWrapper('List_get'));
var _List_set = (Module._List_set = createExportWrapper('List_set'));
var _List_size = (Module._List_size = createExportWrapper('List_size'));
var _List_setCounter = (Module._List_setCounter = createExportWrapper('List_setCounter'));
var _List_getCounter = (Module._List_getCounter = createExportWrapper('List_getCounter'));
var _Pixels_new = (Module._Pixels_new = createExportWrapper('Pixels_new'));
var _Pixels_size = (Module._Pixels_size = createExportWrapper('Pixels_size'));
var _Pixels_getBrightness = (Module._Pixels_getBrightness = createExportWrapper('Pixels_getBrightness'));
var _Pixels_setBrightness = (Module._Pixels_setBrightness = createExportWrapper('Pixels_setBrightness'));
var _Pixels_get = (Module._Pixels_get = createExportWrapper('Pixels_get'));
var _Pixels_increment = (Module._Pixels_increment = createExportWrapper('Pixels_increment'));
var _Pixels_animation = (Module._Pixels_animation = createExportWrapper('Pixels_animation'));
var _Pixels_getCurrentState = (Module._Pixels_getCurrentState = createExportWrapper('Pixels_getCurrentState'));
var _createAnimationArgs = (Module._createAnimationArgs = createExportWrapper('createAnimationArgs'));
var ___errno_location = (Module.___errno_location = createExportWrapper('__errno_location'));
var _fflush = (Module._fflush = createExportWrapper('fflush'));
var stackSave = (Module.stackSave = createExportWrapper('stackSave'));
var stackRestore = (Module.stackRestore = createExportWrapper('stackRestore'));
var stackAlloc = (Module.stackAlloc = createExportWrapper('stackAlloc'));
var _emscripten_stack_init = (Module._emscripten_stack_init = function () {
  return (_emscripten_stack_init = Module._emscripten_stack_init = Module.asm.emscripten_stack_init).apply(
    null,
    arguments
  );
});
var _emscripten_stack_get_free = (Module._emscripten_stack_get_free = function () {
  return (_emscripten_stack_get_free = Module._emscripten_stack_get_free = Module.asm.emscripten_stack_get_free).apply(
    null,
    arguments
  );
});
var _emscripten_stack_get_end = (Module._emscripten_stack_get_end = function () {
  return (_emscripten_stack_get_end = Module._emscripten_stack_get_end = Module.asm.emscripten_stack_get_end).apply(
    null,
    arguments
  );
});
function ExitStatus(status) {
  (this.name = 'ExitStatus'), (this.message = 'Program terminated with exit(' + status + ')'), (this.status = status);
}
function run(args) {
  function doRun() {
    calledRun ||
      ((calledRun = !0),
      (Module.calledRun = !0),
      ABORT ||
        (initRuntime(),
        preMain(),
        Module.onRuntimeInitialized && Module.onRuntimeInitialized(),
        assert(
          !Module._main,
          'compiled without a main, but one is present. if you added it from JS, use Module["onRuntimeInitialized"]'
        ),
        postRun()));
  }
  0 < runDependencies ||
    (_emscripten_stack_init(),
    writeStackCookie(),
    preRun(),
    0 < runDependencies ||
      (Module.setStatus
        ? (Module.setStatus('Running...'),
          setTimeout(function () {
            setTimeout(function () {
              Module.setStatus('');
            }, 1),
              doRun();
          }, 1))
        : doRun(),
      checkStackCookie()));
}
function checkUnflushedContent() {
  const oldOut = out;
  const oldErr = err;
  let has = !1;
  (out = err =
    function (x) {
      has = !0;
    }),
    (out = oldOut),
    (err = oldErr),
    has &&
      (warnOnce(
        'stdio streams had content in them that was not flushed. you should set EXIT_RUNTIME to 1 (see the FAQ), or make sure to emit a newline when you printf etc.'
      ),
      warnOnce(
        '(this may also be due to not including full filesystem support - try building with -s FORCE_FILESYSTEM=1)'
      ));
}
if (
  (Object.getOwnPropertyDescriptor(Module, 'intArrayFromString') ||
    (Module.intArrayFromString = function () {
      abort("'intArrayFromString' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
    }),
  Object.getOwnPropertyDescriptor(Module, 'intArrayToString') ||
    (Module.intArrayToString = function () {
      abort("'intArrayToString' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
    }),
  Object.getOwnPropertyDescriptor(Module, 'ccall') ||
    (Module.ccall = function () {
      abort("'ccall' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
    }),
  Object.getOwnPropertyDescriptor(Module, 'cwrap') ||
    (Module.cwrap = function () {
      abort("'cwrap' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
    }),
  Object.getOwnPropertyDescriptor(Module, 'setValue') ||
    (Module.setValue = function () {
      abort("'setValue' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
    }),
  (Module.getValue = getValue),
  Object.getOwnPropertyDescriptor(Module, 'allocate') ||
    (Module.allocate = function () {
      abort("'allocate' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
    }),
  Object.getOwnPropertyDescriptor(Module, 'UTF8ArrayToString') ||
    (Module.UTF8ArrayToString = function () {
      abort("'UTF8ArrayToString' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
    }),
  Object.getOwnPropertyDescriptor(Module, 'UTF8ToString') ||
    (Module.UTF8ToString = function () {
      abort("'UTF8ToString' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
    }),
  Object.getOwnPropertyDescriptor(Module, 'stringToUTF8Array') ||
    (Module.stringToUTF8Array = function () {
      abort("'stringToUTF8Array' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
    }),
  Object.getOwnPropertyDescriptor(Module, 'stringToUTF8') ||
    (Module.stringToUTF8 = function () {
      abort("'stringToUTF8' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
    }),
  Object.getOwnPropertyDescriptor(Module, 'lengthBytesUTF8') ||
    (Module.lengthBytesUTF8 = function () {
      abort("'lengthBytesUTF8' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
    }),
  Object.getOwnPropertyDescriptor(Module, 'stackTrace') ||
    (Module.stackTrace = function () {
      abort("'stackTrace' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
    }),
  Object.getOwnPropertyDescriptor(Module, 'addOnPreRun') ||
    (Module.addOnPreRun = function () {
      abort("'addOnPreRun' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
    }),
  Object.getOwnPropertyDescriptor(Module, 'addOnInit') ||
    (Module.addOnInit = function () {
      abort("'addOnInit' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
    }),
  Object.getOwnPropertyDescriptor(Module, 'addOnPreMain') ||
    (Module.addOnPreMain = function () {
      abort("'addOnPreMain' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
    }),
  Object.getOwnPropertyDescriptor(Module, 'addOnExit') ||
    (Module.addOnExit = function () {
      abort("'addOnExit' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
    }),
  Object.getOwnPropertyDescriptor(Module, 'addOnPostRun') ||
    (Module.addOnPostRun = function () {
      abort("'addOnPostRun' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
    }),
  Object.getOwnPropertyDescriptor(Module, 'writeStringToMemory') ||
    (Module.writeStringToMemory = function () {
      abort("'writeStringToMemory' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
    }),
  Object.getOwnPropertyDescriptor(Module, 'writeArrayToMemory') ||
    (Module.writeArrayToMemory = function () {
      abort("'writeArrayToMemory' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
    }),
  Object.getOwnPropertyDescriptor(Module, 'writeAsciiToMemory') ||
    (Module.writeAsciiToMemory = function () {
      abort("'writeAsciiToMemory' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
    }),
  Object.getOwnPropertyDescriptor(Module, 'addRunDependency') ||
    (Module.addRunDependency = function () {
      abort(
        "'addRunDependency' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ). Alternatively, forcing filesystem support (-s FORCE_FILESYSTEM=1) can export this for you"
      );
    }),
  Object.getOwnPropertyDescriptor(Module, 'removeRunDependency') ||
    (Module.removeRunDependency = function () {
      abort(
        "'removeRunDependency' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ). Alternatively, forcing filesystem support (-s FORCE_FILESYSTEM=1) can export this for you"
      );
    }),
  Object.getOwnPropertyDescriptor(Module, 'FS_createFolder') ||
    (Module.FS_createFolder = function () {
      abort("'FS_createFolder' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
    }),
  Object.getOwnPropertyDescriptor(Module, 'FS_createPath') ||
    (Module.FS_createPath = function () {
      abort(
        "'FS_createPath' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ). Alternatively, forcing filesystem support (-s FORCE_FILESYSTEM=1) can export this for you"
      );
    }),
  Object.getOwnPropertyDescriptor(Module, 'FS_createDataFile') ||
    (Module.FS_createDataFile = function () {
      abort(
        "'FS_createDataFile' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ). Alternatively, forcing filesystem support (-s FORCE_FILESYSTEM=1) can export this for you"
      );
    }),
  Object.getOwnPropertyDescriptor(Module, 'FS_createPreloadedFile') ||
    (Module.FS_createPreloadedFile = function () {
      abort(
        "'FS_createPreloadedFile' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ). Alternatively, forcing filesystem support (-s FORCE_FILESYSTEM=1) can export this for you"
      );
    }),
  Object.getOwnPropertyDescriptor(Module, 'FS_createLazyFile') ||
    (Module.FS_createLazyFile = function () {
      abort(
        "'FS_createLazyFile' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ). Alternatively, forcing filesystem support (-s FORCE_FILESYSTEM=1) can export this for you"
      );
    }),
  Object.getOwnPropertyDescriptor(Module, 'FS_createLink') ||
    (Module.FS_createLink = function () {
      abort("'FS_createLink' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
    }),
  Object.getOwnPropertyDescriptor(Module, 'FS_createDevice') ||
    (Module.FS_createDevice = function () {
      abort(
        "'FS_createDevice' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ). Alternatively, forcing filesystem support (-s FORCE_FILESYSTEM=1) can export this for you"
      );
    }),
  Object.getOwnPropertyDescriptor(Module, 'FS_unlink') ||
    (Module.FS_unlink = function () {
      abort(
        "'FS_unlink' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ). Alternatively, forcing filesystem support (-s FORCE_FILESYSTEM=1) can export this for you"
      );
    }),
  Object.getOwnPropertyDescriptor(Module, 'getLEB') ||
    (Module.getLEB = function () {
      abort("'getLEB' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
    }),
  Object.getOwnPropertyDescriptor(Module, 'getFunctionTables') ||
    (Module.getFunctionTables = function () {
      abort("'getFunctionTables' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
    }),
  Object.getOwnPropertyDescriptor(Module, 'alignFunctionTables') ||
    (Module.alignFunctionTables = function () {
      abort("'alignFunctionTables' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
    }),
  Object.getOwnPropertyDescriptor(Module, 'registerFunctions') ||
    (Module.registerFunctions = function () {
      abort("'registerFunctions' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
    }),
  Object.getOwnPropertyDescriptor(Module, 'addFunction') ||
    (Module.addFunction = function () {
      abort("'addFunction' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
    }),
  Object.getOwnPropertyDescriptor(Module, 'removeFunction') ||
    (Module.removeFunction = function () {
      abort("'removeFunction' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
    }),
  Object.getOwnPropertyDescriptor(Module, 'getFuncWrapper') ||
    (Module.getFuncWrapper = function () {
      abort("'getFuncWrapper' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
    }),
  Object.getOwnPropertyDescriptor(Module, 'prettyPrint') ||
    (Module.prettyPrint = function () {
      abort("'prettyPrint' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
    }),
  Object.getOwnPropertyDescriptor(Module, 'makeBigInt') ||
    (Module.makeBigInt = function () {
      abort("'makeBigInt' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
    }),
  Object.getOwnPropertyDescriptor(Module, 'dynCall') ||
    (Module.dynCall = function () {
      abort("'dynCall' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
    }),
  Object.getOwnPropertyDescriptor(Module, 'getCompilerSetting') ||
    (Module.getCompilerSetting = function () {
      abort("'getCompilerSetting' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
    }),
  Object.getOwnPropertyDescriptor(Module, 'print') ||
    (Module.print = function () {
      abort("'print' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
    }),
  Object.getOwnPropertyDescriptor(Module, 'printErr') ||
    (Module.printErr = function () {
      abort("'printErr' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
    }),
  Object.getOwnPropertyDescriptor(Module, 'getTempRet0') ||
    (Module.getTempRet0 = function () {
      abort("'getTempRet0' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
    }),
  Object.getOwnPropertyDescriptor(Module, 'setTempRet0') ||
    (Module.setTempRet0 = function () {
      abort("'setTempRet0' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
    }),
  Object.getOwnPropertyDescriptor(Module, 'callMain') ||
    (Module.callMain = function () {
      abort("'callMain' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
    }),
  Object.getOwnPropertyDescriptor(Module, 'abort') ||
    (Module.abort = function () {
      abort("'abort' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
    }),
  Object.getOwnPropertyDescriptor(Module, 'stringToNewUTF8') ||
    (Module.stringToNewUTF8 = function () {
      abort("'stringToNewUTF8' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
    }),
  Object.getOwnPropertyDescriptor(Module, 'setFileTime') ||
    (Module.setFileTime = function () {
      abort("'setFileTime' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
    }),
  Object.getOwnPropertyDescriptor(Module, 'abortOnCannotGrowMemory') ||
    (Module.abortOnCannotGrowMemory = function () {
      abort("'abortOnCannotGrowMemory' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
    }),
  Object.getOwnPropertyDescriptor(Module, 'emscripten_realloc_buffer') ||
    (Module.emscripten_realloc_buffer = function () {
      abort("'emscripten_realloc_buffer' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
    }),
  Object.getOwnPropertyDescriptor(Module, 'ENV') ||
    (Module.ENV = function () {
      abort("'ENV' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
    }),
  Object.getOwnPropertyDescriptor(Module, 'ERRNO_CODES') ||
    (Module.ERRNO_CODES = function () {
      abort("'ERRNO_CODES' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
    }),
  Object.getOwnPropertyDescriptor(Module, 'ERRNO_MESSAGES') ||
    (Module.ERRNO_MESSAGES = function () {
      abort("'ERRNO_MESSAGES' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
    }),
  Object.getOwnPropertyDescriptor(Module, 'setErrNo') ||
    (Module.setErrNo = function () {
      abort("'setErrNo' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
    }),
  Object.getOwnPropertyDescriptor(Module, 'DNS') ||
    (Module.DNS = function () {
      abort("'DNS' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
    }),
  Object.getOwnPropertyDescriptor(Module, 'getHostByName') ||
    (Module.getHostByName = function () {
      abort("'getHostByName' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
    }),
  Object.getOwnPropertyDescriptor(Module, 'GAI_ERRNO_MESSAGES') ||
    (Module.GAI_ERRNO_MESSAGES = function () {
      abort("'GAI_ERRNO_MESSAGES' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
    }),
  Object.getOwnPropertyDescriptor(Module, 'Protocols') ||
    (Module.Protocols = function () {
      abort("'Protocols' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
    }),
  Object.getOwnPropertyDescriptor(Module, 'Sockets') ||
    (Module.Sockets = function () {
      abort("'Sockets' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
    }),
  Object.getOwnPropertyDescriptor(Module, 'getRandomDevice') ||
    (Module.getRandomDevice = function () {
      abort("'getRandomDevice' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
    }),
  Object.getOwnPropertyDescriptor(Module, 'traverseStack') ||
    (Module.traverseStack = function () {
      abort("'traverseStack' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
    }),
  Object.getOwnPropertyDescriptor(Module, 'UNWIND_CACHE') ||
    (Module.UNWIND_CACHE = function () {
      abort("'UNWIND_CACHE' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
    }),
  Object.getOwnPropertyDescriptor(Module, 'withBuiltinMalloc') ||
    (Module.withBuiltinMalloc = function () {
      abort("'withBuiltinMalloc' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
    }),
  Object.getOwnPropertyDescriptor(Module, 'readAsmConstArgsArray') ||
    (Module.readAsmConstArgsArray = function () {
      abort("'readAsmConstArgsArray' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
    }),
  Object.getOwnPropertyDescriptor(Module, 'readAsmConstArgs') ||
    (Module.readAsmConstArgs = function () {
      abort("'readAsmConstArgs' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
    }),
  Object.getOwnPropertyDescriptor(Module, 'mainThreadEM_ASM') ||
    (Module.mainThreadEM_ASM = function () {
      abort("'mainThreadEM_ASM' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
    }),
  Object.getOwnPropertyDescriptor(Module, 'jstoi_q') ||
    (Module.jstoi_q = function () {
      abort("'jstoi_q' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
    }),
  Object.getOwnPropertyDescriptor(Module, 'jstoi_s') ||
    (Module.jstoi_s = function () {
      abort("'jstoi_s' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
    }),
  Object.getOwnPropertyDescriptor(Module, 'getExecutableName') ||
    (Module.getExecutableName = function () {
      abort("'getExecutableName' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
    }),
  Object.getOwnPropertyDescriptor(Module, 'listenOnce') ||
    (Module.listenOnce = function () {
      abort("'listenOnce' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
    }),
  Object.getOwnPropertyDescriptor(Module, 'autoResumeAudioContext') ||
    (Module.autoResumeAudioContext = function () {
      abort("'autoResumeAudioContext' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
    }),
  Object.getOwnPropertyDescriptor(Module, 'dynCallLegacy') ||
    (Module.dynCallLegacy = function () {
      abort("'dynCallLegacy' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
    }),
  Object.getOwnPropertyDescriptor(Module, 'getDynCaller') ||
    (Module.getDynCaller = function () {
      abort("'getDynCaller' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
    }),
  Object.getOwnPropertyDescriptor(Module, 'dynCall') ||
    (Module.dynCall = function () {
      abort("'dynCall' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
    }),
  Object.getOwnPropertyDescriptor(Module, 'callRuntimeCallbacks') ||
    (Module.callRuntimeCallbacks = function () {
      abort("'callRuntimeCallbacks' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
    }),
  Object.getOwnPropertyDescriptor(Module, 'abortStackOverflow') ||
    (Module.abortStackOverflow = function () {
      abort("'abortStackOverflow' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
    }),
  Object.getOwnPropertyDescriptor(Module, 'reallyNegative') ||
    (Module.reallyNegative = function () {
      abort("'reallyNegative' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
    }),
  Object.getOwnPropertyDescriptor(Module, 'unSign') ||
    (Module.unSign = function () {
      abort("'unSign' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
    }),
  Object.getOwnPropertyDescriptor(Module, 'reSign') ||
    (Module.reSign = function () {
      abort("'reSign' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
    }),
  Object.getOwnPropertyDescriptor(Module, 'formatString') ||
    (Module.formatString = function () {
      abort("'formatString' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
    }),
  Object.getOwnPropertyDescriptor(Module, 'PATH') ||
    (Module.PATH = function () {
      abort("'PATH' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
    }),
  Object.getOwnPropertyDescriptor(Module, 'PATH_FS') ||
    (Module.PATH_FS = function () {
      abort("'PATH_FS' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
    }),
  Object.getOwnPropertyDescriptor(Module, 'SYSCALLS') ||
    (Module.SYSCALLS = function () {
      abort("'SYSCALLS' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
    }),
  Object.getOwnPropertyDescriptor(Module, 'syscallMmap2') ||
    (Module.syscallMmap2 = function () {
      abort("'syscallMmap2' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
    }),
  Object.getOwnPropertyDescriptor(Module, 'syscallMunmap') ||
    (Module.syscallMunmap = function () {
      abort("'syscallMunmap' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
    }),
  Object.getOwnPropertyDescriptor(Module, 'JSEvents') ||
    (Module.JSEvents = function () {
      abort("'JSEvents' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
    }),
  Object.getOwnPropertyDescriptor(Module, 'specialHTMLTargets') ||
    (Module.specialHTMLTargets = function () {
      abort("'specialHTMLTargets' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
    }),
  Object.getOwnPropertyDescriptor(Module, 'maybeCStringToJsString') ||
    (Module.maybeCStringToJsString = function () {
      abort("'maybeCStringToJsString' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
    }),
  Object.getOwnPropertyDescriptor(Module, 'findEventTarget') ||
    (Module.findEventTarget = function () {
      abort("'findEventTarget' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
    }),
  Object.getOwnPropertyDescriptor(Module, 'findCanvasEventTarget') ||
    (Module.findCanvasEventTarget = function () {
      abort("'findCanvasEventTarget' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
    }),
  Object.getOwnPropertyDescriptor(Module, 'polyfillSetImmediate') ||
    (Module.polyfillSetImmediate = function () {
      abort("'polyfillSetImmediate' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
    }),
  Object.getOwnPropertyDescriptor(Module, 'demangle') ||
    (Module.demangle = function () {
      abort("'demangle' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
    }),
  Object.getOwnPropertyDescriptor(Module, 'demangleAll') ||
    (Module.demangleAll = function () {
      abort("'demangleAll' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
    }),
  Object.getOwnPropertyDescriptor(Module, 'jsStackTrace') ||
    (Module.jsStackTrace = function () {
      abort("'jsStackTrace' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
    }),
  Object.getOwnPropertyDescriptor(Module, 'stackTrace') ||
    (Module.stackTrace = function () {
      abort("'stackTrace' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
    }),
  Object.getOwnPropertyDescriptor(Module, 'getEnvStrings') ||
    (Module.getEnvStrings = function () {
      abort("'getEnvStrings' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
    }),
  Object.getOwnPropertyDescriptor(Module, 'checkWasiClock') ||
    (Module.checkWasiClock = function () {
      abort("'checkWasiClock' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
    }),
  Object.getOwnPropertyDescriptor(Module, 'flush_NO_FILESYSTEM') ||
    (Module.flush_NO_FILESYSTEM = function () {
      abort("'flush_NO_FILESYSTEM' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
    }),
  Object.getOwnPropertyDescriptor(Module, 'writeI53ToI64') ||
    (Module.writeI53ToI64 = function () {
      abort("'writeI53ToI64' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
    }),
  Object.getOwnPropertyDescriptor(Module, 'writeI53ToI64Clamped') ||
    (Module.writeI53ToI64Clamped = function () {
      abort("'writeI53ToI64Clamped' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
    }),
  Object.getOwnPropertyDescriptor(Module, 'writeI53ToI64Signaling') ||
    (Module.writeI53ToI64Signaling = function () {
      abort("'writeI53ToI64Signaling' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
    }),
  Object.getOwnPropertyDescriptor(Module, 'writeI53ToU64Clamped') ||
    (Module.writeI53ToU64Clamped = function () {
      abort("'writeI53ToU64Clamped' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
    }),
  Object.getOwnPropertyDescriptor(Module, 'writeI53ToU64Signaling') ||
    (Module.writeI53ToU64Signaling = function () {
      abort("'writeI53ToU64Signaling' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
    }),
  Object.getOwnPropertyDescriptor(Module, 'readI53FromI64') ||
    (Module.readI53FromI64 = function () {
      abort("'readI53FromI64' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
    }),
  Object.getOwnPropertyDescriptor(Module, 'readI53FromU64') ||
    (Module.readI53FromU64 = function () {
      abort("'readI53FromU64' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
    }),
  Object.getOwnPropertyDescriptor(Module, 'convertI32PairToI53') ||
    (Module.convertI32PairToI53 = function () {
      abort("'convertI32PairToI53' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
    }),
  Object.getOwnPropertyDescriptor(Module, 'convertU32PairToI53') ||
    (Module.convertU32PairToI53 = function () {
      abort("'convertU32PairToI53' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
    }),
  Object.getOwnPropertyDescriptor(Module, 'uncaughtExceptionCount') ||
    (Module.uncaughtExceptionCount = function () {
      abort("'uncaughtExceptionCount' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
    }),
  Object.getOwnPropertyDescriptor(Module, 'exceptionLast') ||
    (Module.exceptionLast = function () {
      abort("'exceptionLast' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
    }),
  Object.getOwnPropertyDescriptor(Module, 'exceptionCaught') ||
    (Module.exceptionCaught = function () {
      abort("'exceptionCaught' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
    }),
  Object.getOwnPropertyDescriptor(Module, 'ExceptionInfoAttrs') ||
    (Module.ExceptionInfoAttrs = function () {
      abort("'ExceptionInfoAttrs' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
    }),
  Object.getOwnPropertyDescriptor(Module, 'ExceptionInfo') ||
    (Module.ExceptionInfo = function () {
      abort("'ExceptionInfo' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
    }),
  Object.getOwnPropertyDescriptor(Module, 'CatchInfo') ||
    (Module.CatchInfo = function () {
      abort("'CatchInfo' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
    }),
  Object.getOwnPropertyDescriptor(Module, 'exception_addRef') ||
    (Module.exception_addRef = function () {
      abort("'exception_addRef' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
    }),
  Object.getOwnPropertyDescriptor(Module, 'exception_decRef') ||
    (Module.exception_decRef = function () {
      abort("'exception_decRef' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
    }),
  Object.getOwnPropertyDescriptor(Module, 'Browser') ||
    (Module.Browser = function () {
      abort("'Browser' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
    }),
  Object.getOwnPropertyDescriptor(Module, 'funcWrappers') ||
    (Module.funcWrappers = function () {
      abort("'funcWrappers' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
    }),
  Object.getOwnPropertyDescriptor(Module, 'getFuncWrapper') ||
    (Module.getFuncWrapper = function () {
      abort("'getFuncWrapper' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
    }),
  Object.getOwnPropertyDescriptor(Module, 'setMainLoop') ||
    (Module.setMainLoop = function () {
      abort("'setMainLoop' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
    }),
  Object.getOwnPropertyDescriptor(Module, 'FS') ||
    (Module.FS = function () {
      abort("'FS' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
    }),
  Object.getOwnPropertyDescriptor(Module, 'mmapAlloc') ||
    (Module.mmapAlloc = function () {
      abort("'mmapAlloc' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
    }),
  Object.getOwnPropertyDescriptor(Module, 'MEMFS') ||
    (Module.MEMFS = function () {
      abort("'MEMFS' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
    }),
  Object.getOwnPropertyDescriptor(Module, 'TTY') ||
    (Module.TTY = function () {
      abort("'TTY' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
    }),
  Object.getOwnPropertyDescriptor(Module, 'PIPEFS') ||
    (Module.PIPEFS = function () {
      abort("'PIPEFS' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
    }),
  Object.getOwnPropertyDescriptor(Module, 'SOCKFS') ||
    (Module.SOCKFS = function () {
      abort("'SOCKFS' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
    }),
  Object.getOwnPropertyDescriptor(Module, 'tempFixedLengthArray') ||
    (Module.tempFixedLengthArray = function () {
      abort("'tempFixedLengthArray' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
    }),
  Object.getOwnPropertyDescriptor(Module, 'miniTempWebGLFloatBuffers') ||
    (Module.miniTempWebGLFloatBuffers = function () {
      abort("'miniTempWebGLFloatBuffers' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
    }),
  Object.getOwnPropertyDescriptor(Module, 'heapObjectForWebGLType') ||
    (Module.heapObjectForWebGLType = function () {
      abort("'heapObjectForWebGLType' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
    }),
  Object.getOwnPropertyDescriptor(Module, 'heapAccessShiftForWebGLHeap') ||
    (Module.heapAccessShiftForWebGLHeap = function () {
      abort("'heapAccessShiftForWebGLHeap' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
    }),
  Object.getOwnPropertyDescriptor(Module, 'GL') ||
    (Module.GL = function () {
      abort("'GL' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
    }),
  Object.getOwnPropertyDescriptor(Module, 'emscriptenWebGLGet') ||
    (Module.emscriptenWebGLGet = function () {
      abort("'emscriptenWebGLGet' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
    }),
  Object.getOwnPropertyDescriptor(Module, 'computeUnpackAlignedImageSize') ||
    (Module.computeUnpackAlignedImageSize = function () {
      abort("'computeUnpackAlignedImageSize' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
    }),
  Object.getOwnPropertyDescriptor(Module, 'emscriptenWebGLGetTexPixelData') ||
    (Module.emscriptenWebGLGetTexPixelData = function () {
      abort(
        "'emscriptenWebGLGetTexPixelData' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)"
      );
    }),
  Object.getOwnPropertyDescriptor(Module, 'emscriptenWebGLGetUniform') ||
    (Module.emscriptenWebGLGetUniform = function () {
      abort("'emscriptenWebGLGetUniform' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
    }),
  Object.getOwnPropertyDescriptor(Module, 'emscriptenWebGLGetVertexAttrib') ||
    (Module.emscriptenWebGLGetVertexAttrib = function () {
      abort(
        "'emscriptenWebGLGetVertexAttrib' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)"
      );
    }),
  Object.getOwnPropertyDescriptor(Module, 'writeGLArray') ||
    (Module.writeGLArray = function () {
      abort("'writeGLArray' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
    }),
  Object.getOwnPropertyDescriptor(Module, 'AL') ||
    (Module.AL = function () {
      abort("'AL' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
    }),
  Object.getOwnPropertyDescriptor(Module, 'SDL_unicode') ||
    (Module.SDL_unicode = function () {
      abort("'SDL_unicode' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
    }),
  Object.getOwnPropertyDescriptor(Module, 'SDL_ttfContext') ||
    (Module.SDL_ttfContext = function () {
      abort("'SDL_ttfContext' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
    }),
  Object.getOwnPropertyDescriptor(Module, 'SDL_audio') ||
    (Module.SDL_audio = function () {
      abort("'SDL_audio' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
    }),
  Object.getOwnPropertyDescriptor(Module, 'SDL') ||
    (Module.SDL = function () {
      abort("'SDL' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
    }),
  Object.getOwnPropertyDescriptor(Module, 'SDL_gfx') ||
    (Module.SDL_gfx = function () {
      abort("'SDL_gfx' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
    }),
  Object.getOwnPropertyDescriptor(Module, 'GLUT') ||
    (Module.GLUT = function () {
      abort("'GLUT' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
    }),
  Object.getOwnPropertyDescriptor(Module, 'EGL') ||
    (Module.EGL = function () {
      abort("'EGL' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
    }),
  Object.getOwnPropertyDescriptor(Module, 'GLFW_Window') ||
    (Module.GLFW_Window = function () {
      abort("'GLFW_Window' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
    }),
  Object.getOwnPropertyDescriptor(Module, 'GLFW') ||
    (Module.GLFW = function () {
      abort("'GLFW' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
    }),
  Object.getOwnPropertyDescriptor(Module, 'GLEW') ||
    (Module.GLEW = function () {
      abort("'GLEW' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
    }),
  Object.getOwnPropertyDescriptor(Module, 'IDBStore') ||
    (Module.IDBStore = function () {
      abort("'IDBStore' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
    }),
  Object.getOwnPropertyDescriptor(Module, 'runAndAbortIfError') ||
    (Module.runAndAbortIfError = function () {
      abort("'runAndAbortIfError' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
    }),
  Object.getOwnPropertyDescriptor(Module, 'warnOnce') ||
    (Module.warnOnce = function () {
      abort("'warnOnce' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
    }),
  Object.getOwnPropertyDescriptor(Module, 'stackSave') ||
    (Module.stackSave = function () {
      abort("'stackSave' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
    }),
  Object.getOwnPropertyDescriptor(Module, 'stackRestore') ||
    (Module.stackRestore = function () {
      abort("'stackRestore' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
    }),
  Object.getOwnPropertyDescriptor(Module, 'stackAlloc') ||
    (Module.stackAlloc = function () {
      abort("'stackAlloc' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
    }),
  Object.getOwnPropertyDescriptor(Module, 'AsciiToString') ||
    (Module.AsciiToString = function () {
      abort("'AsciiToString' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
    }),
  Object.getOwnPropertyDescriptor(Module, 'stringToAscii') ||
    (Module.stringToAscii = function () {
      abort("'stringToAscii' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
    }),
  Object.getOwnPropertyDescriptor(Module, 'UTF16ToString') ||
    (Module.UTF16ToString = function () {
      abort("'UTF16ToString' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
    }),
  Object.getOwnPropertyDescriptor(Module, 'stringToUTF16') ||
    (Module.stringToUTF16 = function () {
      abort("'stringToUTF16' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
    }),
  Object.getOwnPropertyDescriptor(Module, 'lengthBytesUTF16') ||
    (Module.lengthBytesUTF16 = function () {
      abort("'lengthBytesUTF16' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
    }),
  Object.getOwnPropertyDescriptor(Module, 'UTF32ToString') ||
    (Module.UTF32ToString = function () {
      abort("'UTF32ToString' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
    }),
  Object.getOwnPropertyDescriptor(Module, 'stringToUTF32') ||
    (Module.stringToUTF32 = function () {
      abort("'stringToUTF32' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
    }),
  Object.getOwnPropertyDescriptor(Module, 'lengthBytesUTF32') ||
    (Module.lengthBytesUTF32 = function () {
      abort("'lengthBytesUTF32' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
    }),
  Object.getOwnPropertyDescriptor(Module, 'allocateUTF8') ||
    (Module.allocateUTF8 = function () {
      abort("'allocateUTF8' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
    }),
  Object.getOwnPropertyDescriptor(Module, 'allocateUTF8OnStack') ||
    (Module.allocateUTF8OnStack = function () {
      abort("'allocateUTF8OnStack' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
    }),
  (Module.writeStackCookie = writeStackCookie),
  (Module.checkStackCookie = checkStackCookie),
  Object.getOwnPropertyDescriptor(Module, 'ALLOC_NORMAL') ||
    Object.defineProperty(Module, 'ALLOC_NORMAL', {
      configurable: !0,
      get: function () {
        abort("'ALLOC_NORMAL' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
      },
    }),
  Object.getOwnPropertyDescriptor(Module, 'ALLOC_STACK') ||
    Object.defineProperty(Module, 'ALLOC_STACK', {
      configurable: !0,
      get: function () {
        abort("'ALLOC_STACK' was not exported. add it to EXTRA_EXPORTED_RUNTIME_METHODS (see the FAQ)");
      },
    }),
  (dependenciesFulfilled = function runCaller() {
    calledRun || run(), calledRun || (dependenciesFulfilled = runCaller);
  }),
  (Module.run = run),
  Module.preInit)
) {
  for ('function' == typeof Module.preInit && (Module.preInit = [Module.preInit]); 0 < Module.preInit.length; ) {
    Module.preInit.pop()();
  }
}
(noExitRuntime = !0), run();
