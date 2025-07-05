import subprocess
import json
import time
import ollama

# Use mistral model locally via Ollama
MODEL = "mistral"

def run_command(command):
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            executable="/bin/bash"  # ensures macOS compatibility
        )
        output = f"$ {command}\n{result.stdout}{result.stderr}"
        return output.strip()
    except Exception as e:
        return f"[ERROR] Failed to run command: {e}"

def ask_ai(messages):
    response = ollama.chat(model=MODEL, messages=messages)
    return response['message']['content']

def main():
    print("🧠 AI Terminal Assistant (Mistral via Ollama)\n")
    goal = input("🎯 What should the AI do using the macOS terminal?\n> ").strip()

    system_prompt = (
        "You are a macOS terminal automation AI. "
        "Your job is to complete the user's goal by thinking step by step, running one terminal command at a time. "
        "After every command, wait to see the result, then decide the next move. "
        "Only say the next terminal command or say DONE when the goal is fully completed."
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"My goal is: {goal}"}
    ]

    while True:
        print("\n🤖 Thinking...")
        ai_command = ask_ai(messages).strip()

        if ai_command.lower() == "done":
            print("✅ AI says task is complete.")
            break

        print(f"\n🧠 AI decided to run:\n{ai_command}\n")

        output = run_command(ai_command)
        print(f"\n📤 Command Output:\n{output}")

        messages.append({"role": "assistant", "content": ai_command})
        messages.append({"role": "user", "content": f"Output:\n{output}"})

        time.sleep(1)

if __name__ == "__main__":
    main()
