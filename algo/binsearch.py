low = 0
high = len(lst) - 1
mid = 0
result = -1

while low <= high:
 
    mid = (high + low) // 2
 
    # If x is greater, ignore left half
    if lst[mid] < x:
        low = mid + 1
 
    # If x is smaller, ignore right half
    elif lst[mid] > x:
        high = mid - 1
 
    # means x is present at mid
    else:
        result = mid
        break
 
print(result)