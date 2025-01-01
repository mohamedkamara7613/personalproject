// Récupérer le canvas et son contexte
const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");

// Paramètres de jeu
const gridSize = 20;
let snake = [{ x: 5 * gridSize, y: 5 * gridSize }];
let direction = { x: 0, y: 0 };
let food = { 
    x: Math.floor(Math.random() * canvas.width / gridSize) * gridSize, 
    y: Math.floor(Math.random() * canvas.height / gridSize) * gridSize 
};
let gameOver = false;

// Dessiner le jeu
function drawGame() {
    // Effacer l'écran
    ctx.fillStyle = "black";
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // Dessiner la nourriture
    ctx.fillStyle = "red";
    ctx.fillRect(food.x, food.y, gridSize, gridSize);

    // Dessiner le serpent
    ctx.fillStyle = "green";
    for (const segment of snake) {
        ctx.fillRect(segment.x, segment.y, gridSize, gridSize);
    }
}

// Mettre à jour la logique du jeu
function updateGame() {
    if (gameOver) return;

    // Calculer la nouvelle position de la tête
    const head = {
        x: (snake[0].x + direction.x * gridSize + canvas.width) % canvas.width,
        y: (snake[0].y + direction.y * gridSize + canvas.height) % canvas.height
    };

    // Vérifier si le serpent se mord
    if (snake.some(segment => segment.x === head.x && segment.y === head.y)) {
        gameOver = true;
        alert("Game Over!");
        return;
    }

    // Ajouter la nouvelle tête
    snake.unshift(head);

    // Vérifier si le serpent mange la nourriture
    if (head.x === food.x && head.y === food.y) {
        food = {
            x: Math.floor(Math.random() * canvas.width / gridSize) * gridSize,
            y: Math.floor(Math.random() * canvas.height / gridSize) * gridSize
        };
    } else {
        // Retirer la queue (le serpent avance)
        snake.pop();
    }
}

// Gérer les entrées clavier
window.addEventListener("keydown", (e) => {
    if (e.key === "ArrowUp" && direction.y === 0) direction = { x: 0, y: -1 };
    if (e.key === "ArrowDown" && direction.y === 0) direction = { x: 0, y: 1 };
    if (e.key === "ArrowLeft" && direction.x === 0) direction = { x: -1, y: 0 };
    if (e.key === "ArrowRight" && direction.x === 0) direction = { x: 1, y: 0 };
});

// Boucle principale
function gameLoop() {
    updateGame();
    drawGame();
    if (!gameOver) setTimeout(gameLoop, 100); // Met à jour le jeu toutes les 100ms
}

gameLoop();
