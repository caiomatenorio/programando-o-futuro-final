const input = document.getElementById("search-input");
const imgContainer = document.getElementById("imgContainer");
const imgResult = document.getElementById("imgResult");

const games = [
  {
    name: "Quem sou eu?",
    html: `<a href="jogos/quem-sou-eu"><img src="/static/images/home/quemSouEu.png" alt="Who am I"/></a>`,
  },
  {
    name: "Memória das Emoções",
    html: `<a href="jogos/jogo-da-memoria"><img src="/static/images/home/memoriaDasEmocoes.png" alt="Memory game"/></a>`,
  },
  {
    name: "Jogo das Cores",
    html: `<a href="jogos/jogo-das-cores"><img src="/static/images/home/jogoDasCores.png" alt="Color game"/></a>`,
  },
  {
    name: "Vamos Contar",
    html: `<a href="jogos/vamos-contar"><img src="/static/images/home/VamosContar.png" alt="Let's count"/></a>`,
  },
];

input.addEventListener("input", function () {
  const query = this.value.toLowerCase();
  if (query.length < 2) {
    imgContainer.style.display = "";
    imgResult.style.display = "none";
    imgResult.innerHTML = games.map((g) => g.html).join("");
    return;
  }
  const filtered = games.filter((g) => g.name.toLowerCase().includes(query));
  if (filtered.length === 1) {
    imgContainer.style.display = "none";
    imgResult.style.display = "flex";
    imgResult.innerHTML = filtered[0].html;
  } else if (filtered.length > 1) {
    imgContainer.style.display = "none";
    imgResult.style.display = "flex";
    imgResult.innerHTML = filtered.map((g) => g.html).join("");
  } else {
    imgResult.style.display = "none";
  }
});

input.addEventListener("blur", function () {
  if (!input.value) {
    imgResult.style.display = "none";
    imgContainer.style.display = "grid";
    imgResult.innerHTML = games.map((g) => g.html).join("");
  }
});
