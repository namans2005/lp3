def fibo_recursive(n):
    global steps
    steps += 1

    if n <= 1:
        return n
    else:
        return fibo_recursive(n-1) + fibo_recursive(n-2)


def fibo_iterative(n):
    global steps
    a, b = 0, 1

    for i in range(n):
        steps += 1
        print(a, end=" ")
        a, b = b, a+b


n = int(input("Enter number: "))

# Recursive approach
steps = 0
print("\nFibonacci recursive: ", end=" ")
for i in range(n):
    print(fibo_recursive(i), end=" ")

print(f"\nSteps count: {steps}")

# Iterative approach
steps = 0
print("\nFibonacci iterative: ", end=" ")
fibo_iterative(n)
print(f"\nSteps count: {steps}")
