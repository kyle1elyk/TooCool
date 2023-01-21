import random
import pygame
from datetime import datetime

WINDOW_SIZE = 640
BORDER = 10

QUAD_SIZE = (WINDOW_SIZE - 4 * BORDER) / 2
SIZE_PADDING = QUAD_SIZE / 4

MARGIN = 8
SIZE = SIZE_PADDING - 2 * MARGIN
SQ_SIZE = (SIZE, SIZE)
HIGHLIGHT = 5
HIGHLIGHT_SIZE = (SIZE + 2 * HIGHLIGHT, SIZE + 2 * HIGHLIGHT)

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
move_count = 0

r_icon = pygame.image.load("r.png")
l_icon = pygame.image.load("l.png")


def main():
    board = [x for x in range(64)]
    random.shuffle(board)
    print_board(board)
    print()
    running = True
    won = False
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode([WINDOW_SIZE, WINDOW_SIZE])
    start = datetime.now()
    end = datetime.now()
    global move_count

    while running:
        do_move = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                do_move = True
                if won:
                    running = False

        if won:
            pygame.draw.rect(screen, WHITE, pygame.Rect(0, 0, 640, 640))
            font = pygame.font.Font(None, 25)
            text = font.render(f"You win! {move_count} moves in {end - start}", True, BLACK)
            text_rect = text.get_rect(center=(WINDOW_SIZE / 2, WINDOW_SIZE / 2))
            screen.blit(text, text_rect)

            pygame.display.update()
        else:
            (cur_x, cur_y) = pygame.mouse.get_pos()
            (x, y) = get_space(cur_x, cur_y)
            if x is not None and y is not None:
                move_horizontal = get_moves(board, x, y, True)
                move_vertical = get_moves(board, x, y, False)
                if do_move and pygame.mouse.get_pressed()[0] and move_horizontal is not None:
                    make_move(board, x, y, move_horizontal)
                    draw_screen(screen, board, None, cur_x, cur_y, x, y)
                    print_board(board)
                    won = game_check(board)
                elif do_move and pygame.mouse.get_pressed()[2] and move_vertical is not None:
                    make_move(board, x, y, move_vertical)
                    draw_screen(screen, board, None, cur_x, cur_y, x, y)
                    print_board(board)
                    won = game_check(board)
                else:
                    draw_screen(screen, board, [move_horizontal, move_vertical], cur_x, cur_y, x, y)

            else:
                draw_screen(screen, board, None, cur_x, cur_y, x, y)
            if won:
                end = datetime.now()

            # make_move(board, x, y, move)
            # print_board(board)
        clock.tick(60)


def game_check(board):
    for i in range(64):
        if get_color(board[i]) != get_color(i):
            # print(f"board[i]={board[i]}, i={i}, get_color(board[i])={get_color(board[i])}, get_color(i)={get_color(
            # i)}")
            return False
    return True


def get_space(cur_x, cur_y):
    if cur_x <= BORDER or cur_x >= WINDOW_SIZE - BORDER or cur_y <= BORDER or cur_y >= WINDOW_SIZE - BORDER:
        return None, None
    middle = WINDOW_SIZE / 2
    if -BORDER <= cur_x - middle <= BORDER or -BORDER <= cur_y - middle <= BORDER:
        return None, None

    xi = (cur_x - 3 * BORDER) if cur_x > middle else (cur_x - BORDER)
    yi = (cur_y - 3 * BORDER) if cur_y > middle else (cur_y - BORDER)

    z = QUAD_SIZE * 2
    return int(8 * xi / z), int(8 * yi / z)


def draw_screen(screen, board, moves, cur_x, cur_y, hover_x, hover_y):
    screen.fill((255, 255, 255))
    pygame.draw.rect(screen, RED, pygame.Rect(0, 0, 320, 320))
    pygame.draw.rect(screen, GREEN, pygame.Rect(320, 0, 320, 320))
    pygame.draw.rect(screen, BLUE, pygame.Rect(0, 320, 320, 320))
    pygame.draw.rect(screen, WHITE, pygame.Rect(320, 320, 320, 320))
    pygame.draw.rect(screen, WHITE, pygame.Rect(BORDER, BORDER, 640 - 2 * BORDER, 640 - 2 * BORDER))

    for y in range(8):
        for x in range(8):
            space = board[x + y * 8]
            x_quad_buf = 2 * BORDER if x > 3 else 0
            y_quad_buf = 2 * BORDER if y > 3 else 0

            color = get_color(space)
            pygame.draw.rect(screen, color_to_tup(color), pygame.Rect(
                (x * SIZE_PADDING + x_quad_buf + MARGIN + BORDER, y * SIZE_PADDING + y_quad_buf + MARGIN + BORDER),
                SQ_SIZE),
                             0 if color != "W" else 5)

    if moves and hover_x is not None and hover_y is not None:
        for move in moves:
            if hover_x is not None and hover_y is not None:
                x_quad_buf = 2 * BORDER if hover_x > 3 else 0
                y_quad_buf = 2 * BORDER if hover_y > 3 else 0

                pygame.draw.rect(screen, (111, 139, 214), pygame.Rect(
                    (hover_x * SIZE_PADDING + x_quad_buf + MARGIN + BORDER - HIGHLIGHT,
                     hover_y * SIZE_PADDING + y_quad_buf + MARGIN + BORDER - HIGHLIGHT),
                    HIGHLIGHT_SIZE), 2 * HIGHLIGHT)

            if move is not None:
                right = move[1][0] > 3
                bottom = move[1][1] > 3

                x_quad_buf = 2 * BORDER if right else 0
                y_quad_buf = 2 * BORDER if bottom else 0

                if hover_y == move[1][1]:
                    icon = l_icon
                    # horizontal
                    icon_rel_x = SIZE_PADDING if right else -SIZE_PADDING
                    icon_rel_y = 0
                else:
                    icon = r_icon
                    # vertical
                    icon_rel_x = 0
                    icon_rel_y = SIZE_PADDING if bottom else -SIZE_PADDING

                pygame.draw.rect(screen, (111, 214, 214), pygame.Rect(
                    (move[1][0] * SIZE_PADDING + x_quad_buf + MARGIN + BORDER - HIGHLIGHT,
                     move[1][1] * SIZE_PADDING + y_quad_buf + MARGIN + BORDER - HIGHLIGHT),
                    HIGHLIGHT_SIZE), 2 * HIGHLIGHT)

                screen.blit(icon,
                            (hover_x * SIZE_PADDING + x_quad_buf + MARGIN + BORDER + icon_rel_x,
                             hover_y * SIZE_PADDING + y_quad_buf + MARGIN + BORDER + icon_rel_y))
    pygame.display.update()


def print_board(board):
    print("\r\n" + color_to_emoji("R") + "0 1 2 3  4 5 6 7 " + color_to_emoji("G"))
    for y in range(8):
        # print(" ".join("[" + get_color(n) + "(%02d)]" % n for n in board[y * 8:y * 8 + 8]))
        y_row = [color_to_emoji(get_color(n)) for n in board[y * 8:y * 8 + 8]]
        print(str(y) + " " + "".join(y_row[:4]) + " " + "".join(y_row[4:]))
        if y == 3:
            print()
    print(color_to_emoji("B") + "                 " + color_to_emoji("W"))


def get_color(piece_num):
    right = piece_num % 8 <= 3
    top = piece_num < 32
    if top:
        if right:
            return "R"
        else:
            return "G"
    else:
        if right:
            return "B"
        else:
            return "W"


def color_to_emoji(color):
    return {
        "G": "🟩",
        "R": "🟥",
        "W": "🟨",
        "B": "🟦"
    }[color]


def color_to_tup(color):
    return {
        "R": RED,
        "G": GREEN,
        "B": BLUE,
        "W": (0, 0, 0)
    }[color]


def get_piece_num(board, x, y):
    return board[x + y * 8]


def get_moves(board, x, y, horizontal):
    piece_num = get_piece_num(board, x, y)
    top = y <= 3
    left = x <= 3
    if horizontal:
        if left:
            row = board[4 + y * 8: 8 + y * 8]
            coors = [[xi, y] for xi in range(4, 8)]
        else:
            row = board[y * 8: 4 + y * 8][::-1]
            coors = [[xi, y] for xi in range(3, -1, -1)]

    else:
        if top:
            row = board[32 + x: 32 + x + 8 * 4: 8]
            coors = [[x, yi] for yi in range(4, 8)]
        else:
            row = board[x: x + 8 * 4: 8][::-1]
            coors = [[x, yi] for yi in range(3, -1, -1)]

    # print("\r\n" + "".join(color_to_emoji(get_color(n)) for n in row))

    possibles = [[row[i], coors[i]] for i in range(4)]
    # print(possibles)
    return next((target_piece for target_piece in possibles if get_color(target_piece[0]) != get_color(piece_num)),
                None)


def make_move(board, x, y, move):
    global move_count
    move_count = move_count + 1
    print(
        f"{color_to_emoji(get_color(board[x + y * 8]))} {x},{y} to {color_to_emoji(get_color(board[move[1][0] + move[1][1] * 8]))} {move[1][0]},{move[1][1]}")
    board[move[1][0] + move[1][1] * 8] = board[x + y * 8]
    board[x + y * 8] = move[0]


if __name__ == "__main__":
    main()
