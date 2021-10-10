/* exported simpleColor simpleAnimation simpleSequence stopAllSequences */

const controllers_section = document.getElementById('expand-Controllers-section');
const brightness_section = document.getElementById('expand-Brightness-section');
const colors_section = document.getElementById('expand-Colors-section');
const animations_section = document.getElementById('expand-Animations-section');
const sequences_section = document.getElementById('expand-Sequences-section');
const other_section = document.getElementById('expand-Other-section');
const controllers_area = document.getElementById('expanded-controllers-area');
const brightness_area = document.getElementById('expanded-brightness-area');
const colors_area = document.getElementById('expanded-colors-area');
const animations_area = document.getElementById('expanded-animations-area');
const sequences_area = document.getElementById('expanded-sequences-area');
const other_area = document.getElementById('expanded-other-area');

controllers_section.addEventListener('click', () => {
  expandControllersSection();
});
brightness_section.addEventListener('click', () => {
  expandBrightnessSection();
  startSliderAnimations();
});
colors_section.addEventListener('click', () => {
  expandColorsSection();
});
animations_section.addEventListener('click', () => {
  expandAnimationsSection();
});
sequences_section.addEventListener('click', () => {
  expandSequencesSection();
});
other_section.addEventListener('click', () => {
  expandOtherSection();
});

document.getElementById('close-expanded-button').addEventListener('click', () => {
  showSections();
});

processQueryArgs();

function expandControllersSection() {
  hideSections();
  controllers_area.style.display = 'flex';
}

function expandBrightnessSection() {
  hideSections();
  brightness_area.style.display = 'flex';
}

function expandColorsSection() {
  hideSections();
  colors_area.style.display = 'flex';
}

function expandAnimationsSection() {
  hideSections();
  animations_area.style.display = 'flex';
}

function expandSequencesSection() {
  hideSections();
  sequences_area.style.display = 'flex';
}

function expandOtherSection() {
  hideSections();
  other_area.style.display = 'flex';
}

function processQueryArgs() {
  const urlParams = new URLSearchParams(window.location.search);
  const expanded = urlParams.get('expanded');
  switch (expanded) {
    case 'controllers':
      expandControllersSection();
      break;
    case 'brightness':
      expandBrightnessSection();
      break;
    case 'colors':
      expandColorsSection();
      break;
    case 'animations':
      expandAnimationsSection();
      break;
    case 'sequences':
      expandSequencesSection();
      break;
    case 'other':
      expandOtherSection();
      break;
  }
}

function hideSections() {
  const expanded_sections = document.getElementsByClassName('expanded-area');
  for (let i = 0; i < expanded_sections.length; i++) {
    expanded_sections[i].style.display = 'none';
  }
  document.documentElement.style.setProperty('--display-toggle-value', 'none');
  document.documentElement.style.setProperty('--expand-display-toggle-value', 'flex');
}

function showSections() {
  stopSliderAnimations();
  document.documentElement.style.setProperty('--display-toggle-value', 'flex');
  document.documentElement.style.setProperty('--expand-display-toggle-value', 'none');
}
