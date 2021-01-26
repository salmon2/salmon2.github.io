def solution(n):
    dp = []
    if n <= 3:
        return n
    else:
        for i in range(n):   
            if i<3:
                dp.append(i+1)
            else:
                dp.append(dp[-1]+dp[-2])
    return dp[-1]
    

answer = solution(6)

print(answer)