const gameBoard = document.getElementById("game-board");
const imgShadowContainer = document.getElementById("imgShadow");
const imgOptions = document.getElementById("imgOptions");

const images = [
  "/static/images/whoAmI/ball.png",
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
        alert("Correct!");
        nextPhase();
      } else {
        alert("Try again!");
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
    alert("Parabéns! Você completou todas as fases!");
    // Aqui você pode reiniciar ou mostrar um botão de reinício, se quiser
  }
}

// Inicializa o jogo
createImageShadow();
createImageOptions();
