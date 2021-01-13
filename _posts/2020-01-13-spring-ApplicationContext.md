---
layout: post
title: ApplicationContext
category: spring
tags: [spring, ApplicationContext]
---
## BeanFactory와 ApplicationContext
---
![그림1](https://itphutran.com/wp-content/uploads/2017/04/applicationcontext.jpg)

### BeanFactory

- 스프링 컨테이너의 최상위 인터페이스이다.
- 스프링 빈을 관리하고 조회하는 역활을 한다.
- getBean()을 제공한다.

    - appConfig를 통해 등록된 Bean들을 key값과 대응하는 객체값으로 보여준다.
- 대부분의 기본 기능은 Beanfactory가 제공한다.

### ApplicationContext
- BeanFactory 기능을 모두 상속받아서 제공한다.
- 애플리케이션을 개발할때는 빈을 관리하고 조회하는 기능은 물론, 수 많은 부가기능이 필요하다.

![그림2](https://t1.daumcdn.net/cfile/blog/136F2D3F4E8991D926)
- 메시지소스를 활용한 국제화 기능
    - 한국에서 들어오면 한국어로, 영어권에서 들어오면 영어로 출력
- 환경변수
    - 로컬, 개발, 운영등을 구분해서 처리
- 애플리케이션 이벤트
    - 이벤트를 발행하고 구독하는 모델을 편리하게 지원
- 편리한 리소스 조회
  - 파일, 클래스패스, 외부 등에서 리소스를 편리하게 조회
등등 사용이 가능하다.

BeanFactory 또는 ApplicationContext를 스프링 컨테이너라고 부른다.

## 다양한 설정 형식 지원 - xml, annotation(자바)

![그림 3](https://4.bp.blogspot.com/-szB6l8UWlhA/UC-SrBHNI-I/AAAAAAAAAGQ/nxq7H8s-bcs/s1600/applicationcontext_7_1.JPG)

### 어노테이션 기반
- new AnnotationConfigApplicationContext(AppConfig.class)
- AnnotationConfigApplicationContext 클래스를 사용하면서 자바 코드로된 설정 정보를 넘기면 된다.
```java
public class abc{
    AnnotationConfigApplicationContext ac = new
        AnnotationConfigApplicationContext(TestConfig.class);


    public class TestConfig{
        @Bean
        public memberRepository memberrepository(){
            return new MemoryMemberRepository();
        }
    }
}
```

### xml 기반
- 최근에는 잘 사용하지는 않는다..
- 그러나 아직까지 많은 파일이 xml으로 작성되어졌다.
- GenericXmlApplictionContext 를 사용하면서 xml 설정 파일을 넘기면 된다.
```java
ApplicationContext ac = new GenericXmlApplicationContext("appConfig.xml");
```
---
## 스프링 빈 설정 메타 정보 - BeanDefinition
---
역할과 구현을 개념적으로 나눈 것이다!

    XML을 읽어서 BeanDefinition을 만들면 된다.
    자바 코드를 읽어서 BeanDefinition을 만들면 된다.
    스프링 컨테이너는 자바 코드인지, XML인지 몰라도 된다. 오직 BeanDefinition만 알면 된다.

BeanDefinition 을 빈 설정 메타정보라 한다.

@Bean , <bean> 당 각각 하나씩 메타 정보가 생성된다.

스프링 컨테이너는 이 메타정보를 기반으로 스프링 빈을 생성한다.

![그림3](https://media.vlpt.us/images/happykimnh/post/5e76919b-d992-42fb-8aef-db1ddc30fdb6/image.png)


