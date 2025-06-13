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

  if (!ev.target.contains(draggedElem)) {
    ev.target.appendChild(draggedElem);
  }
}
