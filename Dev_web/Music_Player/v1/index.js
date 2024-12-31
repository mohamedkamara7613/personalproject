let progress = document.getElementById("progress");
let song = document.getElementById("song");
let ctrlIcon = document.getElementById("ctrlIcon");

// Quand les métadonnées de la chanson sont chargées
song.onloadedmetadata = function(){
    progress.max = song.duration;
    progress.value = song.currentTime;
};

// Fonction playPause pour basculer entre play et pause
function playPause(){
    if(ctrlIcon.classList.contains("fa-pause")){
        song.pause();
        ctrlIcon.classList.remove("fa-pause");
        ctrlIcon.classList.add("fa-play");
    }
    else{
        song.play().then(() => { // Assurez-vous que la chanson commence à jouer avant d'ajouter l'icône "pause"
            ctrlIcon.classList.add("fa-pause");
            ctrlIcon.classList.remove("fa-play");
        }).catch(error => {
            console.error("Erreur lors du démarrage de la lecture : ", error);
        });
    }
}

// Mettre à jour la barre de progression en continu pendant la lecture
song.addEventListener("play", () => {
    setInterval(() => {
        progress.value = song.currentTime;
    }, 500);
});

// Changer la position de la lecture lorsque l'utilisateur modifie la barre de progression
progress.onchange = function(){
    song.currentTime = progress.value;
    song.play().then(() => { // Assurez-vous que la chanson commence à jouer
        ctrlIcon.classList.add("fa-pause");
        ctrlIcon.classList.remove("fa-play");
    }).catch(error => {
        console.error("Erreur lors du démarrage de la lecture : ", error);
    });
};
