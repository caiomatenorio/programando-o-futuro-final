const gameBoard = document.getElementById("game-board");
const imgShadowContainer = document.getElementById("imgShadow");
const imgOptions = document.getElementById("imgOptions");

const correctContainer = document.getElementById("correct");
const incorrectContainer = document.getElementById("incorrect");
const gameWinnerContainer = document.getElementById("gameWin");
const messagesContainer = document.getElementById("messagesContainer");

const images = [
  "/static/images/whoAmI/car.png",
  "/static/images/whoAmI/book.png",
  "/static/images/whoAmI/dog.png",
  "/static/images/whoAmI/house.png",
  "/static/images/whoAmI/pencil.png",
];

let shadowImageSrc = null;
let lastShadowImageSrc = null;
let currentPhase = 1;
const totalPhases = 3;

function createImageShadow() {
  let newShadow;
  do {
    newShadow = images[Math.floor(Math.random() * images.length)];
  } while (newShadow === lastShadowImageSrc);
  shadowImageSrc = newShadow;
  lastShadowImageSrc = shadowImageSrc;

  imgShadowContainer.innerHTML = "";
  const img = document.createElement("img");
  img.src = shadowImageSrc;
  imgShadowContainer.appendChild(img);
}

function createImageOptions() {
  imgOptions.innerHTML = "";
  const options = new Set();

  while (options.size < 3) {
    options.add(images[Math.floor(Math.random() * images.length)]);
  }

  if (!options.has(shadowImageSrc)) {
    const optionsArr = Array.from(options);
    optionsArr[Math.floor(Math.random() * 3)] = shadowImageSrc;
    options.clear();
    optionsArr.forEach((opt) => options.add(opt));
  }

  options.forEach((image) => {
    const img = document.createElement("img");
    img.src = image;
    img.classList.add("option-image");
    img.addEventListener("click", () => {
      const shadowImage = imgShadowContainer.querySelector("img");
      if (shadowImage && shadowImage.src === img.src) {
        if (currentPhase === totalPhases) {
          gameWinnerContainer.style.display = "flex";
          messagesContainer.style.display = "flex";
        } else {
          correctContainer.style.display = "flex";
          messagesContainer.style.display = "flex";
          setTimeout(() => {
            correctContainer.style.display = "none";
            messagesContainer.style.display = "none";
          }, 1500);
          nextPhase();
        }
      } else {
        incorrectContainer.style.display = "flex";
        messagesContainer.style.display = "flex";

        setTimeout(() => {
          incorrectContainer.style.display = "none";
          messagesContainer.style.display = "none";
        }, 1500);
      }
    });
    imgOptions.appendChild(img);
  });
}

function nextPhase() {
  if (currentPhase < totalPhases) {
    currentPhase++;
    createImageShadow();
    createImageOptions();
  } else {
    gameWinnerContainer.style.display = "flex";
    messagesContainer.style.display = "flex";
  }
}

function resetGame() {
  currentPhase = 1;
  gameWinnerContainer.style.display = "none";
  messagesContainer.style.display = "none";
  correctContainer.style.display = "none";
  incorrectContainer.style.display = "none";

  createImageShadow();
  createImageOptions();
}
createImageShadow();
createImageOptions();
