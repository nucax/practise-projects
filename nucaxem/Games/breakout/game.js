const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");

// Game Variables
let ballRadius = 10;
let x = canvas.width / 2;
let y = canvas.height - 30;
let dx = 4;
let dy = -4;

let paddleHeight = 10;
let paddleWidth = 100;
let paddleX = (canvas.width - paddleWidth) / 2;

let rightPressed = false;
let leftPressed = false;

let brickRowCount = 6;
let brickColumnCount = 10;
let brickWidth = 70;
let brickHeight = 20;
let brickPadding = 10;
let brickOffsetTop = 50;
let brickOffsetLeft = 35;

let score = 0;

// Create bricks with rainbow colors
let bricks = [];
const rainbowColors = ["#FF0000", "#FF7F00", "#FFFF00", "#00FF00", "#0000FF", "#8B00FF"];
for(let c=0; c<brickColumnCount; c++) {
  bricks[c] = [];
  for(let r=0; r<brickRowCount; r++) {
    bricks[c][r] = { x: 0, y: 0, status: 1, color: rainbowColors[r % rainbowColors.length] };
  }
}

// Event listeners
document.addEventListener("keydown", keyDownHandler);
document.addEventListener("keyup", keyUpHandler);

function keyDownHandler(e) {
  if(e.key === "Right" || e.key === "ArrowRight") rightPressed = true;
  if(e.key === "Left" || e.key === "ArrowLeft") leftPressed = true;
}
function keyUpHandler(e) {
  if(e.key === "Right" || e.key === "ArrowRight") rightPressed = false;
  if(e.key === "Left" || e.key === "ArrowLeft") leftPressed = false;
}

// Collision detection
function collisionDetection() {
  for(let c=0; c<brickColumnCount; c++) {
    for(let r=0; r<brickRowCount; r++) {
      let b = bricks[c][r];
      if(b.status === 1) {
        if(x > b.x && x < b.x + brickWidth && y > b.y && y < b.y + brickHeight) {
          dy = -dy;
          b.status = 0;
          score++;
          if(score === brickRowCount * brickColumnCount) {
            alert("YOU WIN!");
            saveScore(score);
            document.location.reload();
          }
        }
      }
    }
  }
}

// Draw functions
function drawBall() {
  ctx.beginPath();
  ctx.arc(x, y, ballRadius, 0, Math.PI*2);
  ctx.fillStyle = "#FFFFFF";
  ctx.fill();
  ctx.closePath();
}

function drawPaddle() {
  ctx.beginPath();
  ctx.rect(paddleX, canvas.height - paddleHeight, paddleWidth, paddleHeight);
  ctx.fillStyle = "#FFFFFF";
  ctx.fill();
  ctx.closePath();
}

function drawBricks() {
  for(let c=0; c<brickColumnCount; c++) {
    for(let r=0; r<brickRowCount; r++) {
      if(bricks[c][r].status === 1) {
        let brickX = c*(brickWidth+brickPadding)+brickOffsetLeft;
        let brickY = r*(brickHeight+brickPadding)+brickOffsetTop;
        bricks[c][r].x = brickX;
        bricks[c][r].y = brickY;
        ctx.beginPath();
        ctx.rect(brickX, brickY, brickWidth, brickHeight);
        ctx.fillStyle = bricks[c][r].color;
        ctx.fill();
        ctx.closePath();
      }
    }
  }
}

function drawScore() {
  ctx.font = "16px Arial";
  ctx.fillStyle = "#FFFFFF";
  ctx.fillText("Score: "+score, 8, 20);
}

// Game loop
function draw() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  drawBricks();
  drawBall();
  drawPaddle();
  drawScore();
  collisionDetection();

  if(x + dx > canvas.width-ballRadius || x + dx < ballRadius) dx = -dx;
  if(y + dy < ballRadius) dy = -dy;
  else if(y + dy > canvas.height-ballRadius) {
    if(x > paddleX && x < paddleX + paddleWidth) dy = -dy;
    else {
      alert("GAME OVER");
      saveScore(score);
      document.location.reload();
    }
  }

  if(rightPressed && paddleX < canvas.width - paddleWidth) paddleX += 7;
  if(leftPressed && paddleX > 0) paddleX -= 7;

  x += dx;
  y += dy;
  requestAnimationFrame(draw);
}

draw();
