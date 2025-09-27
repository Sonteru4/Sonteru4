#!/usr/bin/env python3
"""
Tic-Tac-Toe Game Handler
Main handler for processing moves, updating README, and replying to comments
"""

import re
import sys
import argparse
import subprocess
from github import Github
from engine import TicTacToeEngine
from update_readme import update_readme_board

class TicTacToeGameHandler:
    """Handles Tic-Tac-Toe game interactions via GitHub issues"""
    
    def __init__(self, github_token: str, repo_name: str):
        self.github = Github(github_token)
        self.repo = self.github.get_repo(repo_name)
        self.engine = TicTacToeEngine()
    
    def extract_move_from_comment(self, comment_body: str) -> str:
        """Extract move from comment body (case-insensitive)"""
        pattern = r'/move\s+([A-Ca-c][1-3])'
        match = re.search(pattern, comment_body, re.IGNORECASE)
        return match.group(1).upper() if match else None
    
    def is_reset_command(self, comment_body: str) -> bool:
        """Check if comment contains reset command"""
        return '/reset' in comment_body.lower()
    
    def commit_changes(self, message: str) -> bool:
        """Commit changes with bot user"""
        try:
            subprocess.run(['git', 'config', 'user.name', 'Tic-Tac-Toe Bot'], check=True)
            subprocess.run(['git', 'config', 'user.email', 'bot@github.com'], check=True)
            subprocess.run(['git', 'add', '.'], check=True)
            subprocess.run(['git', 'commit', '-m', message], check=True)
            subprocess.run(['git', 'push'], check=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error committing changes: {e}")
            return False
    
    def handle_move(self, issue_number: int, commenter: str, move_str: str) -> bool:
        """Handle a move command"""
        # Apply the move
        success, message = self.engine.apply_move(move_str)
        
        if not success:
            # Invalid move - show valid moves
            valid_moves = self.engine.valid_moves()
            reply_message = f"❌ **{message}**\n\n"
            if valid_moves:
                reply_message += f"Available moves: {', '.join(valid_moves)}"
            else:
                reply_message += "No valid moves available."
            
            self.reply_to_comment(issue_number, reply_message)
            return False
        
        # Update README
        if not update_readme_board(
            self.engine.board, 
            self.engine.current_player, 
            self.engine.get_status(),
            self.engine.last_move
        ):
            print("Warning: Failed to update README")
        
        # Commit changes
        commit_message = f"chore(ttt): @{commenter} played {move_str}"
        if not self.commit_changes(commit_message):
            print("Warning: Failed to commit changes")
        
        # Prepare reply
        reply_message = f"✅ **{message}**\n\n"
        reply_message += self.engine.get_board_display()
        
        if self.engine.game_status == 'won':
            reply_message += f"\n🎉 **{self.engine.winner} wins!** Great game!"
            reply_message += "\n\n*Game over! Starting a new game...*"
            # Reset game after win
            self.engine.reset_game()
            update_readme_board(
                self.engine.board, 
                self.engine.current_player, 
                self.engine.get_status()
            )
            self.commit_changes("chore(ttt): Game reset after win")
        elif self.engine.game_status == 'draw':
            reply_message += "\n🤝 **It's a draw!** Well played!"
            reply_message += "\n\n*Game over! Starting a new game...*"
            # Reset game after draw
            self.engine.reset_game()
            update_readme_board(
                self.engine.board, 
                self.engine.current_player, 
                self.engine.get_status()
            )
            self.commit_changes("chore(ttt): Game reset after draw")
        else:
            reply_message += f"\n*Next player: {self.engine.current_player}*"
        
        self.reply_to_comment(issue_number, reply_message)
        return True
    
    def handle_reset(self, issue_number: int, commenter: str) -> bool:
        """Handle a reset command"""
        self.engine.reset_game()
        
        # Update README
        if not update_readme_board(
            self.engine.board, 
            self.engine.current_player, 
            self.engine.get_status()
        ):
            print("Warning: Failed to update README")
        
        # Commit changes
        commit_message = f"chore(ttt): @{commenter} reset game"
        if not self.commit_changes(commit_message):
            print("Warning: Failed to commit changes")
        
        # Reply with confirmation
        reply_message = f"🔄 **Game reset!** New game started by {commenter}\n\n"
        reply_message += self.engine.get_board_display()
        reply_message += "\n*Player X goes first!*"
        
        self.reply_to_comment(issue_number, reply_message)
        return True
    
    def reply_to_comment(self, issue_number: int, message: str):
        """Reply to the issue with a comment"""
        try:
            issue = self.repo.get_issue(issue_number)
            issue.create_comment(message)
        except Exception as e:
            print(f"Error creating comment: {e}")
    
    def process_comment(self, issue_number: int, comment_id: int, comment_body: str, commenter: str) -> bool:
        """Process a comment and handle the appropriate action"""
        
        # Check for reset command
        if self.is_reset_command(comment_body):
            return self.handle_reset(issue_number, commenter)
        
        # Check for move command
        move_str = self.extract_move_from_comment(comment_body)
        if move_str:
            return self.handle_move(issue_number, commenter, move_str)
        
        # No valid command found
        self.reply_to_comment(issue_number, 
            "❓ **Unknown command!** Use `/move A1` to play or `/reset` to start a new game.")
        return False

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='Handle Tic-Tac-Toe game moves')
    parser.add_argument('--issue-number', type=int, required=True)
    parser.add_argument('--comment-id', type=int, required=True)
    parser.add_argument('--comment-body', required=True)
    parser.add_argument('--commenter', required=True)
    parser.add_argument('--repo-name', required=True)
    
    args = parser.parse_args()
    
    # Get GitHub token
    github_token = sys.argv[1] if len(sys.argv) > 1 else None
    if not github_token:
        github_token = sys.environ.get('GITHUB_TOKEN')
    
    if not github_token:
        print("Error: No GitHub token provided")
        sys.exit(1)
    
    # Create handler and process comment
    handler = TicTacToeGameHandler(github_token, args.repo_name)
    success = handler.process_comment(
        args.issue_number,
        args.comment_id,
        args.comment_body,
        args.commenter
    )
    
    if success:
        print("Comment processed successfully")
    else:
        print("Failed to process comment")
        sys.exit(1)

if __name__ == "__main__":
    main()