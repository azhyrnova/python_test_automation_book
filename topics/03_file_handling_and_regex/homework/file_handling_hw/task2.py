'''
Task 2
Print out all words with length of n-characters
'''
from pathlib import Path
import os

os.chdir("topics/03_file_handling_and_regex")
file_01 = Path("assets")/ "file1.txt"
output_file = Path("assets")/ "task_02_result_file.txt"

def process_file(number):
    try:
        with file_01.open("r") as file, output_file.open("w") as out_file:
            lines = file.readlines()
            for line in lines:
                if len(line) == number+1:
                    out_file.write(line)
            file.close()
            out_file.close()
                
    except FileNotFoundError:
        print("File not found!")
    
process_file(6) #file will contains 6 chars words like Banana Cherry
