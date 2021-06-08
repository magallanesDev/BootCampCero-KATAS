var folio = document.querySelector("#folio")


function gestionaRespuestaAsincrona() {
    if (this.readyState === 4 && this.status === 200) {   // ha ido todo bien
        console.log(this.responseText)
        const respuesta = JSON.parse(this.responseText)

        if (respuesta.Response === 'False') {
            alert("No se ha encontrado el título de la película")
        }

        folio.innerHTML = ""  // borramos el folio cuando hacemos una nueva búsqueda

        for (let i = 0; i < respuesta.Search.length; i++) {
            const pelicula = respuesta.Search[i]

            const div = document.createElement("div")
            div.className = "pelicula"

            const img = document.createElement("img")
            img.setAttribute("src", pelicula.Poster)
            img.setAttribute("alt", "Carátula de la película")

            const p = document.createElement("p")
            const textoP = `${pelicula.Title} (${pelicula.Year})`
            p.innerHTML = textoP

            const btn = document.createElement("a")
            btn.setAttribute("href", `https://imdb.com/title/${pelicula.imdbID}/`)
            btn.setAttribute("target", "_blank") // para crear una nueva pestaña en el navegador
            btn.className = "button"
            btn.classList.add("info") // añadimos la clase info además de la button
            btn.innerHTML = "Más info..."

            p.appendChild(btn)

            div.appendChild(img)
            div.appendChild(p)

            folio.appendChild(div)
        }
    }
}

const xhr = new XMLHttpRequest()  // creamos una instancia de este objeto (gestor de peticiones asíncronas)
xhr.onload = gestionaRespuestaAsincrona


document.querySelector("#buscar")
    .addEventListener("click", () => {
        const palabras = document.querySelector("#entrada").value
        xhr.open('GET', `http://www.omdbapi.com/?s=${palabras}&apikey=2bf0cc92`, true)
        xhr.send()
        console.log("He lanzado petición")
    })