


// Charger le fichier text et choisir un mot au hasard dans la liste de mot
fetch("liste.txt")
.then(response => response.text()) // pourquoi et comment then...
.then(data =>{
    var wordList = data.split("\n").filter(word => word.trim() !== "");
    var randomIndex = Math.floor(Math.random() * wordList.length); //Comment fonctionne Math.floor, Math.range()
    const wordToGuess = wordList[randomIndex].toLowerCase();
    const wordContainer = document.getElementById("word");
    console.log(wordToGuess);

    //alert(wordToGuess);

    /* var wordLength = wordToGuess.length;
    var hiddenWordArray = new Array(wordLength).fill("_");
    var hiddenWord = hiddenWordArray.join(""); */

    // Efface le contenu actuel, au cas où un mot précédent était affiché
    wordContainer.innerHTML = "";

    //creer un <span> pour chaque lettre du mot
    for(let i=0; i < wordToGuess.length; i++){
        const span = document.createElement("span")
        span.textContent = "_";
        wordContainer.appendChild(span);
    }

    //document.getElementById("word").innerHTML = hiddenWord;
    var guessInput = document.getElementById("guess");  
    var submitButton = document.getElementById("submit");
    var link = document.getElementById("link"); 
    var result = document.getElementById("result") ; 
    
    function main(){
        var guess = guessInput.value.toLowerCase();
        let mistakes = 0;
        const parts = document.querySelectorAll(".part");

        if(guess.length > 1 || guess.length === 0){
            result.innerHTML = "Entrer une seule lettre !";
        }else if(wordToGuess.indexOf(guess) === -1){
            result.innerHTML = "Mauvaise lettre !";
            // animation de message afficher à l'ecran 
            result.style.color = "red";
            result.style.transform = "scale(1.2)";
            setTimeout(() => result.style.transform = "scale(1)", 500);
            // creer une classe pour l'animation de la lettre
            wordContainer.classList.add("letter-wrong");
            setTimeout(() => wordContainer.classList.remove("letter-wrong"), 500); // Supprime l'animation après 500ms
            // mise à jour de l'erreur et de l'animation associée
            if (mistakes < parts.length) {
                parts[mistakes].classList.add("visible"); // Affiche une partie
                mistakes++;
            }
        
        }else{
            // Quand une lettre est trouvée
            for(var i = 0; i < wordToGuess.length; i++){
                if(wordToGuess[i] === guess){
                    //hiddenWord = hiddenWord.substr(0,i) + guess + hiddenWord.substr(i+1);
                    hiddenWordArray[i] = guess;
                    const letterSpan = wordContainer.children[i];
                    letterSpan.classList.add("letter-correct")
                    setTimeout(() => letterSpan.classList.remove("letter-correct"), 500); // Supprime l'animation après 500ms)
                }
            }
            hiddenWord = hiddenWordArray.join("");
            document.getElementById("word").innerHTML = hiddenWord;

            if(hiddenWord === wordToGuess){
                result.innerHTML = "Bravo vous avez trouvé le mot !";
                result.style.color = "green";
                result.style.transform = "scale(1.2)";
                setTimeout(() => result.style.transform = "scale(1)", 500);
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
.catch(error => console.error("Erreur :", error));