#!/usr/bin/env bash
set -euo pipefail

REPO_URL="${RUPYTHON_REPO_URL:-https://github.com/PanMax13/RuPython.git}"
INSTALL_DIR="${RUPYTHON_HOME:-$HOME/.rupython}"
BIN_DIR="${RUPYTHON_BIN_DIR:-$HOME/.local/bin}"
COMMAND_PATH="$BIN_DIR/rupython"
PATH_LINE="export PATH=\"$BIN_DIR:\$PATH\""
PATH_MARKER="# RuPython PATH"

detect_shell_profile() {
  if [ -n "${RUPYTHON_PROFILE:-}" ]; then
    echo "$RUPYTHON_PROFILE"
    return
  fi

  case "${SHELL:-}" in
    */zsh)
      echo "$HOME/.zshrc"
      ;;
    */bash)
      if [ "$(uname -s)" = "Darwin" ]; then
        echo "$HOME/.bash_profile"
      else
        echo "$HOME/.bashrc"
      fi
      ;;
    *)
      echo "$HOME/.profile"
      ;;
  esac
}

ensure_path_in_profile() {
  if command -v rupython >/dev/null 2>&1; then
    return
  fi

  case ":$PATH:" in
    *":$BIN_DIR:"*)
      return
      ;;
  esac

  profile_path="$(detect_shell_profile)"
  touch "$profile_path"

  if ! grep -F "$PATH_LINE" "$profile_path" >/dev/null 2>&1; then
    {
      echo ""
      echo "$PATH_MARKER"
      echo "$PATH_LINE"
    } >> "$profile_path"
  fi

  echo "Добавил $BIN_DIR в PATH через $profile_path"
}

if ! command -v git >/dev/null 2>&1; then
  echo "Ошибка: для установки нужен git." >&2
  exit 1
fi

if ! command -v python3 >/dev/null 2>&1; then
  echo "Ошибка: для запуска RuPython нужен python3." >&2
  exit 1
fi

mkdir -p "$BIN_DIR"

if [ -d "$INSTALL_DIR/.git" ]; then
  echo "Обновляю существующую установку в $INSTALL_DIR"
  git -C "$INSTALL_DIR" pull --ff-only
elif [ -e "$INSTALL_DIR" ]; then
  echo "Ошибка: $INSTALL_DIR уже существует, но это не git-репозиторий." >&2
  exit 1
else
  echo "Устанавливаю RuPython в $INSTALL_DIR"
  git clone "$REPO_URL" "$INSTALL_DIR"
fi

chmod +x "$INSTALL_DIR/rupython"
ln -sfn "$INSTALL_DIR/rupython" "$COMMAND_PATH"
ensure_path_in_profile

echo "RuPython установлен: $COMMAND_PATH"

if ! command -v rupython >/dev/null 2>&1; then
  echo "Откройте новый терминал или выполните:"
  echo "  $PATH_LINE"
fi
