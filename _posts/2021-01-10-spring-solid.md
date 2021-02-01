---
layout: post
title: solid와 객체지향설계
category: spring
tags: [spring, solid]
---

## 목차

[1. solid란?](#solid-란?)
[2. 예제 코드 보기](#예제-코드-보기)
[3. solid 확인하기](#solid-확인하기)

---
## solid 란?
---
객체 지향 설계 원칙의 앞 글자만을 따서 만든 용어이다.

- SRP (Single Responsibility Principle) 단일 책임 원칙
- OCP (Open Closed Principle) 개방 폐쇄 원칙
- LSP (Liskov Substitution Principle) 리스코프 치환 원칙
- ISP (Interface Segregation Principle) 인터페이스 분리 원칙
- DIP (Dependency Inversion Principle) 의존 역전 원칙

### 1. SRP (Single Responsibility Principle) 단일 책임 원칙

한 클래스는 하나의 책임만 가져야 한다.

- 하나의 책임이라는 것은 모호하다.
- 클 수 있고, 작을 수 있다.
- 문맥과 상황에 따라 다르다.
- 중요한 기준은 변경이다. 변경이 있을 때 파급 효과가 적으면 단일 책임 원칙을 잘 따른 것

### 2. OCP (Open Closed Princple) 개방 폐쇄 원칙
소프트웨어 요소는 확장에는 열려 있으나 변경에는 닫혀 있어야 한다

- 다형성을 활용해본다.
- 인터페이스를 구현한 새로운 클래스를 하나 만들어서 새로운 기능을 구현

### 3. LSP (Liskov Substitution Principle) 리스코프 치환 원칙

프로그램의 객체는 프로그램의 정확성을 깨뜨리지 않으면서 하위 타입의 인스턴스로 바꿀
수 있어야 한다
- 다형성에서 하위 클래스는 인터페이스 규약을 다 지켜야 한다는 것, 다형성을 지원하기 위
한 원칙, 인터페이스를 구현한 구현체는 믿고 사용하려면, 이 원칙이 필요하다.
- 단순히 컴파일에 성공하는 것을 넘어서는 이야기
- 예) 자동차 인터페이스의 엑셀은 앞으로 가라는 기능, 뒤로 가게 구현하면 LSP 위반, 느리
더라도 앞으로 가야함

### ISP (Interface Segregation Principle) 인터페이스 분리 원칙
특정 클라이언트를 위한 인터페이스 여러 개가 범용 인터페이스 하나보다 낫다
- 자동차 인터페이스 -> 운전 인터페이스, 정비 인터페이스로 분리
- 사용자 클라이언트 -> 운전자 클라이언트, 정비사 클라이언트로 분리
- 분리하면 정비 인터페이스 자체가 변해도 운전자 클라이언트에 영향을 주지 않음
- 인터페이스가 명확해지고, 대체 가능성이 높아진다

### DIP (Dependency Inversion Principle) 의존 역전 원칙

프로그래머는 “추상화에 의존해야지, 구체화에 의존하면 안된다.” 의존성 주입은 이 원칙
을 따르는 방법 중 하나다.
- 쉽게 이야기해서 구현 클래스에 의존하지 말고, 인터페이스에 의존하라는 뜻
- 앞에서 이야기한 역할(Role)에 의존하게 해야 한다는 것과 같다. 객체 세상도 클라이언트
가 인터페이스에 의존해야 유연하게 구현체를 변경할 수 있다! 구현체에 의존하게 되면 변
경이 아주 어려워진다.

---
## 예제 코드 보기
---

### 회원 등록 
#### 회원 도메인 클래스 다이어그램
![class](https://user-images.githubusercontent.com/23234577/104121071-fec15580-537e-11eb-94ed-429044b2a570.png)

```MemberServiceImpl``` 은 ```MemberService```를 구현한 구현 객체이다. 이 객체는 다시 ```MemberRepository```를 의존하여 작동한다.

#### 소스코드
##### MemberService.interface
```java
public interface MemberService {
    void join(Member member);

    Member findMember(Long memberId);
}
```

##### MemberServiceImpl.class
```java
public class MemberServiceImpl implements MemberService{

    private final MemberRepository memberRepository = new Memory();

    @Override
    public void join(Member member) {
        memberRepository.save(member);
    }

    @Override
    public Member findMember(Long memberId) {
        return memberRepository.findById(memberId);
    }
}
```
##### MemberRepository.interface
```java
public interface MemberRepository {
    void save(Member member);

    Member findById(Long memberId);

}
```

##### Memory.class

```java
public class Memory implements MemberRepository{
    @Override
    public void save(Member member) {
        ---
    }

    @Override
    public Member findById(Long memberId) {
       ---
    }

}
```
---
## solid 확인하기
---

그렇다면 























<!-- SOLID 원칙들은 결국 자기 자신 클래스 안에 응집도는 내부적으로 높이고, 타 클래스들 간 결합도는 낮추는 High Cohesion - Loose Coupling 원칙을 객체 지향의 관점에서 도입한 것이다.

결과적으로 소프트웨어는 재 사용이 많아지고, 수정이 최소화 되기 때문에 결국 유지 보수가 용이해진다.  -->



