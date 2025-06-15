document.addEventListener("DOMContentLoaded", () => {
  const fases = [
    { numero: 1, bolinhas: 1, gridClass: "grid1" },
    { numero: 2, bolinhas: 2, gridClass: "grid2" },
    { numero: 3, bolinhas: 3, gridClass: "grid3" },
    { numero: 4, bolinhas: 4, gridClass: "grid4" },
    { numero: 5, bolinhas: 5, gridClass: "grid5" }
  ];

  const container = document.querySelector(".container");
  let faseAtual = 0;

  function criarFase(fase) {
    const linha = document.createElement("div");
    linha.className = "linha";

    const caixaNumero = document.createElement("div");
    caixaNumero.className = "caixa-numero";
    caixaNumero.textContent = fase.numero;

    const igual = document.createElement("div");
    igual.className = "igual";
    igual.textContent = "=";

    const caixaResposta = document.createElement("div");
    caixaResposta.className = `caixa-resposta ${fase.gridClass}`;
    caixaResposta.addEventListener("drop", drop);
    caixaResposta.addEventListener("dragover", allowDrop);

    const circulos = document.createElement("div");
    circulos.className = "circulos";

    for (let i = 1; i <= fase.bolinhas; i++) {
      const circulo = document.createElement("div");
      circulo.className = "circulo";
      circulo.id = `bolinha${fase.numero}_${i}`;
      circulo.draggable = true;
      circulo.addEventListener("dragstart", drag);
      circulos.appendChild(circulo);
    }

    linha.appendChild(caixaNumero);
    linha.appendChild(igual);
    linha.appendChild(caixaResposta);
    linha.appendChild(circulos);

    return linha;
  }

  function iniciarProximaFase() {
    if (faseAtual < fases.length) {
      const fase = fases[faseAtual];
      const novaFase = criarFase(fase);

      if (container.firstChild) {
        container.replaceChild(novaFase, container.firstChild);
      } else {
        container.appendChild(novaFase);
      }
    } else {
        document.getElementById("messageContainer").style.display = "flex";
        document.getElementById("playAgain").addEventListener("click", () => {
          location.reload();
        });
    }
  }

  function allowDrop(ev) {
    ev.preventDefault();
  }

  function drag(ev) {
    ev.dataTransfer.setData("text", ev.target.id);
  }

  function drop(ev) {
    ev.preventDefault();
    const data = ev.dataTransfer.getData("text");
    const draggedElem = document.getElementById(data);
    const target = ev.target;

    if (!target.contains(draggedElem)) {
      target.appendChild(draggedElem);
    }

    const esperadas = fases[faseAtual].bolinhas;
    if (target.children.length === esperadas) {
      setTimeout(() => {
        faseAtual++;
        iniciarProximaFase();
      }, 400);
    }
  }

  iniciarProximaFase();
});
