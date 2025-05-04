import os

def ensure_output_dir():
    if not os.path.exists("output"):
        os.makedirs("output")
