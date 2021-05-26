---
layout: post
title: stack
category: c++
tags: [c++, stack]
---

## 목차
-  c++ stack 이란?
-  stack의 선언
-  stack 기본 함수


---

## c++ stack 이란?

---
스택은 자주 사용되는 자료구조 중 하나로 LIFO( Last In First Out)의 특징을 가지고 있습니다.

c++ STL 스택 라이브러리를 통하여 push, pop, size, empty 등등 여러 함수들을 간편하게 사용할 수 있습니다.

---
## stack의 선언

---
```cpp
    #include<stack>
    using namespace std;

    stack<int> st_int;      //int 형 stack 생성

    stack<char> st_int;      //char 형 stack 생성

```
---
## stack 기본 함수

---
```cpp

    #include<stack>
    using namespace std;

    int main(){
 
    stack<int> stack; //int type stack create
 
    stack.push(4); //push 4, 5, 6 to stack
    stack.push(5);
    stack.push(6);
 
    cout << "stack size : " << stack.size() <<endl; //stack size
 
    cout << stack.top() <<endl; //get top element of stack
    stack.pop();    // remove top element of stack
 
    cout <<stack.top() <<endl;
    stack.pop();
 
    cout << stack.top() <<endl;
    stack.pop();

    stack.push(4); //push 4, 5, 6 to stack
    stack.push(5);
    stack.push(6);

    for(int i = 0; i < stack.size(); i++){              // 4, 5, 6 출력
        cout << stack.top() <<endl;
        stack.pop();
    }

    if(stack.empty()){ // check if stack is empty
        cout << "stack is empty " <<endl;
    }
 
    return 0;
}


```
