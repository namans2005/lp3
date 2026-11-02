
n = int(input("Enter number of items: "))

profit = []
weight = []

for i in range(n):
    profit.append(int(input(f"Enter profit of item {i+1}: ")))
    weight.append(int(input(f"Enter weight of item {i+1}: ")))

capacity = int(input("Enter knapsack capacity: "))

dp = [0] * (capacity + 1)

for i in range(n):
    for w in range(capacity, weight[i] - 1, -1):
        dp[w] = max(dp[w], profit[i] + dp[w - weight[i]])

print("Maximum profit:", dp[capacity])
