function gestionaRespuesta() {
    if (this.readyState === 4 && this.status === 200) {
        console.log(this.responseText)
        const respuesta = JSON.parse(this.responseText)

        if (respuesta.status != "success") {
            alert("Se ha producido un error en la traducción")
            return
        }

        const parrafo = document.createElement("p")
        const elfolio = document.querySelector("#folio")
        parrafo.innerHTML = respuesta.pilengua
        elfolio.appendChild(parrafo)

    }   
}


xhr = new XMLHttpRequest()
xhr.onload = gestionaRespuesta


document.querySelector("#btn-aceptar")
    .addEventListener("click", () => { 
        const laEntrada = document.querySelector("#entrada").value
        const url = `http://localhost:5000/pilengua/${laEntrada}`
        xhr.open("GET", url, true)
        xhr.send()
        console.log("peticion", url, "realizado")
    })