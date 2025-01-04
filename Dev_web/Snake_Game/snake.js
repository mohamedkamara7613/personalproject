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

        function initGame(){
            
            // Initialisation de la position de la tete du serpent 
            // peut etre fait en utilisant push
            snake[0] = {
                x : Math.floor(canvas.width / (2 * box_size)) * box_size,
                y: Math.floor(canvas.height / (2 * box_size)) * box_size,
                direction : "none",
                color : "green"
            };
            snake_head = snake[0]

            // Proprieté de la nourriture
            food = {
                x : Math.floor(Math.random() * (canvas.width / box_size)) * box_size,
                y : Math.floor(Math.random() * (canvas.height / box_size)) * box_size,
                color : "red"
            };
        };

        function gestionEvenement(){
            // Gestion des evenements
            document.addEventListener("keydown", direction);
            function direction(event){
                if (event.key === "ArrowUp" && snake_head.direction !== "down"){
                    snake_head.direction = "up";
                }
                if (event.key === "ArrowDown" && snake_head.direction !== "up"){
                    snake_head.direction = "down";
                }
                if (event.key === "ArrowRight" && snake_head.direction !== "left"){
                    snake_head.direction = "right";
                }
                if (event.key === "ArrowLeft" && snake_head.direction !== "right"){
                    snake_head.direction = "left";
                }
            }
        };

        function updateGame(){
             // Clear the canvas
            ctx.clearRect(0, 0, canvas.width, canvas.height); 

            // Mise a jour de la position du serpent
            if (snake_head.direction === "up"){
                snake_head.y -= box_size;
            }
            if (snake_head.direction === "down"){
                snake_head.y += box_size;
            }
            if (snake_head.direction === "left"){
                snake_head.x -= box_size;
            }
            if (snake_head.direction === "right"){
                snake_head.x += box_size;
            }

            // Si la nourriture est mangée -> augmenter le serpent
            

        }
        
        function drawGrid(){
            
            // Dessine le serpent
            ctx.fillStyle = snake_head.color;
            ctx.fillRect(snake_head.x, snake_head.y, box_size, box_size);

            // Dessine la nourriture
            ctx.fillStyle = food.color;
            ctx.fillRect(food.x, food.y, box_size, box_size);
        };

        initGame();
        gestionEvenement();
        setInterval(()=>{
            updateGame();
            drawGrid();
        }, 100)
        
    };
    
    
}