import subprocess
import os
import time
import ollama

MODEL = "mistral"

def run_command(command, cwd):
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            cwd=cwd,
            executable="/bin/bash"
        )
        output = f"$ {command}\n{result.stdout}{result.stderr}".strip()
        return output
    except Exception as e:
        return f"[ERROR] {e}"

def ask_ai(messages):
    response = ollama.chat(model=MODEL, messages=messages)
    return response['message']['content'].strip()

def clean_ai_response(response):
    """
    Extracts only the shell command from the AI response.
    """
    lines = response.splitlines()
    for line in lines:
        # Remove markdown or prompts
        if line.strip().startswith("```"):
            continue
        if line.strip().startswith("$"):
            line = line.strip().lstrip("$").strip()
        if line.strip().lower() == "done":
            return "DONE"
        if line.strip() != "":
            return line.strip()
    return ""

def main():
    print("🧠 AI Terminal Assistant (Mistral via Ollama)\n")
    goal = input("🎯 What should the AI do using the macOS terminal?\n> ").strip()

    # Set working directory to user’s home
    working_dir = os.path.expanduser("~")
    os.chdir(working_dir)
    print(f"📂 Starting in: {working_dir}")

    system_prompt = (
        "You are a macOS terminal assistant. "
        "Your job is to complete the user's goal by giving one shell command at a time. "
        "After each command, you will receive the terminal output and suggest the next command. "
        "Only respond with one command (no explanations). "
        "When the task is done, respond with DONE."
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"My goal is: {goal}"}
    ]

    while True:
        print("\n🤖 Thinking...")
        ai_response = ask_ai(messages)
        ai_command = clean_ai_response(ai_response)

        if ai_command.upper() == "DONE":
            print("✅ AI says task is complete.")
            break

        print(f"\n🧠 AI decided to run:\n{ai_command}\n")

        output = run_command(ai_command, cwd=working_dir)
        print(f"\n📤 Command Output:\n{output}")

        messages.append({"role": "assistant", "content": ai_command})
        messages.append({"role": "user", "content": f"Output:\n{output}"})

        time.sleep(1)

if __name__ == "__main__":
    main()
