class Solution:
    """Brute force approach for duplicated elements find in given Array"""

    def contains_duplicate(self, nums):
        for i in nums:
            if i == i:
                return True

            return False


class Solution2:
    """ Optimized solution approach for duplicated elements find in given Array"""

    def contains_duplicate(self, nums):
        hashset = set()

        for element in nums:
            if element in hashset:
                return True

            hashset.add(element)

        return False


class Solution:
    def get_concatenation(self, nums):
        ans = []

        for i in range(2):
            for n in nums:
                ans.append(n)
        return ans


print(Solution().getConcatenation([1, 2, 3]))


# Write a Python function to sum all the numbers in a list
def list_sum(list):
    sum = 0
    for x in list:
        sum = sum+x
    return sum


list = [1, 5, 10, 4, 7]
sum = list_sum(list)
print("Sum of List is = ", sum)
