#!/usr/bin/env bash
# ==============================================================================
# DSA Note Taker - macOS .app Bundle Builder
# ==============================================================================
set -e

echo "🍏 Starting macOS .app build for DSA Note Taker..."

# Ensure we are in the desktop_app directory
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$DIR"

# 1. Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: python3 is not installed or not found in PATH."
    exit 1
fi

echo "🐍 Python version: $(python3 --version)"

# 2. Set up virtual environment
if [ ! -d "venv_build" ]; then
    echo "📦 Creating build virtual environment (venv_build)..."
    python3 -m venv venv_build
fi

source venv_build/bin/activate

# 3. Install required packages
echo "⬇️ Installing PyQt6 and PyInstaller..."
pip install --upgrade pip
pip install PyQt6 pyinstaller

# 4. Clean previous builds
echo "🧹 Cleaning old build artifacts..."
rm -rf build dist

# 5. Build the .app bundle with PyInstaller
echo "🔨 Compiling DSANoteTaker.app bundle..."
pyinstaller --clean DSANoteTaker.spec

# 6. Verify result
if [ -d "dist/DSANoteTaker.app" ]; then
    echo ""
    echo "=================================================================="
    echo "🎉 SUCCESS! Your macOS desktop app was created:"
    echo "   📍 $DIR/dist/DSANoteTaker.app"
    echo "=================================================================="
    echo ""
    echo "To test and launch the app right now:"
    echo "   open dist/DSANoteTaker.app"
    echo ""
    echo "To install it permanently in Applications:"
    echo "   cp -r dist/DSANoteTaker.app /Applications/"
    echo ""
else
    echo "❌ Build failed: dist/DSANoteTaker.app not found."
    exit 1
fi
