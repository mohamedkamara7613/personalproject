
// il faudrait lower les mots aprés les avoirs chargé ainsi que l'entrée du user

// Charger le fichier text et choisir un mot au hasard dans la liste de mot
fetch("liste.txt")
.then(response => response.text()) // pourquoi et comment then...
.then(data =>{
    var wordList = data.split("\n");
    var randomIndex = Math.floor(Math.random() * wordList.length); //Comment fonctionne Math.floor, Math.range()
    const wordToGuess = wordList[randomIndex].toLowerCase();

    //alert(wordToGuess);

    var wordLength = wordToGuess.length;
    var hiddenWordArray = new Array(wordLength).fill("_");
    var hiddenWord = hiddenWordArray.join("");
    

    document.getElementById("word").innerHTML = hiddenWord;
    var guessInput = document.getElementById("guess");  
    var submitButton = document.getElementById("submit");
    var link = document.getElementById("link"); 
    var result = document.getElementById("result") ; 
    
    function main(){
        var guess = guessInput.value.toLowerCase();
        console.log(guess);

        if(guess.length > 1 || guess.length === 0){
            result.innerHTML = "Entrer une seule lettre !";
        }else if(wordToGuess.indexOf(guess) === -1){
            result.innerHTML = "Mauvaise lettre !";
        }else{
            for(var i = 0; i < wordToGuess.length; i++){
                if(wordToGuess[i] === guess){
                    //hiddenWord = hiddenWord.substr(0,i) + guess + hiddenWord.substr(i+1);
                    hiddenWordArray[i] = guess;
                }
            }
            hiddenWord = hiddenWordArray.join("");
            document.getElementById("word").innerHTML = hiddenWord;

            if(hiddenWord === wordToGuess){
                result.innerHTML = "Bravo !";
                guessInput.style.display = "none";
                submitButton.style.display = "none";
                link.style.display = "block";
            }else{
                result.innerHTML = "Bonne lettre !";
            }

            guessInput.value = ""

        }
    }
    submitButton.onclick = main;
    guessInput.onkeyup = function(e){
        if(e.key === "Enter"){
            main();
            }
        }
})