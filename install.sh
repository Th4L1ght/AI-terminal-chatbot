#!/bin/bash

set -e

SCRIPT_NAME="ai_shell_agent.py"
INSTALL_DIR="$HOME/.ai_shell"
BIN_PATH="/usr/local/bin/aish"

echo "Installazione AI Shell Agent..."

# 1. Crea directory
mkdir -p "$INSTALL_DIR"

# 2. Copia lo script
if [ -f "$SCRIPT_NAME" ]; then
    cp "$SCRIPT_NAME" "$INSTALL_DIR/"
    echo "Script copiato in $INSTALL_DIR"
else
    echo "Errore: il file $SCRIPT_NAME non esiste nella directory corrente."
    exit 1
fi

# 3. Crea wrapper eseguibile
WRAPPER="$INSTALL_DIR/aish"
echo -e '#!/bin/bash\npython3 ~/.ai_shell/ai_shell_agent.py "$@"' > "$WRAPPER"
chmod +x "$WRAPPER"

# 4. Collegamento simbolico
sudo ln -sf "$WRAPPER" "$BIN_PATH"
echo "Collegamento creato: puoi usare il comando 'aish'"

# 5. Controlla se Ollama è installato
if ! command -v ollama &> /dev/null; then
    echo "Ollama non è installato. Vuoi installarlo ora? [y/n]"
    read -r ollama_reply
    if [[ "$ollama_reply" == "y" ]]; then
        curl -fsSL https://ollama.com/install.sh | sh
        echo "Ollama installato. Ora puoi fare: ollama pull mistral"
    else
        echo "Puoi installarlo manualmente da https://ollama.com"
    fi
fi

echo "Installazione completata! Digita 'aish' per avviare l'assistente."
