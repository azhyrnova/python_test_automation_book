'''
Task 2
Count a number of Upper case letters in the string. E.g. '7865serS3' - 'Number of Capital letters: 1'
'''
import re

test_string_should_return_1 = '7865serS3'
test_string_should_return_4= 'Python is a high-level programming language that lets you work more efficiently and effectively. You can download the latest version of Python for Windows'

def count_upper_case(input_string):
    pattern = "([A-Z])"
    count = 0
    for char in input_string:
        if re.match(pattern, char):
            count+=1
    return 'Number of Capital letters: ' + str(count)

print(count_upper_case(test_string_should_return_1))
print(count_upper_case(test_string_should_return_4))