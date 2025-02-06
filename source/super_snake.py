import pygame
import sys
import random
from time import sleep


# draw the game to the screen
def draw_screen(screen, position: list, apples: list, length: int, this_frame: int, direction: str, grew: bool, font, background) -> None:
    this_frame = this_frame - 8

    # draw background
    draw_background(screen, background)

    # draw scoreboard
    draw_scoreboard(screen, font, length)

    # draw snake body
    draw_snake_body(screen, position)

    # draw head of snake
    draw_snake_head(screen, direction, position, this_frame)

    # draw apple(s)
    draw_apples(screen, apples)

    # draw back of the snake
    if not grew:
        draw_snake_end(screen, position, this_frame)


def draw_snake_end(screen, position: list, this_frame: int) -> None:
    back_direction = ''
    back = position[-2:]
    x1, y1 = back[0]
    x2, y2 = back[1]

    if y1 < y2:
        back_direction = 'u'
    elif y1 > y2:
        back_direction = 'd'
    elif x1 < x2:
        back_direction = 'l'
    elif x1 > x2:
        back_direction = 'r'

    if back_direction == 'u':
        pygame.draw.rect(screen, (5, 165, 245),
                         pygame.Rect(back[0][0] * 40, (back[0][1]) * 40 + 200 - this_frame * 5, 40, 40))
    elif back_direction == 'd':
        pygame.draw.rect(screen, (5, 165, 245),
                         pygame.Rect(back[0][0] * 40, (back[0][1]) * 40 + 200 + this_frame * 5, 40, 40))
    elif back_direction == 'l':
        pygame.draw.rect(screen, (5, 165, 245),
                         pygame.Rect((back[0][0]) * 40 - this_frame * 5, back[0][1] * 40 + 200, 40, 40))
    elif back_direction == 'r':
        pygame.draw.rect(screen, (5, 165, 245),
                         pygame.Rect((back[0][0]) * 40 + this_frame * 5, back[0][1] * 40 + 200, 40, 40))


def draw_snake_head(screen, direction: str, position: list, this_frame: int) -> None:
    if direction == 'u':
        pygame.draw.rect(screen, (5, 165, 245),
                         pygame.Rect(position[0][0] * 40, position[0][1] * 40 + 200 - 5 * this_frame, 40, 40))
        pygame.draw.rect(screen, (2, 102, 232),
                         pygame.Rect(position[0][0] * 40, position[0][1] * 40 + 200 - 5 * this_frame, 40, 40))

    elif direction == 'd':
        pygame.draw.rect(screen, (5, 165, 245),
                         pygame.Rect(position[0][0] * 40, position[0][1] * 40 + 200 + 5 * this_frame, 40, 40))
        pygame.draw.rect(screen, (2, 102, 232),
                         pygame.Rect(position[0][0] * 40, position[0][1] * 40 + 200 + 5 * this_frame, 40, 40))

    elif direction == 'l':
        pygame.draw.rect(screen, (5, 165, 245),
                         pygame.Rect(position[0][0] * 40 - 5 * this_frame, position[0][1] * 40 + 200, 40, 40))
        pygame.draw.rect(screen, (2, 102, 232),
                         pygame.Rect(position[0][0] * 40 - 5 * this_frame, position[0][1] * 40 + 200, 40, 40))

    elif direction == 'r':
        pygame.draw.rect(screen, (5, 165, 245),
                         pygame.Rect(position[0][0] * 40 + 5 * this_frame, position[0][1] * 40 + 200, 40, 40))
        pygame.draw.rect(screen, (2, 102, 232),
                         pygame.Rect(position[0][0] * 40 + 5 * this_frame, position[0][1] * 40 + 200, 40, 40))
    # pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(position[0][0] * 40, position[0][1] * 40 + 200, 40, 40), 2)


def draw_apples(screen, apples: list) -> None:
    for apple in apples:
        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(apple[0] * 40, apple[1] * 40 + 200, 40, 40))


def draw_snake_body(screen, position: list) -> None:
    # draw snake body
    for body in position[1:-1]:
        pygame.draw.rect(screen, (5, 165, 245), pygame.Rect(body[0] * 40, body[1] * 40 + 200, 40, 40))


def draw_scoreboard(screen, font, length: int) -> None:
    pygame.draw.rect(screen, (0, 164, 5), pygame.Rect(0, 0, 800, 200))
    score_text = font.render(f"Score: {length * 10 - 30}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))


def draw_background(screen, background) -> None:
    screen.blit(background, (0, 200))


def move_snake_main(position: list, direction: str, length: int) -> tuple:

    # don't move if the snake is standing still
    if direction == '':
        return False, position

    # move in the direction the snake is facing
    else:
        # move current segments forwards
        temp_position = move_snake_move(direction, position)
        # add segment if the snake can grow
        grow, temp_position = move_snake_grow(length, position, temp_position.copy())
        # return if the snake grew and new snake position list
        return grow, temp_position


def move_snake_move(direction: str, position: list) -> list:
    temp_position = []
    if direction == 'u':
        temp_position.append([position[0][0], position[0][1] - 1])
    if direction == 'd':
        temp_position.append([position[0][0], position[0][1] + 1])
    if direction == 'l':
        temp_position.append([position[0][0] - 1, position[0][1]])
    if direction == 'r':
        temp_position.append([position[0][0] + 1, position[0][1]])
    return temp_position


def move_snake_grow(length: int, position: list, this_temp_position: list) -> tuple:
    if len(position) < length:
        this_temp_position += position
        grow = True
    else:
        this_temp_position += position[:-1]
        grow = False
    return grow, this_temp_position


def check_collision(position: list, apples: list) -> int:
    snake_head = position[0]

    for apple in apples:
        if snake_head == apple:
            return 2

    for snake_body in position[1:]:
        if snake_body == snake_head:
            return 1

    if snake_head[0] < 0 or snake_head[0] > 19:
        return 1
    elif snake_head[1] < 0 or snake_head[1] > 19:
        return 1

    return 0


def apple_spawn(position: list, apples: list) -> list:
    invalid_positions = position + apples
    apples.remove(position[0])

    while True:
        new_apple = [random.randint(0, 19), random.randint(0, 19)]
        if new_apple not in invalid_positions:
            apples.append(new_apple)
            return apples


def end_game():  # TODO make the end of the game
    sleep(3)
    pygame.quit()
    sys.exit()


def main(screen, fps, snake_position, snake_length, apple_position, move_direction, last_direction, bg_img, frame_count):
    # set up game loop variables
    clock = pygame.time.Clock()
    running = True
    # set text font
    text_font = pygame.font.Font('freesansbold.ttf', 36)
    # main game loop
    while running:
        # handle events
        for event in pygame.event.get():

            # close game
            if event.type == pygame.QUIT:
                running = False

            # key press events
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if last_direction != 'd':
                        move_direction = 'u'
                if event.key == pygame.K_LEFT:
                    if last_direction != 'r':
                        move_direction = 'l'
                if event.key == pygame.K_DOWN:
                    if last_direction != 'u':
                        move_direction = 'd'
                if event.key == pygame.K_RIGHT:
                    if last_direction != 'l':
                        move_direction = 'r'

        if frame_count == 1:
            # move snake and display screen
            snake_grow, snake_position = move_snake_main(snake_position, move_direction, snake_length)
            last_direction = move_direction

            collision = check_collision(snake_position, apple_position)
            if collision != 0:
                if collision == 1:
                    end_game()
                elif collision == 2:
                    snake_length += 1
                    apple_position = apple_spawn(snake_position, apple_position.copy())

        draw_screen(screen, snake_position, apple_position, snake_length, frame_count, last_direction, snake_grow, text_font, bg_img)

        if frame_count == 8:
            frame_count = 1
        else:
            frame_count += 1

        # Refresh the display
        pygame.display.flip()

        # control the frame rate
        clock.tick(fps)

    # quit Pygame
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    # initialize Pygame
    pygame.init()

    # set up display
    width, height = 800, 1000
    main_screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Super Snake")

    # create variables
    main_fps = 60
    snake_pos = [[6, 10], [5, 10]]  # list containing coordinates of snake body locations in lists
    snake_len = 3  # length of snake
    apple_pos = [[14, 10]]  # list containing coordinates of apple location in lists
    move_dir = 'r'  # the direction the snake is facing
    last_dir = 'l'  # the last direction that the snake has moved in
    bg = pygame.image.load("Super_Snake_bg.png")  # load background image
    frame = 1

    # run main function
    main(main_screen, main_fps, snake_pos, snake_len, apple_pos, move_dir, last_dir, bg, frame)
