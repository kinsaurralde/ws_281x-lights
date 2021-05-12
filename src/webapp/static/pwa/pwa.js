/* exported simpleColor simpleAnimation simpleSequence stopAllSequences */

const controllers_section = document.getElementById("expand-controllers-section")
const brightness_section = document.getElementById("expand-brightness-section")
const colors_section = document.getElementById("expand-colors-section")
const animations_section = document.getElementById("expand-animations-section")
const sequences_section = document.getElementById("expand-sequences-section")
const other_section = document.getElementById("expand-other-section")

controllers_section.addEventListener("click", () => {
  expandControllersSection()
})
brightness_section.addEventListener("click", () => {
  expandBrightnessSection()
})
colors_section.addEventListener("click", () => {
  expandColorsSection()
})
animations_section.addEventListener("click", () => {
  expandAnimationsSection()
})
sequences_section.addEventListener("click", () => {
  expandSequencesSection()
})
other_section.addEventListener("click", () => {
  expandOtherSection()
})

document.getElementById("close-expanded-button").addEventListener("click", () => {
  showSections()
})

function expandControllersSection() {
  hideSections()
  controllers_section.style.display = "flex"
}

function expandBrightnessSection() {
  hideSections()
  brightness_section.style.display = "flex"
}

function expandColorsSection() {
  hideSections()
  colors_section.style.display = "flex"
}

function expandAnimationsSection() {
  hideSections()
  animations_section.style.display = "flex"
}

function expandSequencesSection() {
  hideSections()
  sequences_section.style.display = "flex"
}

function expandOtherSection() {
  hideSections()
  other_section.style.display = "flex"
}

function createAnimationArgs() {
  return {
    animation: 0,
    color: 0,
    color_bg: 0,
    colors: [],
    arg1: 0,
    arg2: 0,
    arg3: 0,
    arg4: 0,
    arg5: 0,
    arg6: false,
    arg7: false,
    arg8: false,
    wait_ms: 40,
    inc_steps: 1,
    id: "a",
  }
}

function send(payload) {
  console.log("Sending", payload)
  fetch("/data", { method: "post", body: JSON.stringify(payload) })
}

function simpleColor(r, g, b) {
  const payload = [createAnimationArgs()]
  payload[0].color = combineRGB(r, g, b)
  send(payload)
}

function simpleAnimation(args) {
  const payload = createAnimationArgs()
  for (const arg of Object.keys(args)) {
    if (arg in payload) {
      payload[arg] = args[arg]
    }
  }
  send([payload])
}

function simpleSequence(sequence_name, function_name) {
  fetch(`/sequence/start?sequence=${sequence_name}&function=${function_name}`)
}

function stopAllSequences() {
  fetch("/sequence/stopall")
}

function hideSections() {
  const expanded_sections = document.getElementsByClassName("expanded-area")
  for (let i = 0; i < expanded_sections.length; i++) {
    expanded_sections[i].style.display = "none"
  }
  document.documentElement.style.setProperty("--display-toggle-value", "none")
  document.documentElement.style.setProperty("--expand-display-toggle-value", "flex")
}

function showSections() {
  document.documentElement.style.setProperty("--display-toggle-value", "flex")
  document.documentElement.style.setProperty("--expand-display-toggle-value", "none")
}
