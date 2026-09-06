# Caro Game (Gomoku) - Python Tkinter Implementation

A simple implementation of the Caro game (also known as Gomoku or Five in a Row) using Python and Tkinter. Play against an AI opponent on a 15x15 board.

## Features

- Classic Caro/Gomoku gameplay on a 15x15 board
- Play as 'O' (human) vs AI as 'X'
- Simple AI that evaluates positions to make strategic moves
- Visual feedback with colored pieces (blue for human, red for AI)
- Restart button to play again
- Win/draw detection with popup messages
- Responsive GUI with smooth animations

## Requirements

- Python 3.x
- Tkinter (usually comes pre-installed with Python on most systems)

## How to Run

1. Clone or download this repository
2. Navigate to the project directory
3. Run the game:

```bash
python caro_game.py
```

## How to Play

- You play as the blue 'O' pieces
- Click on any empty cell to place your piece
- The AI (red 'X') will automatically make its move after yours
- First player to get 5 of their pieces in a row (horizontally, vertically, or diagonally) wins
- If the board fills up without a winner, the game ends in a draw
- Click "Chơi lại" (Play Again) to start a new game

## AI Difficulty

The AI uses a simple evaluation function that:
- Prioritizes creating lines of 4 or more pieces
- Attempts to block the player's potential winning moves
- Considers both offensive and defensive positions
- Adds a small delay (0.3 seconds) to simulate "thinking" for better user experience

## Files

- `caro_game.py`: Main game implementation

## Screenshots

*(Add screenshots here if available)*

## Contributing

Feel free to submit issues or pull requests if you'd like to improve the game!

## License

This project is open source and available under the [MIT License](LICENSE).

---

Enjoy playing Caro!