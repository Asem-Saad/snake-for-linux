# snake-for-linux

A terminal snake game for Linux. Pure Python 3 with the standard-library `curses` module, so there is nothing to install.

## Run

```sh
python3 snake.py
```

## Controls

| Key | Action |
|---|---|
| Arrow keys or `w` `a` `s` `d` | Steer |
| `p` | Pause |
| `q` or `Esc` | Quit |

Eat `*` to grow and score. The snake speeds up as you eat. Hitting a wall or yourself ends the game.

## Requirements

- Linux (or any Unix-like terminal with curses)
- Python 3.6+
- A terminal at least 20x10
