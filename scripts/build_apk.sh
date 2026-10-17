#!/usr/bin/env bash
# RB.AI - Flutter Release APK Build Script
set -e

echo "=== [RB.AI] Building Release APK ==="
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
FLUTTER_DIR="$SCRIPT_DIR/flutter_client"

if ! command -v flutter >/dev/null 2>&1; then
    echo "❌ Error: 'flutter' command not found."
    echo "💡 Note: On Termux/Android, compile the APK via the automated GitHub Actions workflow (.github/workflows/build_apk.yml) or run on any Linux/macOS/Windows desktop with Flutter SDK installed."
    exit 1
fi

cd "$FLUTTER_DIR"

echo "📦 Fetching Flutter dependencies..."
flutter pub get

echo "🔨 Compiling Android Release APK..."
flutter build apk --release --no-tree-shake-icons

APK_PATH="$FLUTTER_DIR/build/app/outputs/flutter-apk/app-release.apk"
if [ -f "$APK_PATH" ]; then
    echo "✅ Success! Release APK compiled at:"
    echo "   $APK_PATH"
else
    echo "⚠️ Build finished. Check output in $FLUTTER_DIR/build/app/outputs/flutter-apk/"
fi
