#!/usr/bin/env python3
"""
Tic-Tac-Toe Game Handler for GitHub Issues
Handles /move commands and updates the README with ASCII board
"""

import re
import sys
import argparse
from github import Github
from typing import Dict, List, Optional, Tuple

class TicTacToeGame:
    def __init__(self):
        self.board = [' '] * 9
        self.current_player = 'X'
        self.game_over = False
        self.winner = None
        self.move_count = 0
        
    def reset(self):
        """Reset the game to initial state"""
        self.board = [' '] * 9
        self.current_player = 'X'
        self.game_over = False
        self.winner = None
        self.move_count = 0
    
    def make_move(self, position: int) -> bool:
        """Make a move at the given position (0-8)"""
        if self.game_over or self.board[position] != ' ':
            return False
            
        self.board[position] = self.current_player
        self.move_count += 1
        
        if self.check_winner():
            self.game_over = True
            self.winner = self.current_player
        elif self.move_count >= 9:
            self.game_over = True
        else:
            self.current_player = 'O' if self.current_player == 'X' else 'X'
            
        return True
    
    def check_winner(self) -> bool:
        """Check if current player has won"""
        winning_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # columns
            [0, 4, 8], [2, 4, 6]              # diagonals
        ]
        
        for combo in winning_combinations:
            if all(self.board[i] == self.current_player for i in combo):
                return True
        return False
    
    def get_board_ascii(self) -> str:
        """Generate ASCII representation of the board"""
        def format_cell(cell):
            return f"[{cell}]" if cell != ' ' else "[ ]"
        
        return f"""```
   A   B   C
1 {format_cell(self.board[0])} {format_cell(self.board[1])} {format_cell(self.board[2])}
2 {format_cell(self.board[3])} {format_cell(self.board[4])} {format_cell(self.board[5])}  
3 {format_cell(self.board[6])} {format_cell(self.board[7])} {format_cell(self.board[8])}

Next: {self.current_player} | Status: {self.get_status()}
```"""
    
    def get_status(self) -> str:
        """Get current game status"""
        if self.winner:
            return f"🎉 {self.winner} wins!"
        elif self.game_over:
            return "🤝 It's a draw!"
        else:
            return f"Waiting for {self.current_player}'s move..."
    
    def from_ascii(self, ascii_board: str):
        """Parse game state from ASCII board"""
        lines = ascii_board.strip().split('\n')
        if len(lines) < 4:
            return
            
        # Extract board state from ASCII
        board_line_1 = lines[1]  # 1 [X] [O] [ ]
        board_line_2 = lines[2]  # 2 [ ] [X] [ ]
        board_line_3 = lines[3]  # 3 [ ] [ ] [O]
        
        def extract_cell(line, pos):
            # Extract cell content from "[X]" or "[ ]" format
            start = line.find('[', pos)
            if start == -1:
                return ' '
            end = line.find(']', start)
            if end == -1:
                return ' '
            cell = line[start+1:end].strip()
            return cell if cell else ' '
        
        # Parse board
        self.board = [
            extract_cell(board_line_1, 0),  # A1
            extract_cell(board_line_1, 1),  # B1
            extract_cell(board_line_1, 2),  # C1
            extract_cell(board_line_2, 0),  # A2
            extract_cell(board_line_2, 1),  # B2
            extract_cell(board_line_2, 2),  # C2
            extract_cell(board_line_3, 0),  # A3
            extract_cell(board_line_3, 1),  # B3
            extract_cell(board_line_3, 2),  # C3
        ]
        
        # Parse status line
        status_line = lines[-1] if lines else ""
        if "wins" in status_line:
            self.winner = 'X' if 'X' in status_line else 'O'
            self.game_over = True
        elif "draw" in status_line:
            self.game_over = True
        else:
            # Extract current player from status
            if "Next: X" in status_line:
                self.current_player = 'X'
            elif "Next: O" in status_line:
                self.current_player = 'O'
        
        # Count moves
        self.move_count = sum(1 for cell in self.board if cell != ' ')

def parse_move(move_str: str) -> Optional[int]:
    """Parse move string like 'A1', 'B2', 'C3' to board index (0-8)"""
    move_str = move_str.upper().strip()
    
    if len(move_str) != 2:
        return None
        
    col = move_str[0]
    row = move_str[1]
    
    if col not in 'ABC' or row not in '123':
        return None
    
    col_idx = ord(col) - ord('A')  # A=0, B=1, C=2
    row_idx = int(row) - 1         # 1=0, 2=1, 3=2
    
    return row_idx * 3 + col_idx

def extract_move_from_comment(comment_body: str) -> Optional[str]:
    """Extract move from comment body"""
    # Look for /move A1, /move B2, etc.
    pattern = r'/move\s+([A-C][1-3])'
    match = re.search(pattern, comment_body, re.IGNORECASE)
    return match.group(1) if match else None

def update_readme_board(github_token: str, repo_name: str, new_board_ascii: str):
    """Update the README with new board state"""
    g = Github(github_token)
    repo = g.get_repo(repo_name)
    
    # Read current README
    readme_content = repo.get_contents("README.md").decoded_content.decode()
    
    # Find and replace the board section
    start_marker = "<!-- TIC-TAC-TOE-BOARD-START -->"
    end_marker = "<!-- TIC-TAC-TOE-BOARD-END -->"
    
    start_idx = readme_content.find(start_marker)
    end_idx = readme_content.find(end_marker)
    
    if start_idx == -1 or end_idx == -1:
        print("Could not find board markers in README")
        return False
    
    # Replace the board content
    new_content = (
        readme_content[:start_idx + len(start_marker)] + 
        "\n" + new_board_ascii + "\n" +
        readme_content[end_idx:]
    )
    
    # Update README
    repo.update_file(
        path="README.md",
        message="🎮 Update Tic-Tac-Toe board",
        content=new_content,
        sha=repo.get_contents("README.md").sha
    )
    
    return True

def handle_reset(github_token: str, repo_name: str, issue_number: int, commenter: str):
    """Handle /reset command"""
    g = Github(github_token)
    repo = g.get_repo(repo_name)
    
    # Reset board to initial state
    game = TicTacToeGame()
    new_board_ascii = game.get_board_ascii()
    
    # Update README
    if update_readme_board(github_token, repo_name, new_board_ascii):
        print("README reset successfully")
    else:
        print("Failed to reset README")
        return False
    
    # Reply to comment
    issue = repo.get_issue(issue_number)
    issue.create_comment(
        f"🔄 **Game reset!** New game started by {commenter}\n\n{new_board_ascii}\n\n*Player X goes first!*"
    )
    
    return True

def main():
    parser = argparse.ArgumentParser(description='Handle Tic-Tac-Toe moves')
    parser.add_argument('--issue-number', type=int, required=True)
    parser.add_argument('--comment-id', type=int, required=True)
    parser.add_argument('--comment-body', required=True)
    parser.add_argument('--commenter', required=True)
    
    args = parser.parse_args()
    
    github_token = sys.argv[1] if len(sys.argv) > 1 else None
    if not github_token:
        github_token = sys.environ.get('GITHUB_TOKEN')
    
    if not github_token:
        print("No GitHub token provided")
        sys.exit(1)
    
    # Check for reset command
    if '/reset' in args.comment_body.lower():
        if handle_reset(github_token, "Sonteru4/Sonteru4", args.issue_number, args.commenter):
            print("Game reset successfully")
        else:
            print("Failed to reset game")
        sys.exit(0)
    
    # Extract move from comment
    move_str = extract_move_from_comment(args.comment_body)
    if not move_str:
        print("No valid move found in comment")
        sys.exit(0)
    
    # Parse move to board index
    move_idx = parse_move(move_str)
    if move_idx is None:
        print(f"Invalid move format: {move_str}")
        sys.exit(0)
    
    # Initialize GitHub client
    g = Github(github_token)
    repo = g.get_repo("Sonteru4/Sonteru4")
    
    # Get current README to extract game state
    readme_content = repo.get_contents("README.md").decoded_content.decode()
    
    # Find current board state
    start_marker = "<!-- TIC-TAC-TOE-BOARD-START -->"
    end_marker = "<!-- TIC-TAC-TOE-BOARD-END -->"
    
    start_idx = readme_content.find(start_marker)
    end_idx = readme_content.find(end_marker)
    
    if start_idx == -1 or end_idx == -1:
        print("Could not find board markers in README")
        sys.exit(1)
    
    # Extract current board ASCII
    board_section = readme_content[start_idx + len(start_marker):end_idx].strip()
    
    # Initialize game with current state
    game = TicTacToeGame()
    if board_section:
        game.from_ascii(board_section)
    
    # Make the move
    if not game.make_move(move_idx):
        # Invalid move - reply to comment
        issue = repo.get_issue(args.issue_number)
        issue.create_comment(
            f"❌ **Invalid move!** Position {move_str} is already taken or game is over.\n\n"
            f"Current board:\n{game.get_board_ascii()}"
        )
        sys.exit(0)
    
    # Update README with new board
    new_board_ascii = game.get_board_ascii()
    if update_readme_board(github_token, "Sonteru4/Sonteru4", new_board_ascii):
        print("README updated successfully")
    else:
        print("Failed to update README")
        sys.exit(1)
    
    # Reply to comment with result
    issue = repo.get_issue(args.issue_number)
    
    if game.winner:
        response = f"🎉 **{game.winner} wins!** Great game!\n\n{new_board_ascii}\n\n*Game over! Start a new game by commenting `/reset`*"
    elif game.game_over:
        response = f"🤝 **It's a draw!** Well played!\n\n{new_board_ascii}\n\n*Game over! Start a new game by commenting `/reset`*"
    else:
        response = f"✅ **Move accepted!** {move_str} played by {args.commenter}\n\n{new_board_ascii}\n\n*Next player: {game.current_player}*"
    
    issue.create_comment(response)
    print("Comment posted successfully")

if __name__ == "__main__":
    main()
