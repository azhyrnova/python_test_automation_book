'''
Task 1
Define if a string contains the required characters. 
E.g. if '7865serS3' includes '583' - True; '973' - False
'''

def check_if_string_contains_my_chars(input_string, *my_chars):
    my_chars = [str(char) for char in my_chars] 
    for char in my_chars:
        if char not in input_string: 
            return False   
    return True

test_string = "7865serS3"
test_my_required_chars_true = (5, 8, 3)
test_my_required_chars_false = (9, 7, 3)

print(check_if_string_contains_my_chars(test_string, *test_my_required_chars_true))
print(check_if_string_contains_my_chars(test_string, *test_my_required_chars_false))