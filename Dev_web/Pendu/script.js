
// il faudrait lower les mots aprés les avoirs chargé ainsi que l'entrée du user
// pouvoir valider avec la touche entrée
// Charger le fichier text et choisir un mot au hasard dans la liste de mot
fetch("liste.txt")
.then(response => response.text()) // pourquoi et comment then...
.then(data =>{
    var wordList = data.split("\n");
    var randomIndex = Math.floor(Math.random() * wordList.length); //Comment fonctionne Math.floor, Math.range()
    const wordToGuess = wordList[randomIndex];

    //alert(wordToGuess);

    var wordLength = wordToGuess.length;
    var hiddenWord = "";
    for(var i=0; i < wordLength; i++){
        hiddenWord += "_";
    }

    document.getElementById("word").innerHTML = hiddenWord;
    var guessInput = document.getElementById("guess");
    var submitButton = document.getElementById("submit");
    var link = document.getElementById("link"); 
    var result = document.getElementById("result") ; 

    submitButton.onclick = function(){
        var guess = guessInput.value;

        if(guess.length > 1 || guess.length === 0){
            result.innerHTML = "Entrer une seule lettre !";
        }else if(wordToGuess.indexOf(guess) === -1){
            result.innerHTML = "Mauvaise lettre !";
        }else{
            for(var i = 0; i < wordToGuess.length; i++){
                if(wordToGuess[i] === guess){
                    hiddenWord = hiddenWord.substr(0,i) + guess + hiddenWord.substr(i+1);
                }
            }

            document.getElementById("word").innerHTML = hiddenWord;

            if(hiddenWord === wordToGuess){
                result.innerHTML = "Bravo !";
                guessInput.style.display = "none";
                submitButton.style.display = "none";
                link.style.display = "block";
            }else{
                result.innerHTML = "Bonne lettre !";
            }

            guess.value = ""

        }
    }
})