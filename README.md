# Chess Game in Python

A fully-featured chess game implementation in Python with Tkinter GUI, supporting all standard chess rules including special moves, check/checkmate detection, and game management features.

### UI Features

- **Visual highlights**
- **Score tracking**
- **Move history**
- **Board flipping**
- **Control panel**
- **Undo moves**
- **Algebraic notation**

- **New game**
- **Save/Load games** - JSON format for easy game preservation

## Project Structure

```
chess-py/
├── game_logic/              # Core game logic
│   ├── game_state.py       # Check, checkmate, stalemate detection
│   └── move_executor.py    # Move execution and undo functionality
├── ui/                      # User interface components
│   ├── board_renderer.py   # Board drawing and visual management
│   └── info_panel.py       # Score display, move history, controls
├── utils/                   # Utility modules
│   ├── notation.py         # Algebraic notation conversion
│   ├── game_io.py          # Save/load and PGN export
│   └── image_manager.py    # Image loading and scaling
├── pieces/                  # PNG images for all pieces
│   ├── black/              # Black piece images
│   └── white/              # White piece images
├── main.py                  # Application entry point
├── board.py                 # Main chess board class
├── pieces.py                # Chess piece classes and move logic
└── constx.py                # Constants and helper functions
```

### Start

```bash
cd chess-py
python3 main.py
```

## Architecture

### Design Principles

- **Separation of concerns** - Game logic, UI, and utilities are cleanly separated
- **Modular design** - Each module has a single, well-defined responsibility
- **MVC-inspired** - Board state (model), rendering (view), and game controller
- **Type hints** - Clear function signatures throughout

### Key Classes

#### `ChessBoard` (board.py)

Main orchestrator that coordinates all components:

- Manages game state (board, pieces, scores)
- Coordinates between renderer, move executor, and UI
- Handles user interactions and callbacks

#### `Piece` and subclasses (pieces.py)

Chess piece implementations with move generation:

- `get_moves()` - Returns all legal moves considering checks
- `get_moves_without_check_validation()` - Raw move generation for attack detection
- `would_leave_king_in_check()` - Simulates moves to validate legality

#### `BoardRenderer` (ui/board_renderer.py)

Handles all visual rendering:

- Square coloring with highlights
- Piece drawing with proper positioning
- Board flipping logic

#### `GameStateValidator` (game_logic/game_state.py)

Core chess rule enforcement:

- Check detection
- Checkmate/stalemate detection
- Legal move enumeration

#### `MoveExecutor` (game_logic/move_executor.py)

Move execution and reversal:

- Handles special moves (castling, en passant, promotion)
- Maintains move history
- Complete undo support

### Move Validation Flow

1. User selects a piece
2. `piece.get_moves()` generates candidate moves
3. For each move, `would_leave_king_in_check()` simulates it
4. Only moves that don't leave the king in check are shown
5. After move execution, opponent's legal moves are checked
6. If no legal moves exist, check for checkmate vs stalemate

## File Formats

### Save Game Format (JSON)

```json
{
  "board": [
    [{"name": "bR", "has_moved": false}, ...],
    ...
  ],
  "move_history": ["e4", "e5", "Nf3", ...],
  "white_score": 3,
  "black_score": 0
}
```

### PGN Export

The `export_pgn()` function in `utils/game_io.py` can export games to standard PGN format.

## Development

### Adding New Features

The modular structure makes it easy to extend:

- **New UI elements** → Add to `ui/` directory
- **Game logic changes** → Modify `game_logic/` modules
- **Move validation** → Update `pieces.py`
- **File formats** → Extend `utils/game_io.py`

## License

This project is open source and available for educational purposes.
