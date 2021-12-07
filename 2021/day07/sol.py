#!/usr/bin/env python3

from os import path


def euler_sum(x):
    return (x + 1) * x // 2


with open(path.join(path.dirname(__file__), "input.txt")) as f:
    crabs = list(map(int, f.read().strip().split(",")))
    left, right = min(crabs), max(crabs)
    part1, part2 = float("inf"), float("inf")
    for target in range(left, right + 1):
        part1 = min(part1, sum(abs(target - c) for c in crabs))
        part2 = min(part2, sum(euler_sum(abs(target - c)) for c in crabs))
    print("Part 1:", part1)
    print("Part 2:", part2)

    # part1 target = median
    # part2 target = floor(mean) or ceil(mean)

# The target for part 2 is always in [mean-0.5, mean+0.5] which given that it has to be an integer means it's either floor(mean) or ceil(mean). So actually, the discretization is the only reason why this is helpful to find the exact value. Otherwise, we'd only know a range. Though I guess there must also be a more complex equation that gives the exact value and probably involves both the mean and median 🤔
# 
# Reason:
# We need to minimize sum(|c-T| * (|c-T|+1) / 2 for c in crabs) where T is the target position, i.e. the variable to minimize over.
# 
# The derivative of that is sum(T-c + (1 if c<=T else -1)/2 for c in crabs) and we want to get that to 0.
# 
# If T is the mean = sum(crabs)/len(crabs) then the first part sum(T-c for c in crabs) = T*len(crabs)-sum(crabs) = sum(crabs)/len(crabs)*len(crabs)-sum(crabs) which is obviously 0.
# 
# But obviously, unless the mean is the median, sum((1 if c<=T else -1)/2 for c in crabs) isn't 0. However, it's never more than len(crabs)/2 away from 0. If it's above zero (i.e. at most len(crabs)/2), using T-0.5 will decrease the first part of the derivative that was previously 0 by exactly len(crabs)/2 which means the derivative now has to be <= 0. And obviously the same goes the other way around if it's below zero and using T+0.5. So the T where the derivative is 0 is definitely in [mean-0.5, mean+0.5].
#
# And I guess it's noteworthy that the value we want to minimize is very close to sum((c-T)²/2 for c in crabs) which we already determined is minimal exactly when T is the mean. I guess the reason this works is because the difference between this and the actual value is bounded linearly in the number of crabs which I guess means it's bounded by a constant factor in the mean?
