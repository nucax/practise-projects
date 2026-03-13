const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");

// Game variables
let ballRadius, x, y, dx, dy;
let paddleHeight, paddleWidth, paddleX;
let brickRowCount = 6;
let brickColumnCount = 10;
let brickWidth, brickHeight, brickPadding = 10, brickOffsetTop = 50, brickOffsetLeft = 35;
let score = 0;
let rightPressed = false, leftPressed = false;

// Rainbow bricks
let bricks = [];
const rainbowColors = ["#FF0000", "#FF7F00", "#FFFF00", "#00FF00", "#0000FF", "#8B00FF"];
for(let c=0; c<brickColumnCount; c++){
  bricks[c] = [];
  for(let r=0; r<brickRowCount; r++){
    bricks[c][r] = {x:0, y:0, status:1, color: rainbowColors[r % rainbowColors.length]};
  }
}

// Responsive canvas & high-DPI support
function resizeCanvas() {
  const width = window.innerWidth * 0.95;
  const height = window.innerHeight * 0.7; // keep enough room for leaderboard
  const dpr = window.devicePixelRatio || 1;
  canvas.width = width * dpr;
  canvas.height = height * dpr;
  canvas.style.width = width + "px";
  canvas.style.height = height + "px";
  ctx.setTransform(1,0,0,1,0,0); // reset transform
  ctx.scale(dpr, dpr); // scale for high DPI
  adjustSizes(width, height);
}

function adjustSizes(width, height){
  paddleWidth = width * 0.15;
  paddleHeight = height * 0.025;
  paddleX = (width - paddleWidth)/2;

  ballRadius = width * 0.015;
  dx = width * 0.006;
  dy = -height * 0.006;

  brickWidth = (width - brickOffsetLeft*2 - (brickColumnCount-1)*brickPadding)/brickColumnCount;
  brickHeight = height * 0.04;
}

window.addEventListener('resize', resizeCanvas);
resizeCanvas();

// Keyboard Controls
document.addEventListener("keydown", e => {
  if(e.key === "ArrowRight") rightPressed = true;
  if(e.key === "ArrowLeft") leftPressed = true;
});
document.addEventListener("keyup", e => {
  if(e.key === "ArrowRight") rightPressed = false;
  if(e.key === "ArrowLeft") leftPressed = false;
});

// Touch Controls
canvas.addEventListener("touchstart", handleTouch, {passive:false});
canvas.addEventListener("touchmove", handleTouch, {passive:false});
function handleTouch(e){
  e.preventDefault();
  const touch = e.touches[0];
  const rect = canvas.getBoundingClientRect();
  const touchX = touch.clientX - rect.left;
  paddleX = touchX - paddleWidth/2;
  if(paddleX < 0) paddleX = 0;
  if(paddleX + paddleWidth > canvas.width) paddleX = canvas.width - paddleWidth;
}

// Collision Detection
function collisionDetection(){
  for(let c=0;c<brickColumnCount;c++){
    for(let r=0;r<brickRowCount;r++){
      let b = bricks[c][r];
      if(b.status === 1 && x > b.x && x < b.x + brickWidth && y > b.y && y < b.y + brickHeight){
        dy = -dy;
        b.status = 0;
        score++;
        if(score === brickRowCount*brickColumnCount){
          alert("YOU WIN!");
          saveScore(score);
          document.location.reload();
        }
      }
    }
  }
}

// Draw Functions
function drawBall(){
  ctx.beginPath();
  ctx.arc(x, y, ballRadius, 0, Math.PI*2);
  ctx.fillStyle = "#FFFFFF";
  ctx.fill();
  ctx.closePath();
}

function drawPaddle(){
  ctx.beginPath();
  ctx.rect(paddleX, canvas.height / (window.devicePixelRatio || 1) - paddleHeight, paddleWidth, paddleHeight);
  ctx.fillStyle = "#FFFFFF";
  ctx.fill();
  ctx.closePath();
}

function drawBricks(){
  for(let c=0;c<brickColumnCount;c++){
    for(let r=0;r<brickRowCount;r++){
      let b = bricks[c][r];
      if(b.status === 1){
        let brickX = c*(brickWidth+brickPadding)+brickOffsetLeft;
        let brickY = r*(brickHeight+brickPadding)+brickOffsetTop;
        b.x = brickX;
        b.y = brickY;
        ctx.beginPath();
        ctx.rect(brickX, brickY, brickWidth, brickHeight);
        ctx.fillStyle = b.color;
        ctx.fill();
        ctx.closePath();
      }
    }
  }
}

function drawScore(){
  ctx.font = `${canvas.height*0.04}px Arial`;
  ctx.fillStyle = "#FFFFFF";
  ctx.fillText("Score: "+score, 10, 30);
}

// Game Loop
function draw(){
  ctx.clearRect(0,0,canvas.width,canvas.height);
  drawBricks();
  drawBall();
  drawPaddle();
  drawScore();
  collisionDetection();

  const canvasHeight = canvas.height / (window.devicePixelRatio || 1);

  if(x + dx > canvas.width / (window.devicePixelRatio || 1) - ballRadius || x + dx < ballRadius) dx = -dx;
  if(y + dy < ballRadius) dy = -dy;
  else if(y + dy > canvasHeight - ballRadius){
    if(x > paddleX && x < paddleX + paddleWidth) dy = -dy;
    else {
      alert("GAME OVER");
      saveScore(score);
      document.location.reload();
    }
  }

  if(rightPressed && paddleX < canvas.width / (window.devicePixelRatio || 1) - paddleWidth) paddleX += 7;
  if(leftPressed && paddleX > 0) paddleX -= 7;

  x += dx;
  y += dy;
  requestAnimationFrame(draw);
}

// Start position
x = canvas.width / (2 * (window.devicePixelRatio || 1));
y = canvas.height / (window.devicePixelRatio || 1) - 30;

draw();
