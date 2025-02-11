let paddle;
let ball;
let bricks = [];
let rows = 4;
let cols = 8;
let brickWidth;
let brickHeight = 20;
let gameOver = true;
let displayArea;

function setup() {
  createCanvas(windowWidth * 0.9, windowHeight * 0.7);

  paddle = new Paddle();
  ball = new Ball();

  startButton = createButton('Start');
  startButton.size(150, 40);
  startButton.style('font-size', '24px');
  startButton.style('text-align', 'center');
  startButton.mousePressed(gameStart);
  // displayArea = createP('ball speed');
  // displayArea.position(width / 2 - 80, height /2);
  // displayArea.style('color', 'white');
  brickWidth = width / cols;
  for (let row = 0; row < rows; row++) {
    for (let col = 0; col < cols; col++) {
      bricks.push(new Brick(col * brickWidth, row * brickHeight, brickWidth, brickHeight));
    }
  }
}

function draw() {
  background(0);

  paddle.show();
  paddle.move();

  ball.show();
  ball.move();
  ball.checkEdges();
  ball.checkPaddle(paddle);

  if (gameOver === true) {
    gameIdle();
  }
  paddle.x = constrain(mouseX - paddle.width / 2, 0, width - paddle.width);

  for (let i = bricks.length - 1; i >= 0; i--) {
    bricks[i].show();
    if (ball.hits(bricks[i])) {
      bricks.splice(i, 1);
      ball.reverse();
    }
  }
  if (bricks.length === 0) {
    gameOver = true;
    textSize(32);
    fill(255, 0, 0);
    text('Congratulations!', width / 2 - 80, height / 2);
    text('Score: ' + String(rows * cols - bricks.length), width / 2 - 80, height / 2 + 120);
  }

  if (ball.offScreen()) {
    gameOver = true;
    textSize(32);
    fill(255, 0, 0);
    text('Game Over', width / 2 - 80, height / 2);
    text('Score: ' + String(rows * cols - bricks.length), width / 2 - 80, height / 2 + 120);
  }
}

function gameIdle() {
  noLoop();
}

function gameStart() {
  bricks.splice(0);
  for (let row = 0; row < rows; row++) {
    for (let col = 0; col < cols; col++) {
      bricks.push(new Brick(col * brickWidth, row * brickHeight, brickWidth, brickHeight));
    }
  }
  ball.x = width / 2;
  ball.y = brickHeight * rows + ball.radius;
  ball.xSpeed = random(2, 4);
  ball.ySpeed = random(4, 8);
  gameOver = false;
  loop();
}

function mouseDragged() {
  return false;
}

class Paddle {
  constructor() {
    this.width = 120;
    this.height = 20;
    this.x = width / 2 - this.width / 2;
    this.y = height - 40;
    this.speed = 7;
  }

  show() {
    fill(255);
    rect(this.x, this.y, this.width, this.height);
  }

  move() {
    // タッチ操作時はこのmove()は特に使わないが、今後キーボード操作などと併用する場合のために残す
  }
}

class Ball {
  constructor() {
    this.x = width / 2;
    this.radius = 10;
    this.y = brickHeight * rows + this.radius;
    this.xSpeed = random(2, 4);
    this.ySpeed = 4;
  }

  show() {
    fill(255);
    ellipse(this.x, this.y, this.radius * 2);
  }

  move() {
    this.x += this.xSpeed;
    this.y += this.ySpeed;
  }

  checkEdges() {
    if (this.x < 0 || this.x > width) {
      this.xSpeed *= -1;
    }
    if (this.y < 0) {
      this.ySpeed *= -1;
    }
  }

  checkPaddle(paddle) {
    if (this.y + this.radius > paddle.y &&
        this.y - this.radius < paddle.y &&
        this.x > paddle.x &&
        this.x < paddle.x + paddle.width) {
      this.ySpeed *= -1;
      this.y = paddle.y - this.radius;
    }
  }

  hits(brick) {
    return (this.x > brick.x && this.x < brick.x + brick.w &&
            this.y - this.radius < brick.y + brick.h &&
            this.y + this.radius > brick.y);
  }

  reverse() {
    this.ySpeed *= -1;
  }

  offScreen() {
    return this.y > height;
  }
}

class Brick {
  constructor(x, y, w, h) {
    this.x = x;
    this.y = y;
    this.w = w;
    this.h = h;
  }

  show() {
    fill(255, 100, 100);
    rect(this.x, this.y, this.w, this.h);
  }
}
