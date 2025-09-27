#!/usr/bin/env python3
"""
Tic-Tac-Toe Game Engine
Simplified engine with core functions: load_state, save_state, apply_move, winner, valid_moves
"""

import json
import os
from typing import List, Optional, Tuple

class TicTacToeEngine:
    """Simplified Tic-Tac-Toe engine with core functions"""
    
    def __init__(self, state_file: str = "tictactoe/state.json"):
        self.state_file = state_file
        self.board = [''] * 9  # 9 empty cells
        self.current_player = 'X'
        self.game_status = 'active'  # 'active', 'won', 'draw'
        self.winner = None
        self.move_count = 0
        self.last_move = None
        
        self.load_state()
    
    def load_state(self) -> None:
        """Load game state from JSON file"""
        try:
            if os.path.exists(self.state_file):
                with open(self.state_file, 'r') as f:
                    data = json.load(f)
                    self.board = data.get('board', [''] * 9)
                    self.current_player = data.get('currentPlayer', 'X')
                    self.game_status = data.get('gameStatus', 'active')
                    self.winner = data.get('winner')
                    self.move_count = data.get('moveCount', 0)
                    self.last_move = data.get('lastMove')
            else:
                self.reset_game()
        except (json.JSONDecodeError, KeyError):
            self.reset_game()
    
    def save_state(self) -> bool:
        """Save current game state to JSON file"""
        try:
            os.makedirs(os.path.dirname(self.state_file), exist_ok=True)
            data = {
                'board': self.board,
                'currentPlayer': self.current_player,
                'gameStatus': self.game_status,
                'winner': self.winner,
                'moveCount': self.move_count,
                'lastMove': self.last_move
            }
            with open(self.state_file, 'w') as f:
                json.dump(data, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving state: {e}")
            return False
    
    def parse_cell(self, cell: str) -> Optional[int]:
        """Parse cell string like 'A1', 'B2', 'C3' to board index (0-8)"""
        cell = cell.upper().strip()
        if len(cell) != 2:
            return None
        
        col = cell[0]
        row = cell[1]
        
        if col not in 'ABC' or row not in '123':
            return None
        
        col_idx = ord(col) - ord('A')  # A=0, B=1, C=2
        row_idx = int(row) - 1         # 1=0, 2=1, 3=2
        
        return row_idx * 3 + col_idx
    
    def valid_moves(self) -> List[str]:
        """Get list of valid move strings (A1, B2, etc.)"""
        valid = []
        for i in range(9):
            if self.board[i] == '':
                row = i // 3 + 1
                col = chr(ord('A') + i % 3)
                valid.append(f"{col}{row}")
        return valid
    
    def apply_move(self, cell: str) -> Tuple[bool, str]:
        """Apply a move and return (success, message)"""
        if self.game_status != 'active':
            return False, "Game is not active"
        
        position = self.parse_cell(cell)
        if position is None:
            return False, f"Invalid cell format. Use format like A1, B2, C3"
        
        if self.board[position] != '':
            valid_moves = self.valid_moves()
            return False, f"Cell {cell} is taken. Try one of: {', '.join(valid_moves)}"
        
        # Apply the move
        self.board[position] = self.current_player
        self.move_count += 1
        self.last_move = cell
        
        # Check for winner
        winner = self.check_winner()
        if winner:
            self.game_status = 'won'
            self.winner = winner
            self.save_state()
            return True, f"🎉 {self.current_player} wins!"
        
        # Check for draw
        if self.move_count >= 9:
            self.game_status = 'draw'
            self.winner = None
            self.save_state()
            return True, "🤝 It's a draw!"
        
        # Switch players
        self.current_player = 'O' if self.current_player == 'X' else 'X'
        self.save_state()
        
        return True, f"Move accepted! Next: {self.current_player}"
    
    def check_winner(self) -> Optional[str]:
        """Check for winner and return winning player or None"""
        winning_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # columns
            [0, 4, 8], [2, 4, 6]              # diagonals
        ]
        
        for combination in winning_combinations:
            if all(self.board[i] == self.current_player for i in combination):
                return self.current_player
        
        return None
    
    def reset_game(self) -> None:
        """Reset game to initial state"""
        self.board = [''] * 9
        self.current_player = 'X'
        self.game_status = 'active'
        self.winner = None
        self.move_count = 0
        self.last_move = None
        self.save_state()
    
    def get_board_display(self) -> str:
        """Get ASCII board display"""
        def format_cell(cell):
            return f"[{cell}]" if cell else "[ ]"
        
        return f"""```
   A   B   C
1 {format_cell(self.board[0])} {format_cell(self.board[1])} {format_cell(self.board[2])}
2 {format_cell(self.board[3])} {format_cell(self.board[4])} {format_cell(self.board[5])}  
3 {format_cell(self.board[6])} {format_cell(self.board[7])} {format_cell(self.board[8])}

Next: {self.current_player} | Status: {self.get_status()}
```"""
    
    def get_status(self) -> str:
        """Get current game status message"""
        if self.game_status == 'won':
            return f"🎉 {self.winner} wins!"
        elif self.game_status == 'draw':
            return "🤝 It's a draw!"
        else:
            return f"Waiting for {self.current_player}'s move..."

def main():
    """Test the engine"""
    print("Testing Tic-Tac-Toe Engine")
    print("=" * 30)
    
    engine = TicTacToeEngine()
    
    # Test moves
    success, message = engine.apply_move('A1')
    print(f"Move A1: {message}")
    
    success, message = engine.apply_move('B2')
    print(f"Move B2: {message}")
    
    success, message = engine.apply_move('A2')
    print(f"Move A2: {message}")
    
    success, message = engine.apply_move('C3')
    print(f"Move C3: {message}")
    
    success, message = engine.apply_move('A3')  # Should win
    print(f"Move A3: {message}")
    
    print(f"Final status: {engine.get_status()}")
    print(engine.get_board_display())

if __name__ == "__main__":
    main()