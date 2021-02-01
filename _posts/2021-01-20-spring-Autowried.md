---
layout: post
title: Autowried
category: spring
tags: [spring]
---

## 다양한 의존관계 주입
---
- 생성자 주입
- 수정자 주입(setter 주입)
- 필드 주입
- 일반 메서드 주입
---
## 생성자 주입
```java
private final MemberRepository memberRepository;
private final DiscountPolicy discountPolicy;
@Autowired
public OrderServiceImpl(MemberRepository memberRepository, DiscountPolicy discountPolicy) {
    this.memberRepository = memberRepository;
    this.discountPolicy = discountPolicy;
}
```
- final 키워드를 통해 만약 내가 실수하여 코드를 작성하지 않았더라도 바로 컴파일 에러가 발생하게 해준다.

- 대부분의 의존관계 주입은 한번 일어나면 애플리케이션 종료시점까지 의존관계를 변경할 일이 없다. 오히려 대부분의 의존관계는 애플리케이션 종료 전까지 변하면 안된다.(불변의 원치)

- 누군가 실수로 변경할 수 도 있고, 변경하면 안되는 메서드를 열어두는 것은 좋은 설계 방법이 아니다.

---
## 조회 빈이 2개 이상일 때
---

```java
    @Autowired
    public MemberServiceImpl(MemberRepository memberRepository) {
        this.memberRepository = memberRepository;
    }
```
만약 ac.getbean(memberRepository.class)의 빈이 2개라면 어떻게 될까?
```
NoUniqueBeanDefinitionException: No qualifying bean of type
```
바로 에러메시지가 출력된다.

### 해결방법
- 필드명
- @Qaulifier
- @Primary

#### 필드명
```java
private MemberRepository memoryMemberRepository;
```
빈 조회는 여러 빈 들이 있을 때 필드 이름, 파라미터 이름으로 다시 찾는다. 그러므로 필드명을 원하는 빈의 이름으로 수정하여 등록한다.

#### Qualifier
```java
@Component
@Qualifier("abc")
public class MemoryMemberRepository implements MemberRepository{}

...

@Autowired
public OrderServiceImpl(MemberRepository memberRepository, @Qualifier("abc") MemberRepository memberRepository) {}
```
별명을 지어주듯이 지정된 이름을 @Autowired에 지정해준다.

#### Primary
```java
@Component
@Primary
public class RateDiscountPolicy implements DiscountPolicy {}
```
@Autowired부분에 수정없이 @Component부분에 @Primary 애노테이션을 붙여 설정해준다.

## Primary와 Qualifier

primary는 쉽고 간결하며 Qualifier는 세세하다. 두개 같이 사용한다면 Qualifier가 더 우선권이 있어 Qualfier를 더욱 우선시 한다.



