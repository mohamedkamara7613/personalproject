
//sil y a ajout de score prendre ne compte le cas ou le jeu entre la meme lettre juste deux fois ne pas le compter deux fois
// peut etre resolu en faisant une liste de lettre juste entrer par le user
//s'il tape une lettre verifier si elle est dans la liste si oui cela veut dire que la lettre est juste et à deja etait entrer
//donc ne rien faire Sinon continuer comme d'habitude

// Charger le fichier text et choisir un mot au hasard dans la liste de mot
fetch("liste.txt")
.then(response => response.text()) // pourquoi et comment then...
.then(data =>{
    var wordList = data.split("\n").filter(word => word.trim() !== "");
    var randomIndex = Math.floor(Math.random() * wordList.length); //Comment fonctionne Math.floor, Math.range()
    const wordToGuess = wordList[randomIndex].toLowerCase();
    const wordContainer = document.getElementById("word");
    const hangmanImage = document.querySelector(".hangman img");
    

    //alert(wordToGuess);

    var wordLength = wordToGuess.length;
    var hiddenWordArray = new Array(wordLength).fill("_");
    var hiddenWord = hiddenWordArray.join(""); 

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

    let mistakes = 0;
    const maxGuess = 6;

    function handleWrongGuess() {
        if (mistakes < maxGuess) {
            hangmanImage.src = `images/hangman-${mistakes}.svg`; // Afficher une nouvelle partie
            mistakes++;
        }
        if (mistakes === maxGuess) {
            // Jeu terminé, le bonhomme est complet
            document.getElementById("result").innerText = "Vous avez perdu !";
            document.getElementById("guess").disabled = true; // Désactiver les entrées
            document.getElementById("submit").disabled = true;
        }
    }
    
    function main(){
        var guess = guessInput.value.toLowerCase();

        if(guess === "4123"){
            console.log(wordToGuess);
            guess = ""
        }
        if(guess.length > 1 || guess.length === 0){
            result.innerHTML = "Entrer une seule lettre !";
        }else if(wordToGuess.indexOf(guess) === -1){
            result.innerHTML = "Mauvaise lettre !";
            guessInput.value = ""
            hangmanImage.src = "images/hangman-0.svg";
            // animation de message afficher à l'ecran 
            result.style.color = "red";
            result.style.transform = "scale(1.2)";
            setTimeout(() => result.style.transform = "scale(1)", 500);
            // creer une classe pour l'animation de la lettre
            wordContainer.classList.add("letter-wrong");
            setTimeout(() => wordContainer.classList.remove("letter-wrong"), 500); // Supprime l'animation après 500ms
            // mise à jour de l'erreur et de l'animation associée
            handleWrongGuess();
        
        }else{
            // Quand une lettre est trouvée
            for(var i = 0; i < wordToGuess.length; i++){
                if(wordToGuess[i] === guess){
                    //hiddenWord = hiddenWord.substr(0,i) + guess + hiddenWord.substr(i+1);
                    result.textContent = "Bonne lettre"
                    result.style.color = "blue";
                    //hiddenWordArray[i] = guess;
                    const span = document.querySelectorAll("#word span")[i];
                    span.textContent = guess; // Remplace "_" par la lettre devinée
                    const letterSpan = wordContainer.children[i];
                    letterSpan.classList.add("letter-correct") 
                    setTimeout(() => letterSpan.classList.remove("letter-correct"), 500); // Supprime l'animation après 500ms)
                }
            }
            //hiddenWord = hiddenWordArray.join("");
            //document.getElementById("word").innerHTML = hiddenWord;
            // Vérifier si le mot est entièrement deviné
            const revealedWord = Array.from(document.querySelectorAll("#word span"))
            .map(span => span.textContent)
            .join("");

            if(revealedWord === wordToGuess){
                result.innerHTML = "Bravo vous avez trouvé le mot !";
                result.style.color = "green";
                result.style.transform = "scale(1.2)";
                setTimeout(() => result.style.transform = "scale(1)", 500);
                guessInput.style.display = "none";
                submitButton.style.display = "none";
                link.style.display = "block";
                link.onclick = function (){
                    window.location.reload();
                    hangmanImage.src = "images/hangman-0.svg";
                }
                confetti({
                    particleCount: 100,
                    spread: 70,
                    origin: { y: 0.6 }
                });
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

