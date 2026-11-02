
n = int(input("Enter number of items: "))

profit = []
weight = []

for i in range(n):
    profit.append(int(input(f"Enter profit of item {i+1}: ")))
    weight.append(int(input(f"Enter weight of item {i+1}: ")))

capacity = int(input("Enter knapsack capacity: "))

ratio = [profit[i]/weight[i] for i in range(n)]

items = sorted(range(n), key=lambda i: ratio[i], reverse=True)

max_profit = 0

for i in items:
    if weight[i] <= capacity:
        max_profit += profit[i]
        capacity -= weight[i]
    else:
        max_profit += ratio[i] * capacity
        break

print("Maximum profit:", max_profit)
