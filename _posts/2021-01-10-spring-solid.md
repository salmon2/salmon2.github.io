---
layout: post
title: solid와 객체지향설계
category: spring
tags: [spring, solid]
---
## solid 란?
---
객체 지향 설계 원칙의 앞 글자만을 따서 만든 용어이다.

- SRP (Single Responsibility Principle) 단일 책임 원칙
- OCP (Open Closed Principle) 개방 폐쇄 원칙
- LSP (Liskov Substitution Principle) 리스코프 치환 원칙
- ISP (Interface Segregation Principle) 인터페이스 분리 원칙
- DIP (Dependency Inversion Principle) 의존 역전 원칙

---
## 1. SRP (Single Responsibility Principle) 단일 책임 원칙

---
한 클래스는 하나의 책임만 가져야 한다.
즉, 객체 간의 응집도는 높고 결합도가 낮은 프로그램이라는 뜻으로 해석할 수 있다.

- 하나의 책임이라는 것은 모호하다.
- 클 수 있고, 작을 수 있다.
- 문맥과 상황에 따라 다르다.
- 중요한 기준은 변경이다. 변경이 있을 때 파급 효과가 적으면 단일 책임 원칙을 잘 따른 것

```java
class Calculator{
	public void add(int a, int b){...}   //더하기
	public void sub(int a, int b){...}   //빼기
	public void mul(int a, int b){...}   //곱하기
	public void div(int a, int b){...}   //나누기
}
```
```Calculator```클래스는 사칙연산에 대한 기능만 가지고 있어야한다.

계산기가 추후에 다른 기능을 지원한다해서 계산기에 사칙연산 이외의 기능을 추가한다면 이는 응집도가 낮아지고 메소드간의 결합이 강해질 것이다.

현재는 사칙연산의 계산역활만을 가지는 단일책임 맡고 있어 SRP를 잘 지키고 있다.

---
## 2. OCP (Open Closed Princple) 개방 폐쇄 원칙

---
소프트웨어 요소는 확장에는 열려 있으나 변경에는 닫혀 있어야 한다

- 다형성을 활용해본다.
- 인터페이스를 구현한 새로운 클래스를 하나 만들어서 새로운 기능을 구현

```java
//Car 인터페이스
public interface Car {
	public boolean isHybrid();
}

//Bus 구현 클래스
public class Bus implements Car {
	@Override
	public boolean isHybrid() {
		return false;
	}
}

//Bus 구현 클래스
public class Truck implements Car {
	@Override
	public boolean isHybrid() {
		return true;
	}
}
```
Car인터페이스가 있고, Bus와 Truck 구현 클래스가 있다. 하이브리드 차인지 확인만 하고 싶은 클라이언트는 구현 클래스만 선언해서 호출하면 된다.

```java
Car bus = new Bus();
Car truck = new Truck();

bus.isHybrid();
truck.isHybrid();
```
클라이언트가 Bus에 대한 구현 클래스 기능을 사용하다가 Truck에 대한 구현 클래스 기능을 사용하고자 한다면 기존의 코드가 변경된 것이 아닌가? 라는 의문점이 생길수 있다.

클라이언트가 직접 구현 클래스를 선택하기 때문에 클라이언트 코드의 변경이됨을 확인할 수 있다.즉, 다형성을 이용했지만 OCP 원칙이 깨지는 현상이 발생한다.

따라서, 객체를 생성하고 연관관계를 맺어주는 별도의 조립, 설정자가 필요한데, Spring Framework는 Spring Container와 bean이 이 역할을 담당한다.

---
## 3. LSP (Liskov Substitution Principle) 리스코프 치환 원칙

---

프로그램의 객체는 프로그램의 정확성을 깨뜨리지 않으면서 하위 타입의 인스턴스로 바꿀
수 있어야 한다
- 다형성에서 하위 클래스는 인터페이스 규약을 다 지켜야 한다는 것, 다형성을 지원하기 위
한 원칙, 인터페이스를 구현한 구현체는 믿고 사용하려면, 이 원칙이 필요하다.
- 단순히 컴파일에 성공하는 것을 넘어서는 이야기
- 예) 자동차 인터페이스의 엑셀은 앞으로 가라는 기능, 뒤로 가게 구현하면 LSP 위반, 느리
더라도 앞으로 가야함

```java
public class Car {
	public void accel(int speed) {
		speed += 10;
	}
}

public class MiniCar extends Car{
	@Override
	public void accel(int speed) {
		speed -= 20;
	}
}
```
위 코드는 컴파일 시 ```아무 문제가 발생하지 않는다.``` 하지만 ```부모클래스가 지정한 accel의 기능을 무사히고 있어 LSP에 위배```되고있다.

따라서, ```부모클래스를 상속하는 자식클래스는 부모 클래스의 규약을 무시하거나 오버라이딩을 자제```해야하는 것이 LSP이다.

---
## 4. ISP (Interface Segregation Principle) 인터페이스 분리 원칙

---
특정 클라이언트를 위한 인터페이스 여러 개가 범용 인터페이스 하나보다 낫다
- 자동차 인터페이스 -> 운전 인터페이스, 정비 인터페이스로 분리
- 사용자 클라이언트 -> 운전자 클라이언트, 정비사 클라이언트로 분리
- 분리하면 정비 인터페이스 자체가 변해도 운전자 클라이언트에 영향을 주지 않음
- 인터페이스가 명확해지고, 대체 가능성이 높아진다

```java
interface People {
	public void cook();     //요리하기
	public void cleaning(); //청소하기

	public void work();     //작업하기
	public void submit();   //제출하기
}
```

```java
//주부 인터페이스
interface Housewife {
	public void cook();
	public void cleaning();
}

//직장인 인터페이스
interface Worker {
	public void work();
	public void submit();
}
```
People 에서 Houwewife와 Worker로 분해하여 좀 더 구체적인 책임을 주어 나누어주었다.
좀 더 명확하고 알기 쉬운 코드가 되었다.
이렇게 일반적인 인터페이스(people)을 구체적인 여러 인터페이스(Housewife, Worker)로 나눠주는 것이 객체지향적인 관점에서 더 좋은 설계이며 ISP를 잘 지킨 설계이다.

---
## 5. DIP (Dependency Inversion Principle) 의존 역전 원칙
---
프로그래머는 “추상화에 의존해야지, 구체화에 의존하면 안된다.” 의존성 주입은 이 원칙
을 따르는 방법 중 하나다.
- 쉽게 이야기해서 구현 클래스에 의존하지 말고, 인터페이스에 의존하라는 뜻
- 앞에서 이야기한 역할(Role)에 의존하게 해야 한다는 것과 같다. 객체 세상도 클라이언트
가 인터페이스에 의존해야 유연하게 구현체를 변경할 수 있다! 구현체에 의존하게 되면 변
경이 아주 어려워진다.

- 구현체보다 인터페이스나 추상 클래스에 의존해야 기존 기능의 변경이나 새로운 요구사항을 통한 기능 확장이 되었을 때 유연한 변경이 가능하다.

- 여기서 OCP는 인터페이스와 구현체 둘다 의존하는 것을 알 수 있는데, 이는 DIP를 위반하는 것으로 볼 수 있다.

---
## 결론

---

SOLID 원칙들은 결국 자기 자신 클래스 안에 응집도는 내부적으로 높이고, 타 클래스들 간 결합도는 낮추는 High Cohesion - Loose Coupling 원칙을 객체 지향의 관점에서 도입한 것이다.

결과적으로 소프트웨어는 재 사용이 많아지고, 수정이 최소화 되기 때문에 결국 유지 보수가 용이해진다.



