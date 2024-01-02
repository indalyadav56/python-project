import itertools

numbers = [1, 2, 3]
letters = ['a', 'b']

# Generate all possible pairs of numbers and letters
for pair in itertools.product(numbers, letters):
    print(pair)