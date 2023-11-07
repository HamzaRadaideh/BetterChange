def DynamicBetterChange(amount, denominations):
    n = len(denominations)
    dp = [float("inf")] * (amount + 1)
    dp[0] = 0
    used_coins = [0] * (amount + 1)

    for i in range(1, amount + 1):
        for j in range(n):
            if denominations[j] <= i and dp[i - denominations[j]] + 1 < dp[i]:
                dp[i] = dp[i - denominations[j]] + 1
                used_coins[i] = denominations[j]

    # Retrieve the denominations used to make the change
    change = []
    remaining = amount
    while remaining > 0:
        change.append(used_coins[remaining])
        remaining -= used_coins[remaining]

    return change


def BruteForceBetterChange(amount, denominations):
    def brute_force_helper(remaining_amount, memo):
        if remaining_amount in memo:
            return memo[remaining_amount]

        if remaining_amount == 0:
            return []

        if remaining_amount < 0:
            return None

        best_change = None
        for coin in denominations:
            change = brute_force_helper(remaining_amount - coin, memo)
            if change is not None:
                change.append(coin)
                if best_change is None or len(change) < len(best_change):
                    best_change = change

        memo[remaining_amount] = best_change
        return best_change

    memo = {}
    change = brute_force_helper(amount, memo)
    return change if change is not None else []

    change = brute_force_helper(amount)
    return change if change is not None else []


def GreedyBetterChange(amount, denominations):
    change = []
    for coin in sorted(denominations, reverse=True):
        while amount >= coin:
            amount -= coin
            change.append(coin)
    return change


def BranchAndBoundBetterChange(amount, denominations):
    n = len(denominations)
    stack = [(amount, 0, [])]  # (remaining_amount, coin_index, current_change)
    best_change = None

    while stack:
        remaining_amount, coin_index, current_change = stack.pop()

        if remaining_amount == 0:
            if best_change is None or len(current_change) < len(best_change):
                best_change = current_change
            continue

        if coin_index == n or remaining_amount < 0:
            continue

        # Use the current coin
        new_change = current_change + [denominations[coin_index]]
        stack.append(
            (remaining_amount - denominations[coin_index], coin_index, new_change)
        )

        # Skip the current coin
        stack.append((remaining_amount, coin_index + 1, current_change))

    return best_change if best_change is not None else []


def main():
    print(
        "Welcome to Algorithm Selector:\n"
        "1. Dynamic Programming:\n"
        "2. Brute Force:\n"
        "3. Greedy Algorithm:\n"
        "4. Branch and Bound (with pruning):"
    )

    choice = int(input("Enter the number of the algorithm you want to use: "))

    amount_in_dollars = float(input("Enter the amount in dollars: "))
    amount_in_cents = int(amount_in_dollars * 100)  # Convert dollars to cents
    denominations = [25, 10, 5, 1]  # Denominations in cents

    algorithms = {
        1: DynamicBetterChange,
        2: BruteForceBetterChange,
        3: GreedyBetterChange,
        4: BranchAndBoundBetterChange,
    }

    if choice in algorithms:
        change_function = algorithms[choice]
        change = change_function(amount_in_cents, denominations)
        algorithm_name = change_function.__name__
    else:
        print("Invalid choice. Please choose a valid algorithm (1-4).")
        return

    if change:
        print(f"Change using {algorithm_name}:")
        print("Amount in cents:", amount_in_cents)
        print("Number of coins used:", len(change))
        print("Denominations used:", change)
        print("Change breakdown:")
        change_counts = {d: change.count(d) for d in set(change)}
        for denomination, count in change_counts.items():
            print(f"{count} x {denomination} cents")
    else:
        print("No valid change can be made for the given amount.")


if __name__ == "__main__":
    main()
