const inputElement = document.querySelector(".searchInp");
const searchBtn = document.querySelector(".searchBtn");
const textarea = document.querySelector(".textarea");
const lang = document.getElementById("lang");

const API_URL = "http://localhost";

const searchFunction = () => {
  const songName = inputElement.value;
  const songLang = lang.options[lang.selectedIndex].value;
  if (!songName || !songLang) {
    console.log("Please enter a song name");
    return;
  }
  textarea.innerHTML = "";
  getLyrics(songName, songLang);
};

searchBtn.addEventListener("click", searchFunction);

document.addEventListener("keypress", (e) => {
  if (e.key == "Enter") {
    searchFunction();
  }
});
const getLyrics = async (songName, songLang) => {
  const args = "song=" + songName + "&lang=" + songLang
  fetch(API_URL + "/lyrics?" + args, {
    method: "GET",
  })
    .then((response) => response.text())
    .then((data) => {
      textarea.innerHTML = data;
      console.log("Fetched " + API_URL + "/lyrics?" + args);
    })
    .catch((error) => {
      console.error(error);
      fetch("http://192.168.49.2:30000/lyrics?" + args, {
        method: "GET",
      })
        .then((response) => response.text())
        .then((data) => {
          textarea.innerHTML = data;
          console.log(
            "Fetched http://192.168.49.2:30000/lyrics?" + args
          );
        })
        .catch((error) => console.error(error));
    });
};
