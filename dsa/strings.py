class Solution:
    def is_anagram(self, s: str, t: str) -> bool:

        if len(s) != len(t):
            return False

        countS, countT = {}, {}

        for i in range(len(s)):
            countS[s[i]] = 1 + countS.get(s[i], 0)
            countT[t[i]] = 1 + countT.get(t[i], 0)

        return countS == countT


print(Solution().is_anagram("anagramw", "nagaram"))


# rotate string
str = "indal"
size = len(str)
temp = str+str

for x in range(size):
    for y in range(size):
        print(temp[x+y], end=" ")
    print()
