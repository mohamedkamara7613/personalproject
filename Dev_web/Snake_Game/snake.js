/*
    A faire plus tard :
        - rajouter la logique des boutons graphiques
        - Designer la fin du jeu
        - rajouter les sprites et le background

*/




function main(){
    // Creation de ma variable canvas et recuperatioin du context pour effectuer tous les opérations
    const canvas = document.querySelector("#myCanvas");

    if(canvas.getContext){
        const ctx = canvas.getContext("2d");

        // --------------- VARIABLES -------------------------
        // Taille des boites
        const box_size = 20;   
        // # Proprietés du serpent
        // snake est un tableau qui represente le corp et la tete du serpent
        let snake = [];
        let snake_head;
        let food;             
        // le score actuelle
        let currentScore;
        let highScore = 0;


// -------------------------------------------------------------------------------------------------------------------------
        function updateHighscore(newHighScore){
            highScore = newHighScore;
            const high_scoreElement = document.querySelector(".high-score");
            high_scoreElement.textContent = `High Score : ${highScore}`;
        };
// -------------------------------------------------------------------------------------------------------------------------
        function updateScore(newScore){
            currentScore = newScore;
            const scoreElement = document.querySelector(".score");
            scoreElement.textContent = `Score : ${currentScore}`;
        };
// -------------------------------------------------------------------------------------------------------------------------
        function generateFood(){
            // Génération d'un nouveau food
            // Proprieté de la nourriture
            food = {
                x : Math.floor(Math.random() * (canvas.width / box_size)) * box_size,
                y : Math.floor(Math.random() * (canvas.height / box_size)) * box_size,
                color : "red"
            };
        };
// -------------------------------------------------------------------------------------------------------------------------

        function initGame(){
            if (currentScore > highScore){
                updateHighscore(currentScore);
            };
            currentScore = 0;
            snake = [];
            // Initialisation de la position de la tete du serpent 
            // peut etre fait en utilisant push
            snake[0] = {
                x : Math.floor(canvas.width / (2 * box_size)) * box_size,
                y: Math.floor(canvas.height / (2 * box_size)) * box_size,
                direction : "none",
                color : "green"
            };
            snake_head = snake[0]

            // Genere la nouriture a une position aleatioire
            generateFood();
            updateScore(currentScore);
            
        };
// -------------------------------------------------------------------------------------------------------------------------

        function gestionEvenement(){
            // Gestion des evenements
            document.addEventListener("keydown", direction);
            
            function direction(event){
                for(var i=0; i < snake.length; i++){
                    if (event.key === "ArrowUp" && snake[i].direction !== "down"){
                        snake[i].direction = "up";
                    };
                    if (event.key === "ArrowDown" && snake[i].direction !== "up"){
                        snake[i].direction = "down";
                    };
                    if (event.key === "ArrowRight" && snake[i].direction !== "left"){
                        snake[i].direction = "right";
                    };
                    if (event.key === "ArrowLeft" && snake[i].direction !== "right"){
                        snake[i].direction = "left";
                    };
                };
            };

            const arrowLeftElement = document.querySelector("#ArrowLeft");
            const arrowRightElement = document.querySelector("#ArrowRight");
            const arrowUpElement = document.querySelector("#ArrowUp");
            const arrowDownElement = document.querySelector("#ArrowDown");

            arrowLeftElement.addEventListener("click", ()=>{
                for (var i=0; i < snake.length; i++){
                    if (snake[i].direction !== "right"){
                        snake[i].direction = "left";
                    };
                };
            });
            
            arrowRightElement.addEventListener("click", ()=>{
                for (var i=0; i < snake.length; i++){
                    if (snake[i].direction !== "left"){
                        snake[i].direction = "right";
                    };
                };
            });

            arrowUpElement.addEventListener("click", ()=>{
                for (var i=0; i < snake.length; i++){
                    if (snake[i].direction !== "down"){
                        snake[i].direction = "up";
                    };
                };
            });

            arrowDownElement.addEventListener("click", ()=>{
                for (var i=0; i < snake.length; i++){
                    if (snake[i].direction !== "up"){
                        snake[i].direction = "down";
                    };
                };
            });
        };
// -------------------------------------------------------------------------------------------------------------------------
        function updateGame(){
             // Clear the canvas
            ctx.clearRect(0, 0, canvas.width, canvas.height); 

            // Mise a jout des positions des segments du serpent ---------------------------------------
            for (var i=snake.length-1; i > 0;i--){
                snake[i].x = snake[i-1].x;
                snake[i].y = snake[i-1].y;
            };
            // Mise a jour de la position du serpent----------------------------------------------------
            if (snake_head.direction === "up"){
                snake_head.y -= box_size;
            };
            if (snake_head.direction === "down"){
                snake_head.y += box_size;
            };
            if (snake_head.direction === "left"){
                snake_head.x -= box_size;
            };
            if (snake_head.direction === "right"){
                snake_head.x += box_size;
            } ;

            // Si la nourriture est mangée -> augmenter le serpent----------------------------------------
            if (snake_head.x === food.x && snake_head.y === food.y){
                let snake_current_queue = snake[snake.length-1];
                snake.push(
                    {   
                        x : snake_current_queue.x,
                        y : snake_current_queue.y,
                        direction : snake_current_queue.direction
                        }       
                );

                // Augmenter le score et le mettre a jour
                currentScore++;
                updateScore(currentScore);
                

                // Generer a nouveau une nourriture a une position aleatoire
                generateFood();
            };
            
            // Gestion des collisoions ------------------------------------------------------------
            // si le serpent entre en collision avec son propre corps
            for (var i=1; i < snake.length-1; i++){
                if (snake_head.x === snake[i].x && snake_head.y === snake[i].y){
                    initGame();
                    alert("Game Over");
                };
            };
            // si le serpent touche les murs
            if (snake_head.x < 0 || snake_head.x + box_size > canvas.width || snake_head.y < 0 || snake_head.y + box_size> canvas.height){
                initGame();
                alert("Game Over");
            };
            

        };
// -------------------------------------------------------------------------------------------------------------------------
        
        function drawGrid(){
            
            // Dessine le serpent
            for (var i=0; i < snake.length; i++){
                ctx.fillStyle = "green";
                ctx.fillRect(snake[i].x, snake[i].y, box_size, box_size);
            };
        

            // Dessine la nourriture
            ctx.fillStyle = food.color;
            ctx.fillRect(food.x, food.y, box_size, box_size);
        };
// -------------------------------------------------------------------------------------------------------------------------

        initGame();
        gestionEvenement();

        // Mise a jour a intervalle de temps reguliers
        setInterval(()=>{
            
            updateGame();
            drawGrid();
        }, 200)
        
    };
    
    
};

