import os
import time
import re
import subprocess
import ollama

MODEL = "mistral"

def ask_ai(messages):
    response = ollama.chat(model=MODEL, messages=messages)
    return response['message']['content'].strip()

def clean_ai_response(response):
    lines = response.splitlines()
    for line in lines:
        line = line.strip()
        if not line or line.startswith("```"):
            continue
        if line.lower() == "done":
            return "DONE"
        if line.startswith("$"):
            line = line[1:].strip()
        if re.match(r"^[a-zA-Z0-9_\-./~\s\"'=|><&]+$", line):
            return line
    return ""

def clean_file_content(content):
    # Remove code fences if any
    lines = content.strip().splitlines()
    cleaned_lines = []
    for line in lines:
        # Skip lines that are just "DONE" or empty
        if line.strip().upper() == "DONE":
            continue
        # Skip markdown fences ``` if present
        if line.strip().startswith("```") and line.strip().endswith("```"):
            continue
        if line.strip().startswith("`") and line.strip().endswith("`"):
            continue
        cleaned_lines.append(line)
    return "\n".join(cleaned_lines).strip() + "\n"

def get_file_contents_from_ai(messages, filename):
    prompt = f"Provide only the exact contents to write inside the file '{filename}'. Reply with code only, no explanation.\n\nAfter you have written the contents in hello.py, please create or edit the file as the system instructed. Then execute the following commands:\n\n$ python3 hello.py\n$ rm hello.pyWhen providing the content for the file, ONLY output the exact raw content of the file. Do NOT include explanations, instructions, or any text outside the code. Do NOT include \"DONE\" or any other markers.Only the exact file content should be returned."
    messages.append({"role": "user", "content": prompt})
    response = ask_ai(messages)
    messages.append({"role": "assistant", "content": response})
    return clean_file_content(response)

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
        return f"[ERROR running command]: {e}"

def main():
    print("🧠 AI Terminal Assistant (Mistral via Ollama)\n")
    goal = input("🎯 What should the AI do using the macOS terminal?\n> ").strip()

    working_dir = os.path.expanduser("~")
    os.chdir(working_dir)
    print(f"📂 Starting in: {working_dir}")

    system_prompt = (
        "You are a macOS terminal assistant AI. "
        "You generate exactly one terminal command or one filename to create/edit at a time. "
        "If you want to create/edit a file, ONLY reply with the exact filename (e.g. hello.py). "
        "The system will ask you for the file contents and create the file. "
        "Do NOT issue commands like touch or nano to create files. "
        "Once a file is created, proceed with commands to complete the user's goal. "
        "Only reply with one command or filename or DONE when finished, no explanations."
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

        # If AI "command" is just a filename, treat it as a file creation/edit request
        if re.match(r"^[\w\-.]+(\.py|\.txt|\.sh)?$", ai_command):
            filename = ai_command
            print(f"\n🧠 AI wants to create/edit file: {filename}")

            file_contents = get_file_contents_from_ai(messages, filename)
            file_path = os.path.join(working_dir, filename)
            with open(file_path, "w") as f:
                f.write(file_contents)

            output = f"[File '{filename}' written with AI-generated contents]"
            print(f"\n📤 {output}")

            messages.append({"role": "assistant", "content": ai_command})
            messages.append({"role": "user", "content": f"[File '{filename}' written with AI-generated contents]"})
            #messages.append({"role": "user", "content": output})

        else:
            print(f"\n🧠 AI decided to run:\n{ai_command}\n")
            output = run_command(ai_command, cwd=working_dir)
            print(f"\n📤 Command Output:\n{output}")

            messages.append({"role": "assistant", "content": ai_command})
            messages.append({"role": "user", "content": f"Output:\n{output}"})

        time.sleep(1)

if __name__ == "__main__":
    main()
