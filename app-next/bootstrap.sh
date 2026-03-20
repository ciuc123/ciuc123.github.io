#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

NVM_DIR="${NVM_DIR:-$HOME/.nvm}"
REQUIRED_NODE_VERSION="$(tr -d '[:space:]' < .nvmrc)"
MODE="${1:-dev}"

if [[ ! -s "$NVM_DIR/nvm.sh" ]]; then
  echo "nvm was not found at $NVM_DIR/nvm.sh" >&2
  echo "Install nvm or load a Node.js runtime >= $REQUIRED_NODE_VERSION before running bootstrap.sh." >&2
  exit 1
fi

# shellcheck disable=SC1090
. "$NVM_DIR/nvm.sh"

if ! nvm use "$REQUIRED_NODE_VERSION" >/dev/null 2>&1; then
  echo "Node.js $REQUIRED_NODE_VERSION is not installed in nvm." >&2
  echo "Run: nvm install $REQUIRED_NODE_VERSION" >&2
  exit 1
fi

echo "Using node $(node -v)"
echo "Using npm $(npm -v)"

case "$MODE" in
  dev)
    pkill -f "next dev" >/dev/null 2>&1 || true
    rm -rf .next
    npm install
    exec npm run dev
    ;;
  build)
    npm install
    exec npm run build
    ;;
  start)
    exec npm run start
    ;;
  install)
    exec npm install
    ;;
  *)
    echo "Unknown mode: $MODE" >&2
    echo "Usage: ./bootstrap.sh [dev|build|start|install]" >&2
    exit 1
    ;;
esac

