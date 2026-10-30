#!/usr/bin/env python3
"""Terminal snake game for Linux, built on the standard-library curses module."""

import curses
import random
import time

TICK = 0.12  # seconds per move at the start
MIN_TICK = 0.05
SPEEDUP = 0.002  # seconds shaved off each tick per food eaten

DIRECTIONS = {
    curses.KEY_UP: (-1, 0),
    curses.KEY_DOWN: (1, 0),
    curses.KEY_LEFT: (0, -1),
    curses.KEY_RIGHT: (0, 1),
    ord("w"): (-1, 0),
    ord("s"): (1, 0),
    ord("a"): (0, -1),
    ord("d"): (0, 1),
}


def place_food(snake, height, width):
    free = [
        (y, x)
        for y in range(1, height - 1)
        for x in range(1, width - 1)
        if (y, x) not in snake
    ]
    return random.choice(free) if free else None


def draw_border(win, height, width):
    win.border()
    win.addstr(0, 2, " SNAKE ")


def play(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.keypad(True)

    height, width = stdscr.getmaxyx()
    if height < 10 or width < 20:
        raise SystemExit("Terminal too small: need at least 20x10.")

    snake = [(height // 2, width // 2 - i) for i in range(3)]
    direction = (0, 1)
    food = place_food(snake, height, width)
    score = 0
    tick = TICK
    paused = False

    while True:
        deadline = time.monotonic() + tick
        pending = direction
        while time.monotonic() < deadline:
            key = stdscr.getch()
            if key in (ord("q"), 27):
                return score
            if key == ord("p"):
                paused = not paused
            if key in DIRECTIONS:
                new = DIRECTIONS[key]
                # Ignore a reversal into the snake's own neck.
                if (new[0] + direction[0], new[1] + direction[1]) != (0, 0):
                    pending = new
            time.sleep(0.005)
        if paused:
            stdscr.addstr(0, width - 10, " PAUSED ")
            stdscr.refresh()
            continue
        direction = pending

        head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
        hit_wall = not (0 < head[0] < height - 1 and 0 < head[1] < width - 1)
        if hit_wall or head in snake:
            return score

        snake.insert(0, head)
        if head == food:
            score += 1
            tick = max(MIN_TICK, tick - SPEEDUP)
            food = place_food(snake, height, width)
            if food is None:  # board is full: you win
                return score
        else:
            snake.pop()

        stdscr.erase()
        draw_border(stdscr, height, width)
        stdscr.addstr(0, width - 14, f" Score: {score} ")
        if food:
            stdscr.addstr(food[0], food[1], "*")
        for i, (y, x) in enumerate(snake):
            stdscr.addstr(y, x, "O" if i == 0 else "o")
        stdscr.refresh()


def main():
    score = curses.wrapper(play)
    print(f"Game over! Score: {score}")


if __name__ == "__main__":
    main()
