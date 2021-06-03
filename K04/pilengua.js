document.querySelector("#btn-aceptar")
    .addEventListener("click", () => { 
        laEntrada = document.querySelector("#entrada")
        parrafo = document.createElement("p")
        elfolio = document.querySelector("#folio")
        elfolio.appendChild(parrafo)
        /*
        --> Hacer llamada al servidor de python (en el puerto 5000)
        --> me va a devolver json
        --> vamos a meter el json en el parrafo
        */
        parrafo.innerHTML = laEntrada.value
    })