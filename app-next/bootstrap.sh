#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

          DEFAULT_NVM_DIR="$HOME/.nvm"
ALT_NVM_DIR="$HOME/.config/nvm"
if [[ -n "${NVM_DIR:-}" && -s "${NVM_DIR}/nvm.sh" ]]; then
  RESOLVED_NVM_DIR="$NVM_DIR"
elif [[ -s "$DEFAULT_NVM_DIR/nvm.sh" ]]; then
  RESOLVED_NVM_DIR="$DEFAULT_NVM_DIR"
elif [[ -s "$ALT_NVM_DIR/nvm.sh" ]]; then
  RESOLVED_NVM_DIR="$ALT_NVM_DIR"
else
  RESOLVED_NVM_DIR="${NVM_DIR:-$DEFAULT_NVM_DIR}"
fi

REQUIRED_NODE_VERSION="$(tr -d '[:space:]' < .nvmrc)"
MODE="${1:-dev}"
LOG_FILE="$SCRIPT_DIR/bootstrap.log"

: > "$LOG_FILE"
log() {
  printf '%s\n' "$1" | tee -a "$LOG_FILE"
}

if [[ ! -s "$RESOLVED_NVM_DIR/nvm.sh" ]]; then
  log "nvm was not found at $RESOLVED_NVM_DIR/nvm.sh"
  log "Install nvm or load a Node.js runtime >= $REQUIRED_NODE_VERSION before running bootstrap.sh."
  exit 1
fi

export NVM_DIR="$RESOLVED_NVM_DIR"
# shellcheck disable=SC1090
. "$RESOLVED_NVM_DIR/nvm.sh"

if ! nvm use "$REQUIRED_NODE_VERSION" >/dev/null; then
  log "Node.js $REQUIRED_NODE_VERSION is not installed in nvm."
  log "Run: nvm install $REQUIRED_NODE_VERSION"
  exit 1
fi

log "Loading nvm from $RESOLVED_NVM_DIR/nvm.sh"
log "Using node $(node -v)"
log "Using npm $(npm -v)"
log "Running mode: $MODE"

case "$MODE" in
  dev)
    pkill -f "next dev" >/dev/null 2>&1 || true
    rm -rf .next
    npm install 2>&1 | tee -a "$LOG_FILE"
    npm run dev 2>&1 | tee -a "$LOG_FILE"
    ;;
  build)
    npm install 2>&1 | tee -a "$LOG_FILE"
    npm run build 2>&1 | tee -a "$LOG_FILE"
    ;;
  start)
    npm run start 2>&1 | tee -a "$LOG_FILE"
    ;;
  install)
    npm install 2>&1 | tee -a "$LOG_FILE"
    ;;
  *)
    log "Unknown mode: $MODE"
    log "Usage: ./bootstrap.sh [dev|build|start|install]"
    exit 1
    ;;
esac
