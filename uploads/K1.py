def sum_numbers(numb):
    sum = 0
    i = 1
    while i <= numb:
        sum = sum + i
        i = i + 1
    print("The sum is: " + str(sum))   # Should return instead of print
    return    # Useless return statement

x = input("Enter a number: ")
sum_numbers(int(x))  # No error handling for invalid input
