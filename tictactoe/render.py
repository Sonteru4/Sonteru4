#!/usr/bin/env python3
"""
Tic-Tac-Toe Board Renderer
Returns Markdown ASCII grid with A/B/C & 1/2/3 labels
"""

from typing import List

def render_board(board: List[str], current_player: str, game_status: str, last_move: str = None) -> str:
    """Render the complete board with status information"""
    
    def format_cell(cell):
        return f"[{cell}]" if cell else "[ ]"
    
    # Format each row
    row1 = f"1 {format_cell(board[0])} {format_cell(board[1])} {format_cell(board[2])}"
    row2 = f"2 {format_cell(board[3])} {format_cell(board[4])} {format_cell(board[5])}"
    row3 = f"3 {format_cell(board[6])} {format_cell(board[7])} {format_cell(board[8])}"
    
    # Create the board
    board_text = f"""```
   A   B   C
{row1}
{row2}
{row3}

Next: {current_player} | Status: {game_status}
```"""
    
    # Add last move info if available
    if last_move:
        board_text += f"\n*Last move: {last_move}*"
    
    return board_text

def main():
    """Test the renderer"""
    print("Testing Tic-Tac-Toe Renderer")
    print("=" * 30)
    
    # Test board
    board = ['X', 'O', '', 'X', 'O', '', '', '', '']
    current_player = 'X'
    game_status = "Waiting for X's move"
    last_move = "B2"
    
    result = render_board(board, current_player, game_status, last_move)
    print(result)

if __name__ == "__main__":
    main()