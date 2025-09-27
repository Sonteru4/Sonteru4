#!/usr/bin/env python3
"""
README Updater for Tic-Tac-Toe Game
Replaces board anchors safely in README.md
"""

import os
import re
from typing import Optional

def update_readme_board(board: list, current_player: str, game_status: str, last_move: str = None) -> bool:
    """Update README with current game state"""
    readme_path = "README.md"
    
    # Read current README
    try:
        with open(readme_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: {readme_path} not found")
        return False
    
    # Find Tic-Tac-Toe section
    start_marker = "<!-- TTT-BOARD:START -->"
    end_marker = "<!-- TTT-BOARD:END -->"
    
    start_idx = content.find(start_marker)
    end_idx = content.find(end_marker)
    
    if start_idx == -1 or end_idx == -1:
        print("Error: Tic-Tac-Toe section markers not found in README")
        return False
    
    # Generate new board content
    from render import render_board
    new_board_content = render_board(board, current_player, game_status, last_move)
    
    # Replace the section
    new_content = (
        content[:start_idx + len(start_marker)] + 
        "\n" + new_board_content + "\n" + 
        content[end_idx:]
    )
    
    # Write updated README
    try:
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    except Exception as e:
        print(f"Error writing README: {e}")
        return False

def main():
    """Test the updater"""
    print("Testing README Updater")
    print("=" * 30)
    
    # Test with sample board
    board = ['X', 'O', '', 'X', 'O', '', '', '', '']
    current_player = 'X'
    game_status = "Waiting for X's move"
    last_move = "B2"
    
    success = update_readme_board(board, current_player, game_status, last_move)
    if success:
        print("README updated successfully")
    else:
        print("Failed to update README")

if __name__ == "__main__":
    main()