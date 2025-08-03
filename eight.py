# Write a Python Program to check prime number

num = int(input("Enter a number: "))

if num > 1:
    for i in range(2, int(num**0.5) + 1):
        if num % i == 0:
            print(num, "is NOT a Prime Number")
            break
    else:
        print(num, "is a Prime Number")
else:
    print(num, "is NOT a Prime Number")
