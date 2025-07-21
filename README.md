# Grid Escape Game 🎮

A strategic two-player grid-based escape game built with Pygame.

[![Build Executables](https://github.com/egemertgulderen/grid-escape-game/actions/workflows/build-executables.yml/badge.svg)](https://github.com/egemertgulderen/grid-escape-game/actions/workflows/build-executables.yml)

## 🎯 Game Overview

Grid Escape is a turn-based strategy game where two players compete to move their pawns across the board and escape from the opposite side.

### Features:
- 🎲 7x7 grid board with designated spawn and exit points
- 👥 Two players: Blue (bottom→top) and Red (right→left)  
- 🧠 Strategic pawn placement and movement
- 🏆 Victory achieved by escaping all pawns

## 🎮 How to Play

### Game Flow:
1. **Place Pawns**: Click on your starting positions (circles) to place pawns
2. **Move Pawns**: Click on a pawn, then click where you want to move it
3. **Escape**: When a pawn reaches an exit point (arrows), click it again to escape
4. **Win**: First player to escape all 7 pawns wins!

### Player Rules:
- 🔵 **Blue Player**: Starts bottom row → escapes top row (moves upward only)
- 🔴 **Red Player**: Starts right column → escapes left column (moves leftward only)

## 🎮 Controls

- **🖱️ Mouse Click**: Select and move pawns
- **R Key**: Restart the game
- **ESC Key**: Deselect a pawn

## 📥 Download & Play

### Ready-to-Play Executables

Download the latest version for your system:

- **Windows**: [GridEscape-Windows.exe](https://github.com/egemertgulderen/grid-escape-game/releases/latest/download/GridEscape-Windows.exe)
- **macOS**: [GridEscape-macOS](https://github.com/egemertgulderen/grid-escape-game/releases/latest/download/GridEscape-macOS)
- **Linux**: [GridEscape-Linux](https://github.com/egemertgulderen/grid-escape-game/releases/latest/download/GridEscape-Linux)

### How to Run:
- **Windows**: Double-click the `.exe` file
- **macOS**: Double-click the file (right-click → "Open" if security warning appears)
- **Linux**: Make executable (`chmod +x GridEscape-Linux`) then run (`./GridEscape-Linux`)

## 🛠️ Development

### Running from Source
```bash
# Install dependencies
pip install pygame

# Run the game
python pygame_grid_escape/main.py
```

### Building Executables
The executables are automatically built using GitHub Actions. See [GITHUB_SETUP_GUIDE.md](GITHUB_SETUP_GUIDE.md) for setup instructions.

## 📋 System Requirements

- **Windows**: Windows 7 or later
- **macOS**: macOS 10.12 or later  
- **Linux**: Most modern distributions
- **RAM**: 100 MB minimum
- **Storage**: 50 MB free space

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🎮 Screenshots

*Game screenshots would go here*

---

**Enjoy playing Grid Escape! 🎉**