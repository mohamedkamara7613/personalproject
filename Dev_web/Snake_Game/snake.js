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
                for(var i=0; i < snake.length; i++){
                    if (event.key === "ArrowUp" && snake[i].direction !== "down"){
                        snake[i].direction = "up";
                    }
                    if (event.key === "ArrowDown" && snake[i].direction !== "up"){
                        snake[i].direction = "down";
                    }
                    if (event.key === "ArrowRight" && snake[i].direction !== "left"){
                        snake[i].direction = "right";
                    }
                    if (event.key === "ArrowLeft" && snake[i].direction !== "right"){
                        snake[i].direction = "left";
                    }
                }
            }
            
        };
// -------------------------------------------------------------------------------------------------------------------------
        function updateGame(){
             // Clear the canvas
            ctx.clearRect(0, 0, canvas.width, canvas.height); 

            // Si la nourriture est mangée -> augmenter le serpent
            if (snake_head.x === food.x && snake_head.y === food.y){
                let snake_current_queue = snake[snake.length-1];
                snake.push(
                    {   
                        x : snake_current_queue.x,
                        y : snake_current_queue.y,
                        direction : snake_current_queue.direction
                        }       
                );
            };

            for (var i=0; i < snake.length; i++){
                // Mise a jour de la position du serpent
                if (snake[i].direction === "up"){
                    snake[i].y -= box_size;
                }
                if (snake[i].direction === "down"){
                    snake[i].y += box_size;
                }
                if (snake[i].direction === "left"){
                    snake[i].x -= box_size;
                }
                if (snake[i].direction === "right"){
                    snake[i].x += box_size;
                }    
            }
            
            

        }
// -------------------------------------------------------------------------------------------------------------------------
        
        function drawGrid(){
            
            // Dessine le serpent
            console.log(snake);
            for (var i=0; i < snake.length; i++){
                ctx.fillStyle = "green";
                ctx.fillRect(snake[i].x, snake[i].y, box_size, box_size);
            }
        

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
    
    
}