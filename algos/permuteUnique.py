def interleave(value, l):
    def helper():
        for i in range(len(l)):
            yield l[:i] + [value] + l[i:]

    res = list(helper()) + [l + [value]]
    return res


class Solution(object):
    def permuteUnique(self, nums):
        def helper(nums):
            if len(nums) <= 1:
                return [nums]

            result = []
            tail = nums[1:]
            perms = helper(tail)
            for perm in perms:
                extension = interleave(nums[0], perm)
                result.extend(extension)

            return result

        return helper(nums)


s = Solution()
res = s.permuteUnique([1, 2, 3])
print(res)
