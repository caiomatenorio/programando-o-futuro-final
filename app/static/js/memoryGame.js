const gameBoard = document.getElementById("gameBoard");
const totalCards = 10;
let cards = [];
let flippedCards = [];
let matchedCards = 0;
let isChecking = false;

const containerWinGame = document.getElementById("shadowWinGame");

function createCards() {
  const cardValues = [];

  for (let i = 1; i <= totalCards / 2; i++) {
    cardValues.push(i, i);
  }

  cardValues.sort(() => Math.random() - 0.5);

  cardValues.forEach((value) => {
    const card = document.createElement("div");
    card.classList.add("card");
    card.dataset.value = value;
    gameBoard.appendChild(card);
    cards.push(card);
  });

  revealCardsTemporarily();
}

function revealCardsTemporarily() {
  cards.forEach((card) => {
    card.textContent = card.dataset.value;
    card.classList.add("flipped");
  });

  setTimeout(() => {
    cards.forEach((card) => {
      card.textContent = "";
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

  const clickedCard = event.target;

  if (
    flippedCards.length < 2 &&
    !clickedCard.classList.contains("flipped") &&
    !clickedCard.classList.contains("matched")
  ) {
    flippedCards.push(clickedCard);
    clickedCard.classList.add("flipped");
    clickedCard.textContent = clickedCard.dataset.value;

    if (flippedCards.length === 2) {
      isChecking = true; // Bloqueia interações enquanto verifica as cartas
      setTimeout(() => checkForMatch(), 1000); // Adiciona um delay para mostrar as cartas antes de verificar
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
      card1.textContent = "";
      card2.textContent = "";
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
