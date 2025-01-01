// Charger le fichier text et choisir un mot au hasard dans la liste de mot
fetch("liste.txt")
.then(response => response.text()) // pourquoi et comment then...
.then(data =>{
    var wordList = data.split("\n");
    var randomIndex = Math.floor(Math.random() * wordList.length); //Comment fonctionne Math.floor, Math.range()
    const wordToGuess = wordList[randomIndex];

    var wordLength = wordToGuess.length;
    var hiddenWord = "";
    for(i=0; i < wordLength; i++){
        hiddenWord += "_"
    }

    document.getElementById("word").innerHTML = hiddenWord 
})