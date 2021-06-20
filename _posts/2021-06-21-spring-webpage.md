---
layout: post
title: spring + React 웹페이지 만들기
category: spring
tags: [spring, board]
---

---
## 목차

---
- 기술스택
- 도메인 설계
- 백엔드 구조

---
## 기술스택

---
개발환경 : IntelliJ
빌드 : Maven
백엔드 프레임워크 : Spring
백엔드 라이브러리 : spring security, redis, rabbitmb, eureka server, spring cloud
프론트 : React, Next.js,  
ORM : Jpa, QueryDsl
DB : MariaDB

---
## 도메인 설계

---
![그림](/assets/img/spring/web/01.png)

---
## 백엔드 구조

---
### Spring의 기본 구조

![그림](/assets/img/spring/web/02.png)

### Presentation Layer
```
브라우저상의 웹 클라이언트의 요청 및 응답을 처리
본 프로젝트에서는 rest api를 통하여 http 통신을 하고 json 데이터 형식으로 프론트와 데이터를 주고 받는다.
```


### Business Layer
```
애플리케이션 비즈니스 로직 처리와 비즈니스와 관련된 도메인 모델의 적합성 검증 혹은
repostiory에서 가져온 데이터를 DTO에 맞게 조립한다.
```

### Data Access Layer
```
DB의 테이블과 매칭될 클래스
매칭된 클래스는 Entity 클래스라고 불린다.
```

### DTO(Data Tranfer Object)
```
각 계층간 데이터 교환을 위한 객체 (데이터를 주고 받을 포맷)
Entity 클래스를 바로 사용하는 것은 View Layer와 DB Layer의 역할을 철저하게 분리하기 위해서다.
테이블과 매핑되는 Entity 클래스가 변경되면 여러 클래스에 영향을 끼치게 되지만 View와 통신하는 DTO 클래스는 자주 변경되므로 분리해야 한다.
DTO는 Domain Model을 복사한 형태로, 다양한 Presentation Logic을 추가한 정도로 사용하며 Domain Model 객체는 Persistent만을 위해서 사용한다
```

spring은 계층별로 나누어져 확장성과 재사용성 그리고 중복 코드의 제거를 쉽게 할 수 있다.
그러나 이렇게 계층별로 나눈다면 각 계층별로 코드를 구현하기는 쉬우나 만약 관리되는 도메인(Entity)이 많아진다면 복잡해질 수 있다.
추가로 만약 account 데이터에서 오류가 난다면 post관련 데이터 까지 오류를 살펴보아야한다. 즉 이러한 복잡성과 부분장애에 관한 안정성을 위하여
```MSA(Micro Service Architecure)```로 구현하였다.

### MSA(Micro Service Architecure)
![그림](/assets/img/spring/web/03.png)

### Api GateWay
```
MSA 구조에서 웹 클라이언트의 요청 및 응답을 받는 계층이다.
웹 클라이언트의 url을 분석하여 그에 대응하는 micro service로 url을 보내준다. 
```
### Config Server
```
각 micro service의 DB 주소나, jpa 등의 설정값들을 저장하기 위한 장소로 github 등의 온라인 코드 저장소를 사용할 수도 있고, 
단순히 로컬 디렉토리를 사용할 수도 있다. 이번 프로젝트에서는 github를 통하여 Config Server를 저장하였다.
```
### Micro Server
![그림](/assets/img/spring/web/04.png)
```
각 관리되는 도메인 별로 나누어진 서버로 안에는 controller, business, data access layer로 구성되어 있다.
```

---
## Post 관련 구현

---
### Entity (Java Mapping Class)
![그림](/assets/img/spring/web/05.png)

도메인을 살펴보면 공통된 데이터들은 Post 도메인에 전부 들어 있으며 각 카테고리별 특징들은
각 도메인으로 표현되어지며 이들은 Join을 통해서 데이터를 불러온다.
spring jpa로 상속을 통하여 구현 하였다.

![그림](/assets/img/spring/web/06.png)
![그림](/assets/img/spring/web/07.png)
![그림](/assets/img/spring/web/08.png)

#### @Entity
Java Mapping Class 를 의미

#### Inheritance




