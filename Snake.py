import pygame
import random
import os

from pygame.constants import KEYDOWN
pygame.init()

# Colors
white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)
purple = (153, 50, 204)

# Creating our Game Window
width = 1000
height = 600
gameWindow = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake")
pygame.display.update()
fps = 60

# Background Image
welcome_image = pygame.image.load("welcome.jpg")
bgimg = pygame.image.load("bg.jpg")
mainimg = pygame.image.load("main.png")
welcome_image = pygame.transform.scale(
    welcome_image, (width, height)).convert_alpha()
bgimg = pygame.transform.scale(bgimg, (width, height)).convert_alpha()
mainimg = pygame.transform.scale(mainimg, (width, height)).convert_alpha()

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 30)


def screen_score(text, color, x, y):
    screen_text = font.render(text, True, color)
    gameWindow.blit(screen_text, [x, y])


def plot_snake(gameWindow, col, snake_list, snake_size):
    for [x, y] in snake_list:
        pygame.draw.ellipse(
            gameWindow, col, [x, y, snake_size, snake_size])


def welcome():
    exit_game = False
    while not exit_game:
        gameWindow.fill(white)
        gameWindow.blit(welcome_image, (0, 0))
        screen_score("Welcome to Snake!", purple, 150, 100)
        screen_score("Press Enter to Play", purple, 150, 150)
        screen_score("By Priyanshi", purple, 150, 200)
        screen_score("Rules:", black, 120, 300)
        screen_score("Don't collide with walls", purple, 150, 350)
        screen_score("Don't collide with your body as well", purple, 150, 400)
        screen_score(
            "Score will be increased by 10 on eating food each time", purple, 150, 450)
        pygame.display.update()
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    game_loop()


def game_loop():
    exit_game = False
    game_over = False
    snake_x = 45
    snake_y = 55
    snake_size = 20
    food_x = random.randint(100, width-100)
    food_y = random.randint(200, height-100)
    velocity_x = 0
    velocity_y = 0
    score = 0
    highScore = 0
    # checking if Highscore file exists or not
    if not os.path.exists("HighScore.txt"):
        with open('HighScore.txt', 'w') as f:
            f.write("0")
        f.close()
    with open('HighScore.txt', 'r') as f:
        highScore = f.read()
    f.close()

    snake_list = []
    snake_length = 1

    while not exit_game:
        if game_over:
            with open('HighScore.txt', 'w') as f:
                f.write(str(highScore))
            f.close()
            gameWindow.fill(white)
            gameWindow.blit(bgimg, (0, 0))
            screen_score("Game Over! Press Enter to Restart.", black, 150, 200)
            screen_score("Your Score: "+str(score), black, 150, 250)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        game_loop()
                pygame.display.update()
                clock.tick(fps)

        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        velocity_x = 5
                        velocity_y = 0
                    if event.key == pygame.K_LEFT:
                        velocity_x = -5
                        velocity_y = 0
                    if event.key == pygame.K_UP:
                        velocity_x = 0
                        velocity_y = -5
                    if event.key == pygame.K_DOWN:
                        velocity_x = 0
                        velocity_y = 5
            snake_x = snake_x + velocity_x
            snake_y = snake_y + velocity_y

            if abs(food_x-snake_x) < 20 and abs(food_y-snake_y) < 20:
                score += 10
                food_x = random.randint(0, width/2)
                food_y = random.randint(0, height/2)
                snake_length += 5
                if(score > int(highScore)):
                    highScore = score

            gameWindow.fill(white)
            gameWindow.blit(mainimg, (0, 0))
            screen_score("Score: "+str(score)+"   HighScore: " +
                         str(highScore), black, 5, 5)
            pygame.draw.rect(gameWindow, black, [food_x, food_y, 15, 15])
            #print(food_x, food_y)

            head = []
            head.append(snake_x)
            head.append(snake_y)
            snake_list.append(head)

            if len(snake_list) > snake_length:
                del snake_list[0]

            if head in snake_list[:-1]:
                game_over = True

            if snake_x < 0 or snake_x > width or snake_y < 0 or snake_y > height:
                game_over = True

            plot_snake(gameWindow, purple, snake_list, snake_size)
        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    quit()


welcome()
