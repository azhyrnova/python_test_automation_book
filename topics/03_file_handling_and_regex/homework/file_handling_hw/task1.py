'''
Task 1
Read the file and remove equal lines (if any).
'''
from pathlib import Path
import os

os.chdir("topics/03_file_handling_and_regex")
relative_path_file = Path("homework")/ "file_handling_hw" / "test_file_for_hw.txt"
output_file = Path("assets") / "task_01_result_file.txt"

def process_file():
    seen = set()
    try:
        with relative_path_file.open("r") as file, output_file.open("w") as out_file:                  
            lines = file.readlines()            
            for i, line in enumerate(lines):
                line = line.strip()            
                if line not in seen:
                    seen.add(line)
                    if i < len(lines) - 1:  # Not the last line
                        out_file.write(line + "\n")
                    else:
                        out_file.write(line)

            file.close()
            out_file.close()       
        
    except FileNotFoundError:
        print("File not found!")
      
process_file()