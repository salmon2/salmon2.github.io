---
layout: post
title: ConponentScan
category: spring
tags: [spring, component]
---

---
# 스프링의 컴포넌트 스캔, 자동주입

## 기존의 수동 빈 등록
---
```java
@Configuration
public class AppConfig {
    @Bean
    public MemberService memberService() {
        System.out.println("call AppConfig.memberService");
        return new MemberServiceImpl(memberRepository());
    }

    @Bean
    public OrderService orderService() {
        System.out.println("call AppConfig.orderService");
        return new OrderServiceImpl(memberRepository(),discountPolicy());
    }
    @Bean
    public MemberRepository memberRepository() {
        System.out.println("call AppConfig.memberRepository");
        return new MemoryMemberRepository();
    }
    @Bean
    public DiscountPolicy discountPolicy() {
        return new RateDiscountPolicy();
    }
}
```
그러나 이렇게 등록해야할 빈들이 수천 수백개면 어떻게 할까?
스프링은 설정정보가 없어도 자동으로 등록해주는 ```컴포넌트스캔```과 의존관계를 자동으로 주입해주는 ```Autowired```기능을 제공한다.

---

## AutoAppConfig.java

---
```java
@Configuration
@ComponentScan(
    excludeFilters = @Filter(type = FilterType.ANNOTATION, classes =Configuration.class)
)
public class AutoAppConfig {
}
```

수동 빈등록과는 다르게 추가로 ```@ComponentScan``` 애노태이션을 통해서 컴포넌트 스캔을 사용할 수 있다.

- excludeFilters 는 기존의 ```Configuration.class```를 삭제하지 않기 위해서 사용하였다. ```@configuration```또한 컴포넌트스캔으로 등록되기에 설정 충동을 막기위해 ```Configuration.class```는 등록하지 않도록 하였다.

---
## @Component
---
컴포넌트 스캔은 이름 그대로 @Component 애노테이션이 붙은 클래스를 스캔해서 스프링 빈으로 등록한
다.

이제 각 클래스가 컴포넌트 스캔의 대상이 되도록 @Component 애노테이션을 붙여주자.

```java
@Component
public class MemoryMemberRepository implements MemberRepository {}
...

@Component
public class RateDiscountPolicy implements DiscountPolicy {}
...

@Component
public class MemberServiceImpl implements MemberService {
    private final MemberRepository memberRepository;
    @Autowired
    public MemberServiceImpl(MemberRepository memberRepository) {
        this.memberRepository = memberRepository;
    }
}
```
수동 조작에서는 ```@bean```을 통해서 직접 설정 정보를 주었다면 자동주입에서는 각 class 코드에 ```@Component``` 애노테이션을 붙여서 실행한다. 

의존관계는 ```@Autowired```를 사용한다.

### @ComponentScan 등록

![그림1](https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSM-o1bOng2vUfK7D6e7kj-Q0uIHNdYigtL0Q&usqp=CAU)

스프링은 해당 클래스의 첫번째 문자만 소문자로 바꾼뒤 컨테이너에 등록한다.

### @Autowired 의존관계 자동주입
만약 코드가
```java
@Component
public class MemberServiceImpl implements MemberService {
    private final MemberRepository memberRepository;
    @Autowired
    public MemberServiceImpl(MemberRepository memberRepository) {
        this.memberRepository = memberRepository;
    }
}
```
memberRepository가 주입을 받아야한다면 컨테이너에서 해당 객체를 검색해본다.

```ac.getBean(memberRepository.class)``` 와 비슷한 결과값으로 반환된 객체를 주입한다.

---
## 탐색 위치
---
```java
@ComponentScan(
    basePackages = "hello.core",
}
```
```basePackage```를 통해 탐색위치를 바꿀 수 있지만 default는 해당 Config파일의 위치부터 찾기된다.

그렇기에 보통 Config를 최상단에 위치시켜놓는 것이 바람직하다.

---
## 컴포넌트 스캔 기본 대상
---

```java
@Component
public @interface Controller {}

@Component
public @interface Service {}

@Component
public @interface Configuration {}
```
컴포넌트 스캔의 용도 뿐만 아니라 다음 애노테이션이 있으면 스프링은 부가 기능을 수행한다.

@Controller : 스프링 MVC 컨트롤러로 인식

@Repository : 스프링 데이터 접근 계층으로 인식하고, 데이터 계층의 예외를 스프링 예외로 변환해준다.

@Configuration : 앞서 보았듯이 스프링 설정 정보로 인식하고, 스프링 빈이 싱글톤을 유지하도록 추가 처
리를 한다.

@Service : 사실 @Service 는 특별한 처리를 하지 않는다. 대신 개발자들이 핵심 비즈니스 로직이 여기에
있겠구나 라고 비즈니스 계층을 인식하는데 도움이 된다.

---
## 수동 빈 등록 vs 자동 빈 등록
---

```java
@Configuration
@ComponentScan(excludeFilters = @Filter(type = FilterType.ANNOTATION, classes =Configuration.class))
public class AutoAppConfig {
    @Bean(name = "memoryMemberRepository")
    public MemberRepository memberRepository() {
        return new MemoryMemberRepository();
    }
}
```

```
Consider renaming one of the beans or enabling overriding by setting
spring.main.allow-bean-definition-overriding=true
```
위 코드처럼 충동이 난다면 수동 빈이 기존 빈을 ```overriding```해버린다.


