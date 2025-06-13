const circles = document.querySelectorAll(".circle");
const targets = document.querySelectorAll(".target");

circles.forEach(circle => {
    circle.addEventListener("dragstart", (e) => {
    e.dataTransfer.setData("color", circle.dataset.color);
    e.dataTransfer.setData("id", circle.dataset.color);
    setTimeout(() => {
        circle.style.display = "none";
    }, 0);
    });

    circle.addEventListener("dragend", () => {
    circle.style.display = "block";
    });
});

targets.forEach(target => {
    target.addEventListener("dragover", (e) => {
    e.preventDefault();
    });

    target.addEventListener("drop", (e) => {
    e.preventDefault();
    const draggedColor = e.dataTransfer.getData("color");
    const draggedEl = document.querySelector(`.circle[data-color='${draggedColor}']`);
    const targetColor = target.dataset.color;

    if (draggedColor === targetColor && target.children.length === 0) {
        draggedEl.classList.add("placed");
        draggedEl.classList.remove("circle");
        draggedEl.setAttribute("draggable", "false");
        draggedEl.style.display = "block";
        target.appendChild(draggedEl);

        const allFilled = Array.from(targets).every(t => t.children.length === 1 && t.firstElementChild.classList.contains("placed"));
        if (allFilled) {
            alert("Parabéns! Você completou as cores!" );
        }
    } else {
        draggedEl.style.display = "block";
    }
    });
});