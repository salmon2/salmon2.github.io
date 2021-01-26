---
layout: post
title: singletone
category: spring
tags: [singleton, spring]
---

# 스프링의 싱글톤 컨테이너

---
## 목차
- 스프링의 싱글톤
- 싱글톤 패턴
- 싱글톤 컨테이너
- 싱글톤 방시의 주의점
- @Configuration과 싱글톤 생성방식
---

## 스프링의 싱글톤

스프링은 기업용 온라인 기술을 제공하기 위해서 만들어 졌다.

그렇다면 여러 고객이 동시에 요청을 한다면 ```MemberService``` 객체는 여러번 만들어 질까?

여러번 만들어진다면 큰 문제점이 야기된다. 요청이 500, 1000회 발생한다면 객체를 500개, 1000개를 만들어야하고 결국엔 메모리 과다 사용으로 시스템이 다운될 것이다. 그렇기에 ```오직 하나의 객체만을 생성하고 사용하게 해야한다.```

## 싱글톤 패턴

클래스의 인스턴스가 딱 1개만 생성하는 것을 보장하는 패턴

객체 인스턴스가 2개 이상이 되는 것을 막아야한다.

### 방법 1 Eager Initialization(이른 초기화, Thread-safe)
```java
public class Singleton {
    // Eager Initialization
    private static final Singleton uniqueInstance = new Singleton();

    private Singleton() {}

    public static Singleton getInstance() {
      return uniqueInstance; 
    } 
}
```

- private static final을 통해서 컴파일 시점에서 인스턴스를 생성한다. 

- 생성자를 private선언하여 new를 사용하지 못하도록한다.

### 방법 2 Lazy Initialization with synchronized (동기화 블럭, Thread-safe)

```java
public class Singleton {
    private static Singleton uniqueInstance;

    private Singleton() {}

    // Lazy Initailization
    public static synchronzied Singleton getInstance() {
      if(uniqueInstance == null) {
         uniqueInstance = new Singleton();
      }
      return uniqueInstance;
    }
}
```

- synchromzied 키워드를 사용 if문을 통해 인스턴스가 있으면 해당 인스턴스를 반환하고 없다면 생성하여 반환하도록 만든다.
- 단 synchromzied 사용 시 효율이 100배 감소한다.


### 싱글톤 패턴 문제점

- 싱글톤 패턴을 구현하는 코드 자체가 많이 들어간다.
- 의존관계상 클라이언트가 구체 클래스에 의존한다. DIP를 위반한다.
- 클라이언트가 구체 클래스에 의존해서 OCP 원칙을 위반할 가능성이 높다.
- 테스트하기 어렵다.
- 내부 속성을 변경하거나 초기화 하기 어렵다.
- private 생성자로 자식 클래스를 만들기 어렵다.
- 결론적으로 유연성이 떨어진다.
- 안티패턴으로 불리기도 한다
---
## 싱글톤 컨테이너
---
스프링 컨테이너는 싱글톤 패턴의 문제점을 해결하면서, 객체 인스턴스를 싱글톤(1개만 생성)으로 관리한다.

- 스프링 컨테이너는 싱글턴 패턴을 적용하지 않아도, 객체 인스턴스를 싱글톤으로 관리한다.
- 스프링 컨테이너는 싱글톤 컨테이너 역할을 한다. 이렇게 싱글톤 객체를 생성하고 관리하는 기능을 싱글톤 레지스트리라 한다.

![그림4](https://media.vlpt.us/images/happykimnh/post/5e026f0b-d9e8-4777-9b6f-d466002e76d2/image.png)

## 싱글톤 방식의 주의점

객체 인스턴스를 하나만 생성하여 관리함으로 멀티스레드의 공유자원 문제와 동일한 문제점이 발생하여, 주의가 필요하다.

무상태(stateless)로 설계해야 한다!
- 특정 클라이언트에 의존적인 필드가 있으면 안된다.
- 특정 클라이언트가 값을 변경할 수 있는 필드가 있으면 안된다!
- 가급적 읽기만 가능해야 한다.
- 필드 대신에 자바에서 공유되지 않는, 지역변수, 파라미터 ThreadLocal 등을 사용해야 한다.

## @Configuration과 싱글톤 생성방식
```java
@Configuration
public class AppConfig {
    @Bean
    public MemberService memberService() {
        return new MemberServiceImpl(memberRepository());
    }
    @Bean
    public OrderService orderService() {
        return new OrderServiceImpl(memberRepository(), discountPolicy());
    }
    @Bean
    public MemberRepository memberRepository() {
        return new MemoryMemberRepository();
    }
    ...
}
```
코드를 본다면 return 문에서 다시 ```memberRepository(), discountPolicy()```등의 메소드를 실행하여 새로운 객체를 만드는 것처럼 보인다. 실제로 빈에 등록할 때는 새로운 객체를 연결하여 ```OrderService``` 또는 ```MemberService```를 등록할까?

실제로는 그렇지 않다.

일단 ```ApplicationContext ac = new
AnnotationConfigApplicationContext(AppConfig.class);``` 의 파라미터 ```AppConfig.class``` 또한 빈에 등록을 한다. 

단 클래스 정보를 보면 ```bean = class hello.core.AppConfig$$EnhancerBySpringCGLIB$$bd479d70```로 나타난다.

일반 class로 등록한 것이 아닌 뒤에 코드가 붙는데 이것은 @Configuration 어노테이션의 결과물이다.

@Configruation은 Appconfig 클래스가 빈에 등록되기 전에 자바코드에서 ```바이트 코드```로 변환시키는데 이 코드 내용은 대략 아래와 같다.
```java
@Bean
public MemberRepository memberRepository() {

 if (memoryMemberRepository가 이미 스프링 컨테이너에 등록되어 있으면?) {
    return 스프링 컨테이너에서 찾아서 반환;
 } else { //스프링 컨테이너에 없으면
        기존 로직을 호출해서 MemoryMemberRepository를 생성하고 스프링 컨테이너에 등록
    return 반환
 }
}
```
이렇게 바이트코드로 변환하여 각 빈들을 싱글톤 패턴으로 1개씩 인스턴스로 등록한다.

### @Configuration이 없다면?

@Configuration이 없담면 class로 인식하여 AppConfig가 class로 등록되고
```bean = class hello.core.AppConfig``` 하위 빈들 또한 새로운 객체를 만들어서 의존성을 부여하게 된다.

- @Bean만 사용해도 스프링 빈으로 등록되지만, 싱글톤을 보장하지 않는다.
- 싱글톤으로 보장받기위해서는 @Configuration이 필요하다.





---
## 출처
---
https://medium.com/webeveloper/%EC%8B%B1%EA%B8%80%ED%84%B4-%ED%8C%A8%ED%84%B4-singleton-pattern-db75ed29c36