# Chess Game API Reference

## Overview
This document provides detailed API documentation for the chess game's core components.

## Class Diagram

```mermaid
classDiagram
    class GameController {
        +ChessBoard chessboard
        +str on_move
        +Piece current_piece
        +list possible_moves
        +set dots
        +__init__(root, board, canvas_size)
        +clicked(event)
        +clean_dots()
    }
    
    class ChessBoard {
        +list current_board
        +dict kings
        +list white_pieces
        +list black_pieces
        +int white_score
        +int black_score
        +tuple last_move
        +list move_history
        +BoardRenderer renderer
        +MoveExecutor move_executor
        +InfoPanel info_panel
        +__init__(master, board, pixel_size)
        +move_piece(piece, x, y)
        +is_king_in_check(color)
        +check_game_state(color)
        +undo_move_ui()
        +flip_board()
        +save_game()
        +load_game()
        +new_game()
    }
    
    class Piece {
        +str color
        +str name
        +float weight
        +int x
        +int y
        +tuple position
        +int image_id
        +bool has_moved
        +__init__(color, piece_notation, image_id, x, y)
        +is_valid(x, y, board, board_size)
        +can_take(x, y, board)
        +would_leave_king_in_check(x, y, board, board_size, kings)
        +get_moves(board, board_size, kings)
        +get_moves_without_check_validation(board, board_size)
        +update_position(x, y)
    }
    
    class BoardRenderer {
        +Canvas canvas
        +int square_size
        +int height
        +ImageManager image_manager
        +bool view_from_white
        +tuple selected_square_highlight
        +tuple last_move_highlight
        +draw_board(board, kings, is_king_in_check_fn)
        +create_move_indicator(x, y, indicator_type)
        +flip_board()
    }
    
    class MoveExecutor {
        +list board
        +execute_move(piece, x, y, last_move)
        +undo_move(move_data, pieces_notation)
    }
    
    class GameStateValidator {
        +is_king_in_check(board, board_size, kings, color)$
        +get_all_legal_moves(board, board_size, kings, pieces, color, last_move)$
        +check_game_state(board, board_size, kings, pieces, color, last_move)$
    }
    
    GameController --> ChessBoard
    ChessBoard --> BoardRenderer
    ChessBoard --> MoveExecutor
    ChessBoard --> GameStateValidator
    ChessBoard --> Piece
    MoveExecutor --> Piece
    GameStateValidator --> Piece
```

## Core Components

### GameController

Main game controller handling user interactions.

```mermaid
sequenceDiagram
    participant User
    participant GameController
    participant ChessBoard
    participant Piece
    
    User->>GameController: Click square
    GameController->>ChessBoard: Get piece at position
    ChessBoard-->>GameController: Piece object
    GameController->>Piece: get_moves()
    Piece-->>GameController: List of valid moves
    GameController->>ChessBoard: Draw move indicators
    
    User->>GameController: Click move target
    GameController->>ChessBoard: move_piece(piece, x, y)
    ChessBoard->>ChessBoard: Update board state
    ChessBoard->>ChessBoard: Check game state
    ChessBoard-->>GameController: Move completed
```

**Methods:**

- `__init__(root, board, canvas_size)` - Initialize game controller
- `clicked(event)` - Handle mouse click events
- `clean_dots()` - Remove move indicator dots

### ChessBoard

Central orchestrator managing game state and components.

```mermaid
flowchart LR
    A[ChessBoard] --> B[BoardRenderer]
    A --> C[MoveExecutor]
    A --> D[InfoPanel]
    A --> E[NotationHelper]
    A --> F[GameSerializer]
    A --> G[ImageManager]
    
    B --> H[Visual Display]
    C --> I[Move Logic]
    D --> J[UI Controls]
    E --> K[Notation]
    F --> L[Save/Load]
    G --> M[Images]
```

**Properties:**
- `current_board: list[list]` - 8x8 board representation
- `kings: dict` - Reference to both kings
- `white_pieces: list` - All white pieces
- `black_pieces: list` - All black pieces
- `white_score: int` - White's captured material
- `black_score: int` - Black's captured material
- `last_move: tuple` - Last move made (piece, from, to)
- `move_history: list[dict]` - Complete move history

**Key Methods:**

```python
def move_piece(piece: Piece, x: int, y: int) -> tuple:
    """
    Execute a move and return captured piece info
    
    Args:
        piece: The piece to move
        x: Target row
        y: Target column
    
    Returns:
        Captured piece (if any)
    """
```

```python
def is_king_in_check(color: str) -> bool:
    """
    Check if a king is in check
    
    Args:
        color: 'w' or 'b'
    
    Returns:
        True if king is in check
    """
```

```python
def check_game_state(color: str) -> str:
    """
    Determine current game state
    
    Args:
        color: Color to check
    
    Returns:
        CHECKMATE, STALEMATE, or IN_PROGRESS
    """
```

### Piece Classes

Base class and all piece types.

```mermaid
classDiagram
    class Piece {
        <<abstract>>
        +get_moves()*
        +would_leave_king_in_check()
    }
    
    class Pawn {
        +get_attack_squares()
        +get_taking_squares()
    }
    
    class Rook {
        +moves: [(±1,0), (0,±1)]
    }
    
    class Knight {
        +moves: L-shapes
    }
    
    class Bishop {
        +moves: [(±1,±1)]
    }
    
    class Queen {
        +moves: 8 directions
    }
    
    class King {
        +castling_moves()
        +is_square_attacked()
    }
    
    Piece <|-- Pawn
    Piece <|-- Rook
    Piece <|-- Knight
    Piece <|-- Bishop
    Piece <|-- Queen
    Piece <|-- King
```

## Usage Examples

### Create a new game

```python
import tkinter as tk
from main import GameController

root = tk.Tk()
root.title("Chess")

initial_board = [
    ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
    ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
    [".", ".", ".", ".", ".", ".", ".", "."],
    [".", ".", ".", ".", ".", ".", ".", "."],
    [".", ".", ".", ".", ".", ".", ".", "."],
    [".", ".", ".", ".", ".", ".", ".", "."],
    ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
    ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
]

game = GameController(root, initial_board, 800)
root.mainloop()
```

### Get legal moves for a piece

```python
from pieces import Knight
from constx import WHITE

knight = Knight(WHITE, 0, 7, 1)
board[7][1] = knight

legal_moves = knight.get_moves(board, 8, kings)
# Returns: [(5, 0), (5, 2), (6, 3)]
```
