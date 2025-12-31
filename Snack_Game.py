from tkinter import *
import random

GAME_WIDTH = 700
GAME_HEIGHT = 700
SPEED = 150
SPACE_SIZE = 50
BODY_PARTS = 3

SNAKE_COLOR = "#EF0B0B"
FOOD_COLOR = "blue"
BACKGROUND_COLOR = "white"

BORDER_COLOR = "#3A3A3A"
INNER_BLOCK_COLOR = "#7A7A7A"


class Snake:
    def __init__(self):
        self.coordinates = []
        self.squares = []

        for i in range(BODY_PARTS):
            self.coordinates.append([150, 150])

        for x, y in self.coordinates:
            self.squares.append(
                canvas.create_rectangle(
                    x, y,
                    x + SPACE_SIZE, y + SPACE_SIZE,
                    fill=SNAKE_COLOR,
                    outline="",
                    tag="snake"
                )
            )


class Food:
    def __init__(self):
        while True:
            x = random.randint(1, (GAME_WIDTH // SPACE_SIZE) - 2) * SPACE_SIZE
            y = random.randint(1, (GAME_HEIGHT // SPACE_SIZE) - 2) * SPACE_SIZE
            if [x, y] not in walls:
                break

        self.coordinates = [x, y]

        canvas.create_oval(
            x, y,
            x + SPACE_SIZE, y + SPACE_SIZE,
            fill=FOOD_COLOR,
            outline="black",
            tag="food"
        )


def create_walls():
    # -------- BORDER WALLS (VERY THIN) --------
    for x in range(0, GAME_WIDTH, SPACE_SIZE):
        walls.append([x, 0])
        walls.append([x, GAME_HEIGHT - SPACE_SIZE])

    for y in range(0, GAME_HEIGHT, SPACE_SIZE):
        walls.append([0, y])
        walls.append([GAME_WIDTH - SPACE_SIZE, y])

    for x, y in walls:
        canvas.create_rectangle(
            x, y,
            x + SPACE_SIZE, y + SPACE_SIZE,
            fill=BORDER_COLOR,
            outline="",
            tag="wall"
        )

    # -------- TWO L-SHAPED INNER BLOCKS --------
    l_block_1 = [
        [200, 200], [200, 250], [200, 300],
        [250, 300], [300, 300]
    ]

    l_block_2 = [
        [450, 200], [500, 200], [550, 200],
        [450, 250], [450, 300]
    ]

    for block in (l_block_1 + l_block_2):
        x, y = block
        canvas.create_rectangle(
            x + 5, y + 5,
            x + SPACE_SIZE - 5, y + SPACE_SIZE - 5,
            fill=INNER_BLOCK_COLOR,
            outline="black",
            width=1,
            tag="wall"
        )
        walls.append([x, y])


def next_turn(snake, food):
    x, y = snake.coordinates[0]

    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    snake.coordinates.insert(0, (x, y))

    snake.squares.insert(
        0,
        canvas.create_rectangle(
            x, y,
            x + SPACE_SIZE, y + SPACE_SIZE,
            fill=SNAKE_COLOR,
            outline="",
            tag="snake"
        )
    )

    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score
        score += 1
        label.config(text=f"Score: {score}")
        canvas.delete("food")
        food = Food()
    else:
        canvas.delete(snake.squares.pop())
        snake.coordinates.pop()

    if check_collisions(snake):
        game_over()
    else:
        window.after(SPEED, next_turn, snake, food)


def change_direction(new):
    global direction
    if new == "left" and direction != "right":
        direction = new
    elif new == "right" and direction != "left":
        direction = new
    elif new == "up" and direction != "down":
        direction = new
    elif new == "down" and direction != "up":
        direction = new


def check_collisions(snake):
    x, y = snake.coordinates[0]

    if [x, y] in walls:
        return True

    for part in snake.coordinates[1:]:
        if x == part[0] and y == part[1]:
            return True

    return False


def game_over():
    canvas.create_text(
        GAME_WIDTH // 2,
        GAME_HEIGHT // 2 - 40,
        text="GAME OVER",
        fill="red",
        font=("consolas", 60)
    )
    restart_button.place(x=GAME_WIDTH // 2 - 80, y=GAME_HEIGHT // 2)


def restart_game():
    global snake, food, score, direction, walls
    canvas.delete(ALL)
    score = 0
    direction = "down"
    walls = []

    label.config(text="Score: 0")
    restart_button.place_forget()

    create_walls()
    snake = Snake()
    food = Food()
    next_turn(snake, food)



window = Tk()
window.title("Snake Game")

score = 0
direction = "down"
walls = []

label = Label(window, text="Score: 0", font=("consolas", 40))
label.pack()

canvas = Canvas(
    window,
    bg=BACKGROUND_COLOR,
    width=GAME_WIDTH,
    height=GAME_HEIGHT,
    highlightthickness=0
)
canvas.pack()

restart_button = Button(
    window,
    text="Restart",
    font=("consolas", 20),
    command=restart_game
)

window.bind("<Left>", lambda e: change_direction("left"))
window.bind("<Right>", lambda e: change_direction("right"))
window.bind("<Up>", lambda e: change_direction("up"))
window.bind("<Down>", lambda e: change_direction("down"))

create_walls()
snake = Snake()
food = Food()
next_turn(snake, food)

window.mainloop()