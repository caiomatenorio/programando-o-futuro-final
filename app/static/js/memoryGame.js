const gameBoard = document.getElementById("gameBoard");
const totalCards = 10;
let cards = [];
let flippedCards = [];
let matchedCards = 0;
let isChecking = false;

const images = [
  "/static/images/memoryGame/happy.png",
  "/static/images/memoryGame/sad.png",
  "/static/images/memoryGame/angry.png",
  "/static/images/memoryGame/fear.png",
  "/static/images/memoryGame/disgust.png",
];

const containerWinGame = document.getElementById("shadowWinGame");

function createCards() {
  const cardValues = [];

  for (let i = 1; i <= totalCards / 2; i++) {
    cardValues.push(images[i - 1], images[i - 1]);
  }

  cardValues.sort(() => Math.random() - 0.5);

  cardValues.forEach((value) => {
    const card = document.createElement("div");
    card.classList.add("card");
    card.dataset.value = value;

    const img = document.createElement("img");
    img.src = value;
    img.style.display = "none";
    img.classList.add("card-image");
    card.appendChild(img);

    gameBoard.appendChild(card);
    cards.push(card);
  });

  revealCardsTemporarily();
}

function revealCardsTemporarily() {
  cards.forEach((card) => {
    card.querySelector("img").style.display = "block";
    card.classList.add("flipped");
  });

  setTimeout(() => {
    cards.forEach((card) => {
      card.querySelector("img").style.display = "none";
      card.classList.remove("flipped");
    });

    enableGame();
  }, 10000);
}

function enableGame() {
  cards.forEach((card) => {
    card.addEventListener("click", handleCardClick);
  });
}

function handleCardClick(event) {
  if (isChecking) return; // Bloqueia cliques enquanto as cartas estão sendo verificadas

  const clickedCard = event.currentTarget;

  if (
    flippedCards.length < 2 &&
    !clickedCard.classList.contains("flipped") &&
    !clickedCard.classList.contains("matched")
  ) {
    flippedCards.push(clickedCard);
    clickedCard.classList.add("flipped");

    clickedCard.querySelector("img").style.display = "block";

    if (flippedCards.length === 2) {
      isChecking = true; // Bloqueia interações enquanto verifica as cartas
      setTimeout(() => checkForMatch(), 1000);
    }
  }
}

function checkForMatch() {
  const [card1, card2] = flippedCards;

  if (card1.dataset.value === card2.dataset.value) {
    card1.classList.add("matched");
    card2.classList.add("matched");
    matchedCards += 2;

    if (matchedCards === totalCards) {
      containerWinGame.style.display = "flex"; // Exibe a tela de vitória
    }
  } else {
    setTimeout(() => {
      card1.classList.remove("flipped");
      card2.classList.remove("flipped");
      card1.querySelector("img").style.display = "none";
      card2.querySelector("img").style.display = "none";
    }, 1000);
  }

  flippedCards = [];
  isChecking = false;
}

function playAgain() {
  gameBoard.innerHTML = "";
  cards = [];
  flippedCards = [];
  matchedCards = 0;
  isChecking = false;
  containerWinGame.style.display = "none";
  createCards();
}

createCards();
