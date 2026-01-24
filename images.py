import os
from pathlib import Path
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import ImageFormatter

def batch_highlight_project(project_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for root, _, files in os.walk(project_dir):
        for file in files:
            if file.endswith(".py"):
                file_path = Path(root) / file
                
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        code = f.read()

                    img_bytes = highlight(code, PythonLexer(), ImageFormatter(font_name="Consolas"))

                    relative_path = os.path.relpath(file_path, project_dir)
                    output_filename = relative_path.replace(os.sep, "_") + ".png"
                    output_path = Path(output_dir) / output_filename

                    with open(output_path, "wb") as f:
                        f.write(img_bytes)
                    
                    print(f"Processed: {relative_path} -> {output_filename}")
                
                except Exception as e:
                    print(f"Failed to process {file_path}: {e}")


PROJECT_PATH = "./."
OUTPUT_PATH = "./highlighted_images"

batch_highlight_project(PROJECT_PATH, OUTPUT_PATH)