# Chess Game Architecture

## Project Structure Diagram

```mermaid
graph TB
    subgraph "Entry Point"
        Main[main.py<br/>GameController]
    end
    
    subgraph "Core Board Management"
        Board[board.py<br/>ChessBoard]
    end
    
    subgraph "Game Logic"
        GameState[game_logic/game_state.py<br/>GameStateValidator]
        MoveExec[game_logic/move_executor.py<br/>MoveExecutor]
    end
    
    subgraph "Pieces"
        Pieces[pieces.py<br/>Piece, Pawn, Rook<br/>Knight, Bishop<br/>Queen, King]
    end
    
    subgraph "UI Components"
        Renderer[ui/board_renderer.py<br/>BoardRenderer]
        InfoPanel[ui/info_panel.py<br/>InfoPanel, ControlPanel]
    end
    
    subgraph "Utilities"
        Notation[utils/notation.py<br/>NotationHelper]
        GameIO[utils/game_io.py<br/>GameSerializer]
        ImageMgr[utils/image_manager.py<br/>ImageManager]
    end
    
    subgraph "Constants"
        Constx[constx.py<br/>WHITE, BLACK<br/>CHECKMATE, etc.]
    end
    
    Main --> Board
    Main --> GameState
    Board --> MoveExec
    Board --> GameState
    Board --> Renderer
    Board --> InfoPanel
    Board --> Notation
    Board --> GameIO
    Board --> ImageMgr
    Board --> Pieces
    MoveExec --> Pieces
    GameState --> Pieces
    Renderer --> ImageMgr
    Renderer --> Pieces
    Pieces --> Constx
    Board --> Constx
    Main --> Constx
    
    style Main fill:#e1f5ff
    style Board fill:#fff4e1
    style GameState fill:#f0e1ff
    style MoveExec fill:#f0e1ff
    style Pieces fill:#ffe1e1
    style Renderer fill:#e1ffe1
    style InfoPanel fill:#e1ffe1
```

## Class Hierarchy

```mermaid
classDiagram
    class Piece {
        +str color
        +str name
        +float weight
        +int x, y
        +tuple position
        +bool has_moved
        +get_moves()
        +get_moves_without_check_validation()
        +would_leave_king_in_check()
        +update_position()
    }
    
    class Pawn {
        +get_attack_squares()
        +get_taking_squares()
        +get_moves()
    }
    
    class Rook {
        +get_moves()
    }
    
    class Knight {
        +get_moves_without_check_validation()
        +get_moves()
    }
    
    class Bishop {
        +get_moves()
    }
    
    class Queen {
        +get_moves()
    }
    
    class King {
        +is_square_attacked()
        +castling_moves()
        +get_moves()
    }
    
    Piece <|-- Pawn
    Piece <|-- Rook
    Piece <|-- Knight
    Piece <|-- Bishop
    Piece <|-- Queen
    Piece <|-- King
```

## Move Execution Flow

```mermaid
sequenceDiagram
    participant User
    participant GameController
    participant ChessBoard
    participant Piece
    participant MoveExecutor
    participant GameStateValidator
    participant BoardRenderer
    
    User->>GameController: Click piece
    GameController->>Piece: get_moves()
    Piece->>Piece: would_leave_king_in_check()
    Piece-->>GameController: valid_moves[]
    GameController->>BoardRenderer: Draw move indicators
    
    User->>GameController: Click target square
    GameController->>ChessBoard: move_piece(piece, x, y)
    ChessBoard->>MoveExecutor: execute_move()
    MoveExecutor->>MoveExecutor: Handle special moves
    MoveExecutor-->>ChessBoard: move_data
    ChessBoard->>ChessBoard: Handle promotion/capture
    ChessBoard->>GameStateValidator: check_game_state()
    GameStateValidator->>GameStateValidator: is_king_in_check()
    GameStateValidator->>GameStateValidator: get_all_legal_moves()
    GameStateValidator-->>ChessBoard: CHECKMATE/STALEMATE/IN_PROGRESS
    ChessBoard->>BoardRenderer: rerender()
    BoardRenderer-->>User: Updated board display
```

## Game State Detection Flow

```mermaid
flowchart TD
    Start[Move Made] --> SwitchTurn[Switch to Opponent]
    SwitchTurn --> GetMoves[Get All Legal Moves for Opponent]
    GetMoves --> HasMoves{Has Legal Moves?}
    
    HasMoves -->|Yes| InProgress[Game In Progress]
    HasMoves -->|No| CheckKing{Is King in Check?}
    
    CheckKing -->|Yes| Checkmate[CHECKMATE<br/>Current Player Wins]
    CheckKing -->|No| Stalemate[STALEMATE<br/>Draw]
    
    InProgress --> IsCheck{Is King in Check?}
    IsCheck -->|Yes| DisplayCheck[Display Check Indicator]
    IsCheck -->|No| Continue[Continue Game]
    
    DisplayCheck --> Continue
    Continue --> End[Wait for Next Move]
    Checkmate --> GameOver[Display Game Over Dialog]
    Stalemate --> GameOver
    
    style Checkmate fill:#ffcccc
    style Stalemate fill:#ffffcc
    style InProgress fill:#ccffcc
    style DisplayCheck fill:#ffddaa
```

## Check Validation Flow

```mermaid
flowchart TD
    Start[Player Selects Move] --> Simulate[Temporarily Execute Move]
    Simulate --> GetOpponent[Get Opponent's Pieces]
    GetOpponent --> CheckAttacks[Check if Any Piece Attacks King]
    
    CheckAttacks --> Loop{For Each<br/>Opponent Piece}
    Loop --> IsPawn{Is Pawn?}
    
    IsPawn -->|Yes| PawnAttack[Get Attack Squares]
    IsPawn -->|No| PieceAttack[Get Moves Without Validation]
    
    PawnAttack --> Contains{Contains<br/>King Position?}
    PieceAttack --> Contains
    
    Contains -->|Yes| InCheck[Move Leaves King in Check]
    Contains -->|No| Loop
    
    Loop -->|Done| NoCheck[Move is Legal]
    
    InCheck --> Restore[Restore Board State]
    NoCheck --> Restore
    
    Restore --> Return{Legal?}
    Return -->|Yes| AllowMove[Add to Valid Moves]
    Return -->|No| BlockMove[Remove from Valid Moves]
    
    AllowMove --> End[Return to Player]
    BlockMove --> End
    
    style InCheck fill:#ffcccc
    style NoCheck fill:#ccffcc
    style BlockMove fill:#ffaaaa
    style AllowMove fill:#aaffaa
```

## Special Moves Handling

```mermaid
flowchart TD
    Start[Execute Move] --> CheckSpecial{Special Move?}
    
    CheckSpecial -->|Castling| CheckCastling{King moves<br/>2 squares?}
    CheckSpecial -->|En Passant| CheckEnPassant{Pawn diagonal move<br/>to empty square?}
    CheckSpecial -->|Promotion| CheckPromotion{Pawn reaches<br/>back rank?}
    CheckSpecial -->|Normal| NormalMove[Execute Normal Move]
    
    CheckCastling -->|Yes| MoveCastling[Move King & Rook<br/>Mark both has_moved]
    CheckCastling -->|No| NormalMove
    
    CheckEnPassant -->|Yes| LastMove{Last move was<br/>pawn double push?}
    LastMove -->|Yes| CaptureEnPassant[Capture Pawn<br/>Mark as en passant]
    LastMove -->|No| NormalMove
    
    CheckPromotion -->|Yes| PromotionDialog[Show Promotion Dialog]
    CheckPromotion -->|No| NormalMove
    PromotionDialog --> ReplaceWithPiece[Replace Pawn with Chosen Piece]
    
    MoveCastling --> RecordMove[Record Move Data]
    CaptureEnPassant --> RecordMove
    ReplaceWithPiece --> RecordMove
    NormalMove --> RecordMove
    
    RecordMove --> UpdateHistory[Update Move History]
    UpdateHistory --> UpdateNotation[Generate Algebraic Notation]
    UpdateNotation --> End[Return Move Data]
    
    style MoveCastling fill:#e1f5ff
    style CaptureEnPassant fill:#ffe1f5
    style ReplaceWithPiece fill:#f5ffe1
    style NormalMove fill:#f0f0f0
```

## Data Flow Architecture

```mermaid
graph LR
    subgraph "Input Layer"
        Mouse[Mouse Click]
        Keyboard[Keyboard Input]
        FileLoad[Load Game File]
    end
    
    subgraph "Controller Layer"
        GameCtrl[GameController]
        EventHandler[Event Handler]
    end
    
    subgraph "Business Logic"
        Board[ChessBoard]
        Pieces[Piece Objects]
        Rules[Game Rules]
    end
    
    subgraph "Validation Layer"
        MoveValid[Move Validation]
        CheckValid[Check Detection]
        GameState[Game State Checker]
    end
    
    subgraph "Persistence Layer"
        MoveHistory[Move History]
        GameSave[Game Serializer]
    end
    
    subgraph "Presentation Layer"
        Renderer[Board Renderer]
        InfoUI[Info Panel]
        Dialogs[Dialogs]
    end
    
    Mouse --> EventHandler
    Keyboard --> EventHandler
    FileLoad --> GameCtrl
    
    EventHandler --> GameCtrl
    GameCtrl --> Board
    Board --> Pieces
    Board --> Rules
    
    Pieces --> MoveValid
    MoveValid --> CheckValid
    CheckValid --> GameState
    
    GameState --> MoveHistory
    Board --> GameSave
    
    GameState --> Renderer
    Board --> Renderer
    Board --> InfoUI
    GameCtrl --> Dialogs
    
    Renderer --> Display[Screen]
    InfoUI --> Display
    Dialogs --> Display
    
    style GameCtrl fill:#e1f5ff
    style Board fill:#fff4e1
    style MoveValid fill:#f0e1ff
    style Renderer fill:#e1ffe1
```

## Component Interaction Matrix

```mermaid
graph TD
    subgraph "High-Level Components"
        A[main.py] -->|creates| B[ChessBoard]
        A -->|manages| C[Game Loop]
    end
    
    subgraph "ChessBoard Dependencies"
        B -->|uses| D[BoardRenderer]
        B -->|uses| E[InfoPanel]
        B -->|uses| F[MoveExecutor]
        B -->|uses| G[GameStateValidator]
        B -->|uses| H[NotationHelper]
        B -->|uses| I[GameSerializer]
        B -->|uses| J[ImageManager]
    end
    
    subgraph "Core Logic Dependencies"
        F -->|manipulates| K[Piece Objects]
        G -->|validates| K
        D -->|renders| K
    end
    
    subgraph "Utility Dependencies"
        H -->|formats| L[Move Data]
        I -->|saves/loads| M[Game State]
        J -->|provides| N[Images]
    end
    
    K -->|reference| O[constx.py]
    L -->|uses| O
    M -->|uses| O
    
    style B fill:#ffd700
    style K fill:#ff6b6b
    style D fill:#4ecdc4
    style G fill:#95e1d3
```
