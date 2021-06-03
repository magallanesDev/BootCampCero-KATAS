let botones=document.querySelectorAll(".boton")
for (let i=0; i < botones.length; i++) {
    botones[i].addEventListener("click", (evento) => { 
        origen = evento.target.innerHTML
        entrada = document.querySelector("#entrada")
        parrafo = document.createElement("p")
        folio = document.querySelector("#folio")
        folio.appendChild(parrafo)
        parrafo.innerHTML = `${origen} dice ${entrada.value}!!!`
    })
}