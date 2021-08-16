//let colors = ["#24d05a", "#eb4888", "#10a2f5", "#e9bc3f"];
// massdrop
//let colors = ["teal", "pink", "blue", "flesh"];
//let colors = ["#64B9B0", "#EC6F86", "#344652", "#EEA5A8"];

// Safyi real estate
//let colors = ["red", "d blue", "teal", "yellow"];
//let colors = ["#FF4756", "#161849", "#317585", "#FFB600"];

// camera lens
//let colors = ["blue", "yellow", "rosa", "gray"];
let colors = ["#0099DC", "#FFA500", "#FF446B", "#4A4A4D"];

(function() {
  setModeEventListener();
  setRandomLinkColor();
  //setColorHoverListener();
  setBioEventListener();
  /*setRandomPhoto();*/

/*
  setInterval(() => {
    setRandomPhoto();
  }, 2500);

  setInterval(() => {
    setRandomLinkColor();
  }, 5000);
  */
})();

/* Dark Mode */
function setModeEventListener() {
  let list = document.body.classList;
  document.getElementById("toggler").addEventListener("change", event => {
    event.target.checked ? list.add("dark-mode") : list.remove("dark-mode");
  });
}

/* Colors */

function getRandomColor() {
  return colors[Math.floor(Math.random() * colors.length)];
}

function setRandomLinkColor() {
  Array.from(document.getElementsByTagName("a")).forEach(e => {
    e.style.color = getRandomColor();
  });
  Array.from(document.getElementsByClassName("rnd-bkg-color")).forEach(e => {
    e.style.background = getRandomColor();
  });
}

function setColorHoverListener() {
  Array.from(document.querySelectorAll("a, button")).forEach(e => {
    e.addEventListener("mouseover", setRandomLinkColor);
  });
}

/* Photos */

function setRandomPhoto() {
  let num = Math.floor(Math.random() * 14) + 1;
  document.getElementById(
    "propic"
  ).src = `https://cassidoo.co/img/face${num}.jpg`;
}

/* Bio Toggles */

function setBioEventListener() {
  Array.from(document.getElementsByTagName("button")).forEach(e => {
    e.addEventListener("click", bioToggle);
  });
}

function bioToggle(e) {
  let bioType = e.target;
  let color = getRandomColor();
  off(bioType);
  bioType.style.cssText = `border-color: ${color}; color: ${color}; font-weight: bold;`;
  let bioTypeElement = document.getElementsByClassName(bioType.id)[0];
  if (bioTypeElement !== undefined) bioTypeElement.classList.add("show");
}

function off(bioType) {
  Array.from(document.getElementsByTagName("button")).forEach(butt => {
    butt.style.borderColor = "#96979c";
    butt.style.color = "#96979c";
  });
  Array.from(document.getElementsByClassName("bio")).forEach(e => {
    e.classList.remove("show");
  });
}