---
layout: post
title: DP
category: algorithm
tags: [dp]
---
## 다이나믹 프로그래밍이란?
---
```'하나의 문제는 단 한번만 풀도록 하는 알고리즘'```이다. 한번 푼 것을 여러 번 풀지 않고 푼 정답을 저장해 놓은 뒤 꺼내 사용한다.

---

```분할 정복 기법은 동일한 문제를 다시 푼다는 단점```이 존재한다. 예를 들어 ```피보나치 수열```은 특정한 숫자를 구하기 위해서 그 앞에 있는 숫자와 두칸 앞에 있는 숫자의 합을 구해야 한다. 

```
피보나치 수열의 점화식
D[i] = D[i-1] + D[i-2]
``` 
![그림 1](https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR75p1JKENb3gmxjq9lLbSOmukH_Pf2YvLcZQ&usqp=CAU)

![그림 2](data:image/png;base64,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)

이러한 문제는 분할 정복 기업으로 들어갈 시 큰 문제점이 야기된다. ```이미 해결한 문제를 다시 반복적으로 해결하여 비효율성 문제가 생기고 기존보다 문제를 해결하는데 오랜 시간이 걸린다.``` 위 그림을 통해 D[12]인 경우 3번이나 반복적인 계산을 하고 있음을 알 수 있다.

---
## 다이나믹 프로그래밍의 가정
---

1번 가정 : 큰 문제는 작은 문제로 나눌 수 있다.

2번 가정 : 작은 문제에서 구한 정답은 그것을 포함하는 큰 문제에서도 동일하다.

```즉, 크고 어려운 문제가 있다면 그 문제를 작게 쪼개어 해결한 뒤에 전체의 답을 구하는 것이다.```

분할 정복과 다른 점은 이 ```작은 문제를 배열의 저장```하여 나중에 동일한 연산을 해야할 시 저장된 값을 불려와서 사용한다.

```c
#include <stdio.h>

int d(int x) {
	if(x == 1) return 1;
	if(x == 2) return 1;
	return d(x - 1) + d(x - 2);
}

int main(void) {
	printf("%d", d(10));
}
```
위 경우 Dp[10]은 55 로 잘 나오나
만약 Dp[55]를 계산한다면 엄청난 연산량으로 인해 오랜시간이 걸리게 된다.

이를 해결하기 위해서 다음과 같이 수정한다.
```c
#include <stdio.h>

int d[100];

int fibonacci(int x) {
	if(x == 1) return 1;
	if(x == 2) return 1;
	if(d[x] != 0) return d[x];
	return d[x] = fibonacci(x - 1) + fibonacci(x - 2);
}

int main(void) {
	printf("%d", fibonacci(30));
}
```

앞서 저장된 값들이 d라는 배열에 저장이 되고 한 번 구한 값을 다시 계산할 이유가 없어져 계산량이 훨신 줄어들게 된다.

---
출처

https://blog.naver.com/PostView.nhn?blogId=ndb796&logNo=221233570962&redirect=Dlog&widgetTypeCall=true&directAccess=false