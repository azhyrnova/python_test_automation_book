'''
Task 3
Combine two files into a third file
'''

from pathlib import Path
import os

os.chdir("topics/03_file_handling_and_regex")
file_01 = Path("assets")/ "file1.txt"
file_02 = Path("assets")/ "file2.txt"
output_file = Path("assets")/ "task_03_combined_file.txt"

def merge_two_files(file1, file2, output_file):
        try:
            #with relative_path_file.open("r") as file, relative_path_out_file.open("w") as out_file:
            with file_01.open("r") as f1, file_02.open("r") as f2, output_file.open("w") as out_file:
                out_file.write(f1.read())
                out_file.write("[---DATA FROM FILE_01 IS UPLOADED---]" + "\n")
                out_file.write(f2.read())
                out_file.write("[---DATA FROM FILE_02 IS UPLOADED---]")
            
        except FileNotFoundError:
            print("File(s) not found!")
        except Exception as e:
            print(f"An error occurred: {e}")
            
merge_two_files(file_01, file_02, output_file)