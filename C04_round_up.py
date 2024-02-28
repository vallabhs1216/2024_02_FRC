import math


# Rounding function
def round_up(amount, round_to):
    return int(math.ceil(amount / round_to)) * round_to

# Main Routine

to_round = [2.75, 2.25, 2]

for item in to_round:
    rounded = round_up(item, 5)
    print(f"${item:.2f} --> ${rounded:.2f}")
