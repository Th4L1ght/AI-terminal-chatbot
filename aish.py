import subprocess
import sys
import datetime
import os

LOG_FILE = os.path.expanduser("~/.ai_shell/ai_command_log.txt")

def log_command(prompt, commands):
    with open(LOG_FILE, "a") as f:
        f.write(f"[{datetime.datetime.now()}] Prompt: {prompt}\n")
        f.write("Comandi eseguiti:\n")
        for cmd in commands:
            f.write(f"  {cmd}\n")
        f.write("\n")

def generate_commands(prompt):
    system_prompt = (
        "Agisci come un esperto di terminale Linux. "
        "Quando ti viene chiesto un compito (anche generico come 'installa nginx'), "
        "genera una sequenza di comandi bash, uno per riga, da eseguire direttamente. "
        "Non includere commenti o testo extra.\n\n"
        f"Richiesta: {prompt}\n\n"
        "Comandi:"
    )

    try:
        result = subprocess.run(
            ["ollama", "run", "mistral"],
            input=system_prompt,
            text=True,
            capture_output=True
        )
        commands = result.stdout.strip().splitlines()
        return [cmd.strip() for cmd in commands if cmd.strip()]
    except FileNotFoundError:
        print(" Ollama non trovato. Installa Ollama e il modello mistral.")
        sys.exit(1)

def main():
    os.system('clear')
    print(" AI Terminal Agent - modalità autonoma\n")

    prompt = input("🔎 Cosa vuoi che faccia il terminale? ").strip()
    if not prompt:
        print(" Prompt vuoto.")
        return

    print("\n Generazione comandi...")
    commands = generate_commands(prompt)

    print("\n Comandi generati:")
    for cmd in commands:
        print(f" {cmd}")

    log_command(prompt, commands)

    print("\n Esecuzione automatica...\n")
    for cmd in commands:
        print(f"{cmd}")
        try:
            subprocess.run(cmd, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Errore nel comando: {cmd}\n{e}")

if __name__ == "__main__":
    main()
