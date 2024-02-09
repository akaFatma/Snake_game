import random
import pygame

class Snake:  #stores data about current location and where is the snake heading
    def __init__(self, init_body, init_direction):
        self.body = init_body
        self.direction = init_direction

    def take_step(self, position):  #add this position to the front of the snake’s body, and pop off the back position
        self.body = self.body[1:] + [position]

    def set_direction(self, direction):
        self.direction = direction

    def head(self):
        return self.body[-1]


class Apple:
    def __init__(self, location):
        self.location = location


class Game:
    EMPTY = 0
    HEAD = 1
    BODY = 2
    APPLE = 3

    DISPLAY_CHARS = {
        EMPTY: ' ',
        HEAD: "X",
        BODY: "O",
        APPLE: "*",
    }

    DIRECT_UP = (0, 1)
    DIRECT_DOWN = (0, -1)
    DIRECT_LEFT = (-1, 0)
    DIRECT_RIGHT = (1, 0)

    INPUT_UP = "z"
    INPUT_DOWN = "s"
    INPUT_RIGHT = "d"
    INPUT_LEFT = "q"

    def __init__(self, width, height):
        self.height = height
        self.width = width
        init_body = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0)]
        self.snake = Snake(init_body, self.DIRECT_UP)
        self.generate_apple()

    def generate_apple(self):
        # generate a new apple location that is not in the snake's body
        while True:
            new_apple_loc = (
                random.randint(0, self.width - 1),
                random.randint(0, self.height - 1),
            )
            if new_apple_loc not in self.snake.body:
                break
        self.current_apple = Apple(new_apple_loc)

    def next_position(self, position, step):
        
        return (
            (position[0] + step[0]) % self.width,
            (position[1] + step[1]) % self.height
        )

    def extend_body(self, position):
        self.snake.body.append(position)

    def play(self):
        
        self.render()
        while True:
           
            ch = input("")
            if ch == self.INPUT_UP and self.snake.direction != self.DIRECT_DOWN:
                self.snake.set_direction(self.DIRECT_UP)
            elif ch == self.INPUT_LEFT and self.snake.direction != self.DIRECT_RIGHT:
                self.snake.set_direction(self.DIRECT_LEFT)
            elif ch == self.INPUT_RIGHT and self.snake.direction != self.DIRECT_LEFT:
                self.snake.set_direction(self.DIRECT_RIGHT)
            elif ch == self.INPUT_DOWN and self.snake.direction != self.DIRECT_UP:
                self.snake.set_direction(self.DIRECT_DOWN)

            #the next position of the snake
            next_position = self.next_position(self.snake.head(), self.snake.direction)

            # Check if snake dakhla f roha xd
            if next_position in self.snake.body:
                break

            
            if next_position == self.current_apple.location:
                self.extend_body(next_position)
                self.generate_apple()
            else:
                self.snake.take_step(next_position)

            # Render the updated game state
            self.render()

    def board_matrix(self):
       #this is the board
        matrix = [[self.EMPTY for _ in range(self.height)] for _ in range(self.width)]
        for co in self.snake.body:
            matrix[co[0]][co[1]] = self.BODY

        head = self.snake.head()
        matrix[head[0]][head[1]] = self.HEAD

        apple_loc = self.current_apple.location
        matrix[apple_loc[0]][apple_loc[1]] = self.APPLE

        return matrix

    def render(self):
        matrix = self.board_matrix()

        top_and_bottom_border = "+" + "-" * self.width + "+"

        print(top_and_bottom_border)
        for y in range(0, self.height):
            line = "|"
            for x in range(0, self.width):
                cell_val = matrix[x][self.height - 1 - y]
                line += self.DISPLAY_CHARS[cell_val]
            line += "|"
            print(line)
        print(top_and_bottom_border)



game = Game(50, 50)
game.play()
