const inputElement = document.querySelector(".searchInp")
const searchBtn = document.querySelector(".searchBtn")
const textarea = document.querySelector(".textarea")

const API_URL = "http://localhost"

const searchFunction = () => {
  const songName = inputElement.value
  textarea.innerHTML = ""
  getLyrics(songName)
}

searchBtn.addEventListener("click", searchFunction)

document.addEventListener("keypress", (e) => {
  if (e.key == "Enter") {
    searchFunction()
  }
})
const getLyrics = async (songName) => {
  fetch(API_URL+"/lyrics?song="+songName, {
    method: "GET"
  })
    .then(response => response.text())
    .then(data => {
      textarea.innerHTML = data
    })
    .catch(error => console.error(error));
}