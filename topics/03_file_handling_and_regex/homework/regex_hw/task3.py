'''
Task 3
Define if the string contains at least one Upper case letter followed by Lower case letters. 
E.g. '75serS3' - False; '75WseTrS3' - True
'''
import re

test_pattern_string_ok = "75WseTrS3"
test_pattern_string_fail = "75serS3"

def check_pattern(input_string):
    pattern = ".*([A-Z][a-z])+.*"
    result = True if (re.match(pattern, input_string)) else False
    print(f"For input {input_string} the result is: {result}")
    return result

check_pattern(test_pattern_string_ok)
check_pattern(test_pattern_string_fail)