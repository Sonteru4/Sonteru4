# Profile README Revamp + Playable Tic-Tac-Toe

## 🎯 Overview

This PR completely revamps the GitHub profile README with a modern, high-signal design and implements two interactive Tic-Tac-Toe experiences:

1. **GitHub Pages Game** (`/tic-tac-toe/`) - Instant play with AI opponent
2. **Issue-Based Game** - Turn-based gameplay via GitHub issue comments

## ✨ New Features

### Modern README Design
- **Punchy tagline**: "I build production ML/AI systems and ruthless automations. I mentor, podcast, and ship. If it compounds, I care."
- **Updated social links**: LinkedIn, Buy Me A Coffee, Medium, Personal Website
- **Professional layout** with badges, current projects, selected work, and tech stack
- **Clear CTAs** for mentorship and contact

### GitHub Pages Game (`/tic-tac-toe/`)
- **Separate files**: `index.html`, `style.css`, `app.js` as requested
- **AI opponent** with smart strategy (win, block, center, corners, edges)
- **2-player toggle** for human vs AI or 2-player mode
- **Statistics tracking** with localStorage persistence
- **Full accessibility** with keyboard navigation and ARIA labels
- **Mobile responsive** design with modern animations
- **Favicon** with game emoji (SVG)

### Issue-Based Turn-Based Game (`tictactoe/`)
- **Modular architecture**: `engine.py`, `render.py`, `update_readme.py`, `game_handler.py`
- **State management** with `state.json` for persistent game state
- **Pure game logic** with win/draw detection
- **ASCII board rendering** with A-C columns, 1-3 rows
- **README integration** with `<!-- TTT-BOARD:START -->` and `<!-- TTT-BOARD:END -->` markers
- **GitHub Actions** workflow for processing `/move` and `/reset` commands
- **Automatic commits** with bot user and descriptive messages
- **Smart replies** with board snapshots and game status

## 🛠️ Technical Implementation

### File Structure
```
/
├── README.md                          # Updated with TTT section
├── tic-tac-toe/                       # GitHub Pages game
│   ├── index.html                     # Main game page
│   ├── style.css                      # Game styles
│   ├── app.js                         # Game logic with AI
│   ├── favicon.svg                    # Game favicon
│   └── README.md                      # Game documentation
├── tictactoe/                         # Issue-based game engine
│   ├── state.json                     # Game state storage
│   ├── engine.py                      # Pure game logic
│   ├── render.py                      # ASCII board renderer
│   ├── update_readme.py               # README updater
│   └── game_handler.py                # GitHub integration
├── .github/
│   ├── workflows/
│   │   ├── deploy-pages.yml           # GitHub Pages deployment
│   │   └── tictactoe.yml              # Issue game handler
│   └── ISSUE_TEMPLATE/
│       └── play-tictactoe.md          # Issue template
├── assets/
│   ├── social-card.svg                # Social preview image
│   └── social-card.png                # Social preview placeholder
└── requirements.txt                   # Python dependencies
```

### Key Components

#### GitHub Pages Game (`tic-tac-toe/`)
- **HTML**: Semantic structure with ARIA labels
- **CSS**: Modern design with gradients, animations, and responsive layout
- **JavaScript**: Game logic, AI opponent, statistics, accessibility

#### Issue-Based Game (`tictactoe/`)
- **`engine.py`**: Core functions - `load_state()`, `save_state()`, `apply_move()`, `check_winner()`, `valid_moves()`
- **`render.py`**: ASCII board rendering for README display
- **`update_readme.py`**: README integration with section markers
- **`game_handler.py`**: GitHub API integration for issue comments

#### GitHub Actions
- **`deploy-pages.yml`**: Uses `actions/deploy-pages` for GitHub Pages
- **`tictactoe.yml`**: Processes issue comments and updates README

## 🚀 Setup Instructions

### 1. Enable GitHub Pages
1. Go to repository **Settings** → **Pages**
2. Set **Source** to "GitHub Actions"
3. The workflow will automatically deploy on push to main

### 2. Create Pinned Issue
1. Go to **Issues** tab
2. Click **New issue**
3. Select **"🎮 Play Tic-Tac-Toe"** template
4. Create the issue
5. **Pin the issue** (click the pin icon)

### 3. Test the Implementation
- **GitHub Pages**: Visit `https://yourusername.github.io/yourrepo/tic-tac-toe/`
- **Issue Game**: Comment `/move A1` on the pinned issue
- **Reset**: Comment `/reset` to start new game

## 🎮 Game Features

### GitHub Pages Game
- **vs AI Mode**: Intelligent opponent that tries to win and block
- **2-Player Mode**: Local multiplayer on same device
- **Statistics**: Wins, losses, draws tracked in localStorage
- **Keyboard Support**: Number keys 1-9 for quick moves, R for reset
- **Animations**: Smooth hover effects and win highlighting
- **Responsive**: Works on desktop, tablet, and mobile

### Issue-Based Game
- **Turn-Based**: Comment `/move A1` to play (A1-C3 positions)
- **Persistent State**: Game continues between comments
- **Automatic Updates**: README board updates after each move
- **Win Detection**: Automatic win/draw detection and notifications
- **Reset Support**: Comment `/reset` to start new game
- **Public Play**: Anyone can join and play

## 🔧 Configuration

### Update Repository References
In `tictactoe/game_handler.py`, the repository name is automatically detected from the GitHub context.

### Update Issue Links
In `README.md`, update the issue link:
```markdown
Comment `/move A1` (or B2, C3, etc.) on [this pinned issue](https://github.com/YOURUSERNAME/YOURREPO/issues/1) to play!
```

## 🐛 Troubleshooting

### GitHub Pages Not Working
- Check Actions tab for deployment status
- Verify `deploy-pages.yml` workflow is enabled
- Ensure repository has Pages permission

### Issue Game Not Working
- Check Actions tab for failed workflows
- Verify `tictactoe.yml` workflow is enabled
- Ensure repository has write permissions
- Check if pinned issue exists

### Board Not Updating
- Verify README has `<!-- TTT-BOARD:START -->` and `<!-- TTT-BOARD:END -->` markers
- Check Python script permissions
- Verify GitHub Actions logs

## 📊 Testing Results

- ✅ **Engine Logic**: All game logic tested and working
- ✅ **Renderer**: ASCII board generation working correctly
- ✅ **README Integration**: Section markers and updates working
- ✅ **GitHub Actions**: Workflows configured and ready
- ✅ **Accessibility**: Keyboard navigation and ARIA labels implemented
- ✅ **Mobile Design**: Responsive layout tested

## 🎯 Features Summary

- ✅ **Dual Game Experience**: Both immediate play and turn-based
- ✅ **AI Opponent**: Smart AI that tries to win and block
- ✅ **Statistics Tracking**: Persistent win/loss/draw tracking
- ✅ **Accessibility**: Full keyboard navigation and ARIA labels
- ✅ **Mobile Responsive**: Works on all devices
- ✅ **Automated Updates**: GitHub Actions handle all game logic
- ✅ **Modern Design**: Clean, professional, engaging
- ✅ **Social Integration**: Links to profiles and projects
- ✅ **Mentoring Focus**: Clear CTA for mentorship opportunities

---

**Ready to deploy! 🚀**

The implementation is production-ready with comprehensive documentation, setup guides, error handling, and testing. Both Tic-Tac-Toe experiences will provide engaging ways for visitors to interact with your profile while showcasing your technical skills in automation, GitHub Actions, and modern web development!
