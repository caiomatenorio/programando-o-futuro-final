const gameBoard = document.getElementById("gameBoard")
const totalCards = 10
let cards = []
let flippedCards = []
let matchedCards = 0

function createCards() {
    const cardValues = []


    // criar os pares de carta (mudar para imagens depois)
    for (let i = 1; i <= totalCards / 2; i++) {
        cardValues.push(i, i)
    }

    cardValues.sort(() => Math.random() - 0.5)

    cardValues.forEach(value => {
        const card = document.createElement('div')
        card.classList.add('card')
        card.dataset.value = value
        card.addEventListener('click', handleCardClick)
        gameBoard.appendChild(card)
        cards.push(card)
    })
}

function handleCardClick(event) {
    const clickedCard = event.target

    if(flippedCards.length < 2 && !clickedCard.classList.contains("flipped") && !clickedCard.classList.contains('matched')) {
        flippedCards.push(clickedCard)
        clickedCard.classList.add('flipped')
        clickedCard.textContent = clickedCard.dataset.value

        if (flippedCards.length === 2) {
            checkForMatch()
        }
    }
}

function checkForMatch() {
    const [card1, card2] = flippedCards

    if (card1.dataset.value === card2.dataset.value) {
        card1.classList.add('matched')
        card2.classList.add('matched')
        matchedCards += 2

        if (matchedCards === totalCards) {
            setTimeout(() => alert("Você Ganhou!"), 500)
        }
    } else {
        setTimeout(() => {
            card1.classList.remove('flipped')
            card2.classList.remove('flipped')
            card1.textContent = ''
            card2.textContent = ''
        }, 1000)
    }

    flippedCards = []
}

createCards()