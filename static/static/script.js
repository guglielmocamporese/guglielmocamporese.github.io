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
let rgb_colors = ["rgb(0, 153, 220)", "rgb(255, 165, 0)", "rgb(255, 68, 107)", "rgb(74, 74, 77)"];
let rgba_colors = ["rgba(0, 153, 220, 0.4)", "rgba(255, 165, 0, 0.4)", "rgba(255, 68, 107, 0.4)", "rgba(74, 74, 77, 0.4)"];

(function() {
  setRandomLinkColor();
  setBioEventListener();
  setDarkModeGivenDayTime();
  setInterval(() => {
    setDarkModeGivenDayTime();
  }, 1000 * 30);
})();


/* Dark Mode */
function setModeEventListener() {
  let list = document.body.classList;
  document.getElementById("toggler").addEventListener("change", event => {
    if (event.target.checked) {
      list.add("dark-mode");
    } else {
      list.remove("dark-mode");
    }
  });
}

function setDarkModeGivenDayTime() {
  var today = new Date();
  var time = today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds();
  let list = document.body.classList;
  if (today.getHours() < 6 || (18 < today.getHours() && today.getHours()< 24)) {
    list.add("dark-mode");
  } else {
    list.remove("dark-mode");
  }
}

/* Colors */
function getRandomColor(alpha=false) {
  if (alpha) {
    return rgba_colors[Math.floor(Math.random() * colors.length)];
  }
  else {
    return rgb_colors[Math.floor(Math.random() * colors.length)];
  }
}

function setRandomLinkColor() {
  Array.from(document.getElementsByTagName("a")).forEach(e => {
    e.style.color = getRandomColor();
  });
  Array.from(document.getElementsByClassName("rnd-bkg-color")).forEach(e => {
    e.style.background = getRandomColor();
  });
  Array.from(document.getElementsByClassName("rnd-bkg-color-alpha")).forEach(e => {
    e.style.background = getRandomColor(true);
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