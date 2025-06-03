import os

# 👉 ΕΔΩ βάλε το path του φακέλου του bot
base_path = r"C:\Users\dinod\Desktop\ΒΟΤ\crypto-bot"

output_file = os.path.join(base_path, "all_code.txt")

with open(output_file, "w", encoding="utf-8") as out:
    for root, dirs, files in os.walk(base_path):
        for file in files:
            if file.endswith((".py", ".js", ".ts", ".json", ".txt", ".env")):
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, base_path)
                out.write(f"\n. {rel_path}\n")
                out.write("-" * 50 + "\n")
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    out.write(f.read() + "\n")
