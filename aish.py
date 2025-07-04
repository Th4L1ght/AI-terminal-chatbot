import subprocess
import sys
import datetime
import os

# 🚨 Lista di comandi considerati sensibili
DANGEROUS_KEYWORDS = [
    "rm", "shutdown", "reboot", "mkfs", "dd", ":(){", ">:",
    "kill", "wget", "curl", "nmap", "netcat", "nc", "iptables"
]

LOG_FILE = os.path.expanduser("~/.ai_shell/ai_command_log.txt")

def log_command(prompt, command):
    with open(LOG_FILE, "a") as f:
        f.write(f"[{datetime.datetime.now()}] Prompt: {prompt}\n")
        f.write(f"Command: {command}\n\n")

def is_dangerous(command):
    return any(word in command for word in DANGEROUS_KEYWORDS)

def generate_command(prompt):
    system_prompt = (
        "Sei un assistente esperto della shell. Genera solo il comando bash più efficace per:\n"
        f"{prompt}\n\n"
        "Rispondi solo con il comando, senza spiegazioni."
    )

    try:
        result = subprocess.run(
            ["ollama", "run", "mistral"],
            input=system_prompt,
            text=True,
            capture_output=True
        )
        return result.stdout.strip()
    except FileNotFoundError:
        print("❌ Errore: assicurati che Ollama sia installato e funzionante.")
        sys.exit(1)

def main():
    os.system('clear')
    print("🤖 AI Shell Agent - Potenziato da Mistral\n")

    prompt = input("🔎 Cosa vuoi che faccia il terminale? ").strip()
    if not prompt:
        print("❌ Prompt vuoto. Annullato.")
        return

    print("\n🧠 Sto generando il comando...")
    command = generate_command(prompt)

    print("\n💡 Comando suggerito:")
    print(f"\n👉 {command}\n")

    log_command(prompt, command)

    if is_dangerous(command):
        print("⚠️ Questo comando contiene strumenti sensibili o critici.")
    
    confirm = input("Vuoi eseguire il comando? (y/n): ").strip().lower()
    if confirm != "y":
        print("❌ Esecuzione annullata.")
        return

    print("\n🚀 Esecuzione comando...\n")
    try:
        subprocess.run(command, shell=True)
    except Exception as e:
        print(f"❌ Errore durante l'esecuzione: {e}")

if __name__ == "__main__":
    main()
