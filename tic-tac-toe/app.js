/**
 * Tic-Tac-Toe Game Application
 * Features: 2-player mode, AI opponent, statistics tracking, accessibility
 */

class TicTacToeGame {
    constructor() {
        this.board = ['', '', '', '', '', '', '', '', ''];
        this.currentPlayer = 'X';
        this.gameMode = 'human'; // 'human' or 'ai'
        this.gameActive = true;
        this.winner = null;
        this.moveCount = 0;
        this.stats = this.loadStats();
        
        this.initializeElements();
        this.bindEvents();
        this.updateDisplay();
        this.animateBoard();
    }
    
    initializeElements() {
        this.cells = document.querySelectorAll('.cell');
        this.status = document.getElementById('gameStatus');
        this.resetBtn = document.getElementById('resetBtn');
        this.clearStatsBtn = document.getElementById('clearStatsBtn');
        this.gameModeSelect = document.getElementById('gameModeSelect');
        this.winsCount = document.getElementById('wins-count');
        this.lossesCount = document.getElementById('losses-count');
        this.drawsCount = document.getElementById('draws-count');
    }
    
    bindEvents() {
        this.cells.forEach(cell => {
            cell.addEventListener('click', (e) => this.handleCellClick(e));
            cell.addEventListener('keydown', (e) => this.handleKeyDown(e));
        });
        
        this.resetBtn.addEventListener('click', () => this.resetGame());
        this.clearStatsBtn.addEventListener('click', () => this.clearStats());
        this.gameModeSelect.addEventListener('change', (e) => this.changeGameMode(e.target.value));
        
        // Keyboard navigation
        document.addEventListener('keydown', (e) => this.handleGlobalKeyDown(e));
    }
    
    handleCellClick(event) {
        const cell = event.target;
        const index = parseInt(cell.dataset.index);
        
        if (this.board[index] !== '' || !this.gameActive) {
            return;
        }
        
        this.makeMove(index);
    }
    
    handleKeyDown(event) {
        if (event.key === 'Enter' || event.key === ' ') {
            event.preventDefault();
            this.handleCellClick(event);
        }
    }
    
    handleGlobalKeyDown(event) {
        // Number keys 1-9 for quick cell selection
        if (event.key >= '1' && event.key <= '9') {
            const index = parseInt(event.key) - 1;
            if (this.board[index] === '' && this.gameActive) {
                this.makeMove(index);
            }
        }
        
        // R key for reset
        if (event.key.toLowerCase() === 'r') {
            this.resetGame();
        }
    }
    
    makeMove(index) {
        this.board[index] = this.currentPlayer;
        this.moveCount++;
        
        const cell = this.cells[index];
        cell.textContent = this.currentPlayer;
        cell.classList.add(this.currentPlayer.toLowerCase());
        cell.setAttribute('aria-label', `${this.currentPlayer} in ${this.getCellName(index)}`);
        
        if (this.checkWinner()) {
            this.endGame(this.currentPlayer);
            return;
        }
        
        if (this.moveCount >= 9) {
            this.endGame(null);
            return;
        }
        
        this.currentPlayer = this.currentPlayer === 'X' ? 'O' : 'X';
        this.updateStatus();
        
        // AI move if in AI mode
        if (this.gameMode === 'ai' && this.currentPlayer === 'O' && this.gameActive) {
            this.makeAIMove();
        }
    }
    
    makeAIMove() {
        this.status.textContent = 'AI is thinking...';
        this.status.classList.add('ai-thinking');
        
        // Add delay for better UX
        setTimeout(() => {
            const bestMove = this.getBestMove();
            this.makeMove(bestMove);
        }, 500);
    }
    
    getBestMove() {
        // Simple AI: try to win, then block, then take center, then corners, then edges
        const board = this.board;
        
        // Check for winning move
        for (let i = 0; i < 9; i++) {
            if (board[i] === '') {
                board[i] = 'O';
                if (this.checkWinner()) {
                    board[i] = '';
                    return i;
                }
                board[i] = '';
            }
        }
        
        // Check for blocking move
        for (let i = 0; i < 9; i++) {
            if (board[i] === '') {
                board[i] = 'X';
                if (this.checkWinner()) {
                    board[i] = '';
                    return i;
                }
                board[i] = '';
            }
        }
        
        // Take center if available
        if (board[4] === '') return 4;
        
        // Take corners
        const corners = [0, 2, 6, 8];
        for (const corner of corners) {
            if (board[corner] === '') return corner;
        }
        
        // Take edges
        const edges = [1, 3, 5, 7];
        for (const edge of edges) {
            if (board[edge] === '') return edge;
        }
        
        return 0; // Fallback
    }
    
    checkWinner() {
        const winningCombinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8], // rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8], // columns
            [0, 4, 8], [2, 4, 6]             // diagonals
        ];
        
        for (const combination of winningCombinations) {
            const [a, b, c] = combination;
            if (this.board[a] && this.board[a] === this.board[b] && this.board[a] === this.board[c]) {
                this.highlightWinningCells(combination);
                return true;
            }
        }
        return false;
    }
    
    highlightWinningCells(combination) {
        combination.forEach(index => {
            this.cells[index].classList.add('winning');
        });
    }
    
    endGame(winner) {
        this.gameActive = false;
        this.winner = winner;
        
        if (winner) {
            this.status.textContent = `🎉 ${winner} wins!`;
            this.status.classList.add('winner');
            this.updateStats(winner);
        } else {
            this.status.textContent = "🤝 It's a draw!";
            this.status.classList.add('draw');
            this.updateStats('draw');
        }
        
        this.disableCells();
    }
    
    updateStats(result) {
        if (result === 'X') {
            this.stats.wins++;
        } else if (result === 'O' && this.gameMode === 'ai') {
            this.stats.losses++;
        } else if (result === 'draw') {
            this.stats.draws++;
        }
        
        this.saveStats();
        this.updateStatsDisplay();
    }
    
    updateStatsDisplay() {
        this.winsCount.textContent = this.stats.wins;
        this.lossesCount.textContent = this.stats.losses;
        this.drawsCount.textContent = this.stats.draws;
    }
    
    updateStatus() {
        if (this.gameMode === 'ai' && this.currentPlayer === 'O') {
            this.status.textContent = 'AI is thinking...';
            this.status.classList.add('ai-thinking');
        } else {
            this.status.textContent = `Player ${this.currentPlayer}'s turn`;
            this.status.classList.remove('ai-thinking');
        }
    }
    
    updateDisplay() {
        this.updateStatus();
        this.updateStatsDisplay();
    }
    
    disableCells() {
        this.cells.forEach(cell => {
            cell.disabled = true;
        });
    }
    
    enableCells() {
        this.cells.forEach(cell => {
            cell.disabled = false;
        });
    }
    
    resetGame() {
        this.board = ['', '', '', '', '', '', '', '', ''];
        this.currentPlayer = 'X';
        this.gameActive = true;
        this.winner = null;
        this.moveCount = 0;
        
        this.cells.forEach(cell => {
            cell.textContent = '';
            cell.className = 'cell';
            cell.setAttribute('aria-label', cell.getAttribute('aria-label').split(' in ')[0]);
        });
        
        this.status.textContent = `Player X's turn`;
        this.status.className = 'game-status';
        
        this.enableCells();
        this.updateDisplay();
        this.animateBoard();
    }
    
    changeGameMode(mode) {
        this.gameMode = mode;
        this.resetGame();
    }
    
    clearStats() {
        if (confirm('Are you sure you want to clear all statistics?')) {
            this.stats = { wins: 0, losses: 0, draws: 0 };
            this.saveStats();
            this.updateStatsDisplay();
        }
    }
    
    getCellName(index) {
        const positions = ['top left', 'top center', 'top right', 'middle left', 'center', 'middle right', 'bottom left', 'bottom center', 'bottom right'];
        return positions[index];
    }
    
    animateBoard() {
        this.cells.forEach((cell, index) => {
            cell.style.opacity = '0';
            cell.style.transform = 'scale(0.8)';
            setTimeout(() => {
                cell.style.transition = 'all 0.3s ease';
                cell.style.opacity = '1';
                cell.style.transform = 'scale(1)';
            }, index * 50);
        });
    }
    
    loadStats() {
        try {
            const saved = localStorage.getItem('ticTacToeStats');
            return saved ? JSON.parse(saved) : { wins: 0, losses: 0, draws: 0 };
        } catch (e) {
            return { wins: 0, losses: 0, draws: 0 };
        }
    }
    
    saveStats() {
        try {
            localStorage.setItem('ticTacToeStats', JSON.stringify(this.stats));
        } catch (e) {
            console.warn('Could not save statistics:', e);
        }
    }
}

// Initialize game when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new TicTacToeGame();
});

// Service Worker registration for offline support (optional)
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('/tic-tac-toe/sw.js')
            .then(registration => console.log('SW registered'))
            .catch(error => console.log('SW registration failed'));
    });
}
