"""
Ascending Order: Sorts by always moving larger elements to the end
"""
test_list = [10, 1, 2, 3, 8, 5, 6, 7, 11, -2]

def swap (arr, pos1, pos2):
    arr[pos1], arr[pos2] = arr[pos2], arr[pos1]
    

def bubble_sort_ascending(arr):
    n = len(arr)
    for i in range(n - 1): #outer loop
        for j in range(n - 1 - i): #inner loop for comparing numbers next to each other
            if arr[j] > arr[j + 1]:
                swap(arr, j, j + 1)
    return arr 

print("Sorted list in ASC order:" , bubble_sort_ascending(test_list))

"""
Descending Order: Sorts by always moving smaller elements to the end  
"""

def bubble_sort_descending(arr):
    n = len(arr)
    for i in range(n - 1): #outer loop
        for j in range(n - 1 - i): #inner loop for comparing numbers next to each other
            if arr[j] < arr[j + 1]:
                swap(arr, j, j + 1)
    return arr 

print("Sorted list in DESC order:" , bubble_sort_descending(test_list))

"""
Early Stopping: Improves efficiency by halting if no swaps are made during a pass, meaning the list is already sorted
"""

def bubble_sort_descending_with_early_stopping(arr):
    n = len(arr)
    for i in range(n - 1): #outer loop
        swapped = False
        for j in range(n - 1 - i): #inner loop for comparing numbers next to each other
            if arr[j] < arr[j + 1]:
                swap(arr, j, j + 1)
                swapped = True
            if not swapped: 
                break
    return arr 

print("Sorted list in DESC order with early stop:" , bubble_sort_descending_with_early_stopping(test_list))

test_list = [10, 1, 2, -3, 8, -5, 6, 7, 11, -2]

print(bubble_sort_descending(test_list))   