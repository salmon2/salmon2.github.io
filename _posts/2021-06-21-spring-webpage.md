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
- MSA 구현
- Post 관련 구현
- Entity
- Dto
- Controller
- Service
- Repository

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
## MSA 구현

---
### ServerDiscovery server 구현

---
![그림](/assets/img/spring/web/17.png)
새로 만들어진 spring 프로젝트에 ```@EnalbleEurekaServer``` 어노테이션을 통해 유레카 서버를 만든다.

![그림](/assets/img/spring/web/16.png)
포트번호는 8761
각 service 들은 application.yml을 통해서 eureka client로 등록이되며 micro service로 인정이 된다.

---
### ApiGateway service 구현

---
앞서 본 msa 방식은 apigateway를 통해서 알맞는 service로 이동하게 된다.

![그림](/assets/img/spring/web/18.png)

apigateway에서는 추가로 로그인에 관련된 인증정보 혹은 토큰 필터역활을 추가로 하게 된다.


![그림](/assets/img/spring/web/19.png)

게이트웨이의 포트는 8000으로 msa방식임으로 백엔드의 기본 포트는 8000으로 고정이된다. 또한 ```globalcors```의 ```allowedOrigins``` 속성에서 접근 가능한 포트번호를 3000(프로젝트에서 프론트서버의 포트번호가 3000이다.) 으로 제한을 해둠으로써 보안에 조금 더 신경을 썼다.
```routes``` 속성을 보면  각 path에 따라서 지정된 eureka server로 라우팅되는 것을 볼 수 있다.
예를 들어 Post /user-service/signup으로 들어온 데이터는 ```routes```을 거쳐 id: siy-user-service의 microservice의 /signup url로 맵핑이 된다.

---
### Configuration Server 구현

---
![그림](/assets/img/spring/web/22.png)
```@EnableConfigServer``` 어노테이션으로 ConfigServer임을 명시하고 만든다.


application.yml
![그림](/assets/img/spring/web/20.png)
각 micro service의 설정 파일들을 넣어주는 server이다.
서버가 가동이 되면 ```cloud```속성의 ```uri```에 들어있는 깃허브 주소의 코드를 기준으로 각 service에 속성파일을 넣어준다.
#### 예
#### https://github.com/JeongJin984/SIYBackConfiguration/blob/master/siyPostService-dev.yml
![그림](/assets/img/spring/web/21.png)
PoserService의 설정정보들이 들어있으며 살펴보면 db의 설정정보 그리고 jpa와 mapping library인 hibernate의 설정들이 들어있다.

---
### Post Service 설정

---

application.yml
![그림](/assets/img/spring/web/23.png)
Eureka server id는 ```siy-post-service```이며 등록되는 eureka 서버의 port번호를 통해서 상위의 eureka server와 연결하고 있다.

![그림](/assets/img/spring/web/24.png)
Poser Service는 eureka server의 client임으로 ```@EnableEurekaClient``` 어노테이션을 사용했으며, 후에 나타날 AccountService와의 통신을 위해서 ```@EnableFeignClients```를 사용하였다.

---
### AccountService 구현

---
![그림](/assets/img/spring/web/25.png)
Eureka server id는 ```siy-user-service```이며 등록되는 eureka 서버의 port번호를 통해서 상위의 eureka server와 연결하고 있다.
![그림](/assets/img/spring/web/26.png)
Post Service와 마찬가지로 같은 어노테이션을 사용하였다.



---
## Post 관련 구현

---
### Entity (Java Mapping Class)

---
### post + study, carpool, contest, miniproject
![그림](/assets/img/spring/web/05.png)

도메인을 살펴보면 공통된 데이터들은 Post 도메인에 전부 들어 있으며 각 카테고리별 특징들은
각 도메인으로 표현되어지며 이들은 Join을 통해서 데이터를 불러온다.
spring jpa로 상속을 통하여 구현 하였다.

![그림](/assets/img/spring/web/06.png)
![그림](/assets/img/spring/web/07.png)
![그림](/assets/img/spring/web/08.png)

상속을 통해서 구현을 하였으며 ```@Inheritance``` single_table 전략으로 같은 테이블로 만들었다.
![그림](/assets/img/spring/web/09.png) 후에 jpa를 통해서 category 상관없이 모든 post를 가져오거나, 혹은
카테고리별로 carPool, study 등으로 가져올 수 도 있다.

### Application, 신청 관련 도메인

이 프로젝트는 사람을 모으는 게시글이기때문에 사람이 신청을하고 방장 혹은 팀장이 사람을 뽑아야한다.
그렇기 때문에 게시글에 신청 정보를 놓는 도메인을 만들었다.
포스트와는 1:n 관계이기 때문에 연관관계 맵핑으로 이를 적용한다.

#### Post.java
![그림](/assets/img/spring/web/12.png)

#### application.java
![그림](/assets/img/spring/web/11.png)

### Participatns, 현재 참석중인 회원의 이름을 담는 도메인

참석자의 정보는 AccountService에서 데이터를 받아오고 그 key에 해당하는 username만을 가지는 도메인을 설계하였다.
후에 참석자 데이터가 필요할 때는 ```feign``` 라이브러리를 사용하여 AccountService를 데이터를 가져오고 조립하여 값을 리턴한다.
post와는 1:n 관계로 묶여있다.

#### Post.java
![그림](/assets/img/spring/web/13.png)

#### Participants.java
![그림](/assets/img/spring/web/14.png)

---
### DTO

---
### 1. UserDto
![그림](/assets/img/spring/web/15.png)
feign을 통해서 UserService와 통신을 하면서 받을 데이터의 포맷형식

### 2. PostDto
![그림](/assets/img/spring/web/27.png)
게시글의 기본적인 데이터 목록 게시글의 id, 글쓴이, 제목, 마감날짜등 기본 정보가 들어있으며 Front Server에서 게시글의 List가 필요할 시 List<>() 객체를 사용 값을 반환해 준다.

### 3. ApplicationDto
![그림](/assets/img/spring/web/29.png)
신청자관련 데이터, 신청한 사람의 이름과 신청할 때 작성된 coment등이 담겨있다.

### 4. ParticipantsDto
![그림](/assets/img/spring/web/30.png)
참석자 관련 데이터, 신청한 사람의 기본 정보가 들어있으며 UserDto로 받은 데이터를 Service계층에서 필요한 데이터로 조립할 때 사용된다.

### 5. PostDtoPostingDetail
![그림](/assets/img/spring/web/31.png)
게시글의 필요한 기본적인 데이터가 들어있으며 PostDto에서 추가로 applicationDto를 Set으로 가지고 있다.
게시글과 그 게시글에 연결되어있는 application의 리스트를 같이 포함한 Dto이다.

PostingDtoDetail은 단독으로 사용되지 않고 이 클래스를 상속하여 카테고리에 맞게 파라미터를 추가하여 사용한다.

### 5-1. PositngDtoDetail를 상속하는 CarPoolDtoPostingDetail
![그림](/assets/img/spring/web/32.png)
카풀 성격에 맞게 Gender(성별), fare(요금), departure(출발지), destination(도착지), departTime(출발시간) 등이 있다. 밑에 long과 let 파라미터는 카카오 지도 api의 좌표 정보이다.

### 5-2. PositngDtoDetail를 상속하는 StudyDtoPostingDetail
![그림](/assets/img/spring/web/33.png)
Study 게시판 성격에 맞게 데이터를 추가하였다.

### 5-3. PositngDtoDetail를 상속하는 ContestDtoPostingDetail
![그림](/assets/img/spring/web/34.png)
Contest 게시판 성격에 맞게 데이터를 추가하였다.


### 5-4. PositngDtoDetail를 상속하는 StudyDtoPostingDetail
![그림](/assets/img/spring/web/35.png)
MiniProject 게시판 성격에 맞게 데이터를 추가하였다.

### 6. PostDtoClosedDetail
![그림](/assets/img/spring/web/36.png)

ParticipantsDto가 결합된 Dto 이다.
이하 상속받은 클래스는 생략하겠다.

### 7. PostDtoAllDetail
![그림](/assets/img/spring/web/37.png)
Participantsdto 와 ApplicationDto 전부를 보여주는 Dto이다.
이하 상속받은 클래스는 생략하겠다.

### 8. CreatePostRequest
![그림](/assets/img/spring/web/38.png)
Front에서 받아온 게시글 정보를 db로 저장할 때 Front에서 받아온 데이터를 이 클래스로 맵핑하여 받아오고 저장한다. 이 클래스 단독으로 사용하지 않고 카테고리별 클래스가 이 클래스를 상속 받아서 사용한다.

---
## Post Controller 구현

---
### InnerClass Result<T>
![그림](/assets/img/spring/web/39.png)
db에서 불러온 데이터를 paging 처리 후 paging 데이터를 추가로 보내기 위해서 만든 class
Generic 문법을 사용하여 데이터를 Result 클래스로 한번 감싸서 데이터를 보내준다.

### 1. ~ 5. 각 게시글의 카테고리별 전체 조회
![그림](/assets/img/spring/web/40.png)

Paging 된 PostDto에 Result 클래스를 덮어서 데이터를 반환한다. 
![그림](/assets/img/spring/web/41.png)
반환 시 자동으로 json형식으로 변환된다.

### 6. ~ 10. 각 게시글의 카테고리별 단독 조회 + applicationDto
![그림](/assets/img/spring/web/42.png)
id를 통해서 게시글을 찾아서 데이터를 반환한다.
이때 서비스계층에서는 게시글에 맞는 application 신청자 데이터 또한 같이 보낸다.

![그림](/assets/img/spring/web/43.png)

### 11. ~ 15. 각 게시글의 카테고리별 저장

 ![그림](/assets/img/spring/web/44.png)
 앞서 설명했던 CreateRequestDto를 통해서 매핑된 데이터를 통해 게시글을 db에 저장한다.

### 16. 내가 만든 게시글의 리스트
![그림](/assets/img/spring/web/45.png)
key 값은 username으로 username에 맞는 게시글을 리스트로 변환하여 반환한다.
![그림](/assets/img/spring/web/47.png)


### 17. 내가 참여중인 게시글의 리스트
![그림](/assets/img/spring/web/46.png)
조인 중인 participants 데이터를 key 값인 username을 통해서 조회하고 조회된 게시글을 리스트로 반환한다.
![그림](/assets/img/spring/web/48.png)

### 18. 포스트 삭제
![그림](/assets/img/spring/web/49.png)

### 19. ~ 23. 포스트 수정
![그림](/assets/img/spring/web/50.png)
앞서 설명했던 CreateRequestDto를 통해서 매핑된 데이터와 id를 통해서 찾아낸 게시글의 정보를 수정한다.

### 24. 검색 기능
![그림](/assets/img/spring/web/51.png)
게시글을 키워드를 통해서 검색할 수 있으며 게시글의 제목 또는 게시글의 작성자를 통해서 검색할 수 있다.

### 25. 게시글 마감하기
![그림](/assets/img/spring/web/52.png)

### 30. ~ 34. 각 게시글의 카테고리별 단독 조회 + ParticipantsDto
![그림](/assets/img/spring/web/53.png)

### 35 ~ 39. 각 게시글의 카테고리별 단독 조회 + ParticipantsDto + ApplicationDto
![그림](/assets/img/spring/web/54.png)

---
## ApplicationController 구현

---
Post 뿐만 아니라 Application의 CRUD도 필요하기 때문에 구현하였다.

### 26. 신청자 신청하기
![그림](/assets/img/spring/web/55.png)
application의 id와 postId를 통해서 application 객체를 만들고 postId를 통해 Post와 연관관계를 맺는다.

### 27. 신청 취소하기
![그림](/assets/img/spring/web/56.png)
방장 혹은 게시글을 작성한 신청자만이 신청을 취소할 수 있다.

### 28. 신청 수정하기
![그림](/assets/img/spring/web/57.png)

### 29. 신청 수락하기
![그림](/assets/img/spring/web/58.png)
해당하는 application 데이터는 삭제되며, 대응되는 participants 데이터가 저장된다.

---
## Post Service 계층 구현

---
![그림](/assets/img/spring/web/59.png)
```PostRepostory``` : Interface지만 Spring 특성상 등록된 bean이 자동으로 주입된다. 프로젝트에서는 후에 설명한 PostRepositoryImpl.class 파일이 자동으로 주입되어 사용할 수 있다.
PostRepository는 Jpa와 QueryDsl로 구성되어 있으며 db에서 데이터를 가져오는 ORM 계층이다.


```CircuitBreakerFactory``` :  Feign library를 통해서 user Service에 접근하여 user정보를 가져온다.
```UserServiceClient``` : CircuitBreaker의 콜백함수로 user Service에 맵핑된 url를 실행 user정보를 가져온다.




### 1. ~ 5. 각 게시글의 카테고리별 전체 조회
![그림](/assets/img/spring/web/60.png)
Paging 데이터를 만든 후 Paging 데이터를 repository에 파라미터로 넘겨주고 데이터를 불러와서 리턴한다.



### 6. ~ 10. 각 게시글의 카테고리별 단독 조회 + applicationDto

![그림](/assets/img/spring/web/61.png)
JPA 의 특징으로 연관관계를 맺은 두 클래스는 Getter 함수를 사용하면 자동으로 post와 application을 join하는 query가 db에 날라가고 데이터를 받아온다.
이 데이터를 Dto에 맞추어 조립하고 controller에 반환한다.




### 11. ~ 15. 각 게시글의 카테고리별 저장

 ![그림](/assets/img/spring/web/62.png)
Service 계층에서는 추가로 ```transactional```관리도 하며 spring은 ```transactional```단위로 데이터를 저장하거나 삭제, 수정을 한다. ```@transactional``` 어노테이션으로 ```readOnly = false```로 설정할 수 있다.
#### PostRequestToPostEntity(post, request)
![그림](/assets/img/spring/web/67.png)
가져온 request 데이터를 post 객체의 파라미터에 맞게 데이터를 넣는다. 이 함수는 수정 시에도 또다시 사용한다.

### 16. 내가 만든 게시글의 리스트
![그림](/assets/img/spring/web/63.png)
Paging 데이터를 만든 후 Paging 데이터를 repository에 파라미터로 넘겨주고 데이터를 불러와서 리턴한다.

### 17. 내가 참여중인 게시글의 리스트
![그림](/assets/img/spring/web/64.png)
Paging 데이터를 만든 후 Paging 데이터를 repository에 파라미터로 넘겨주고 데이터를 불러와서 리턴한다.

### 18. 포스트 삭제
![그림](/assets/img/spring/web/65.png)

### 19. ~ 23. 포스트 수정
![그림](/assets/img/spring/web/66.png)
Spring JPA의 특징 중 하나인 영속성 컨테이너를 사용하였다.
id를 통해서 불러온 데이터는 원본 데이터를 메모리에 저장하고 ```Transactional```이 끝나면 원본 데이터와 수정된 데이터를 비교하여 수정된 부분이 있다면 자동적으로 update query가 날라간다.
그렇기 때문에 Mybatis 처럼 따로 query와 함수를 Mapping 필요가 없다.
PostRequestToPostEntity(post, request) 함수를 db에서 가져온 데이터를 수정한다. 




### 24. 검색 기능
![그림](/assets/img/spring/web/68.png)
페이징 후 repository에 관련된 함수를 실행한다.

### 25. 게시글 마감하기
![그림](/assets/img/spring/web/69.png)
영속성 컨테이너를 사용하여, 데이터의 상태를 closed 상태로 바꾼다.

### 30. ~ 34. 각 게시글의 카테고리별 단독 조회 + ParticipantsDto
![그림](/assets/img/spring/web/70.png)

### 35 ~ 39. 각 게시글의 카테고리별 단독 조회 + ParticipantsDto + ApplicationDto
![그림](/assets/img/spring/web/71.png)

---
## Application Service 구현

---
Post 뿐만 아니라 Application의 CRUD도 필요하기 때문에 구현하였다.

### 26. 신청자 신청하기
![그림](/assets/img/spring/web/72.png)
신청된 application을 저장한다.

### 27. 신청 취소하기
![그림](/assets/img/spring/web/73.png)
방장 혹은 게시글을 작성한 신청자만이 신청을 취소할 수 있다.

### 28. 신청 수정하기
![그림](/assets/img/spring/web/74.png)
신청 수정은 comment만을 수정할 수 있다.

### 29. 신청 수락하기
![그림](/assets/img/spring/web/75.png)
게시글과 신청서는 1대다 맵핑이다. 그렇기 때문에 하나의 게시글에 여러개의 application이 있다.
Front에서 appId를 리스트로 받아와서 for each문을 통해서 신청을 수락한다.
새롭게 Participants를 제작하고 저장한뒤 해당하는 application은 삭제한다.

---
## PostRepository 구현하기

---
![그림](/assets/img/spring/web/76.png)

### 기본적인 CRUD를 책임지는 DATA JPA + 사용자가 Custom할 수 있는 QueryDsl
리포지토리 같은 경우 기본적인 CRUD는 코드로 구현하는 것보다 JPA를 사용하여 구현하였으며, 나머지 query를 통해서 얻어와야하는 경우 QueryDsl을 사용하였다.

### JPA, QueryDsl 적용
앞서 Service 계층에서 Bean에서 자동주입을 통해서 PostRepository가 사용된다고 하였다.
PostRepository는 JpaRepository와 RepositoryCustom을 상속받았는데 이 때 Spring은 Jpa와 내가 만든
RepositoryImpl를 주입한 Repository를 service계층에 자동주입한다.

#### JPARepository
![그림](/assets/img/spring/web/78.png)

#### RepositoryCustom
![그림](/assets/img/spring/web/79.png)

#### PostRepository
![그림](/assets/img/spring/web/77.png)


#### RepositoryCustomImpl
여기서 RepositoryCustom을 구현하는 ```RepostioryCustomImpl```는 QueryDsl을 바탕으로 쉽게 query를 만들어 RepositoryCustom을 구현한다.
![그림](/assets/img/spring/web/80.png)

그럼으로 해당 프로젝트에서 repository를 구현하는 대부분의 코드는 RepositoryCustomImpl의 코드를 작성하는 것이 된다.

---
### RepositoryCustomImpl 구현
---

### 1. ~ 5. 각 게시글의 카테고리별 전체 조회
![그림](/assets/img/spring/web/81.png)

QueryDsl을 사용하기 위해서는 Q클래스가 필요하며 maven같은 경우에는 maven compile을 통해서 Q클래스를 생성할 수 있다.
이 Q 클래스를 통해서 query의 from절, where절, orderBy과 QDto 클래스를 통해서 Dto에 맞는 데이터만을 가져올 수 있다.
![그림](/assets/img/spring/web/82.png)
이렇게 작성된 코드는 백엔드 database 설저에 따라 sql문이 생성되고 날라간다.


### 6. ~ 10. 각 게시글의 카테고리별 단독 조회 + applicationDto
#### Service 계층
![그림](/assets/img/spring/web/61.png)
#### Repository 계층
![그림](/assets/img/spring/web/83.png)

단순 조회를 QueryDsl로 조회하고 간단히 형변환을 통해서 Study 로 형변환하여 리턴할 수 있다.
Repository에서 모든 단독조회는 findPostById를 사용한 뒤 형변환을 하여 데이터를 가져오고 Service계층에서 조립한다.


### 11. ~ 15. 각 게시글의 카테고리별 저장

![그림](/assets/img/spring/web/62.png)
![그림](/assets/img/spring/web/78.png)

단순 저장 임으로 JPA의 save함수를 사용한다.


### 16. 내가 만든 게시글의 리스트
![그림](/assets/img/spring/web/84.png)
QueryDsl의 Where절을 통해 데이터를 가져온다.

### 17. 내가 참여중인 게시글의 리스트
![그림](/assets/img/spring/web/85.png)
QueryDsl의 Join 절을 이용하여 각 게시글과 해당하는 모든 application 중에서 application의 username과 key값이 동일한 것 들 중 Dto에 맞게 데이터를 가져온다. 
여기서 Join은 default로 left Join 이기 때문에 post데이터가 중복될 수 있다.
distinct() 함수를 사용하여 중복을 방지한다.


### 18. 포스트 삭제
![그림](/assets/img/spring/web/78.png)
JPA 사용

### 19. ~ 23. 포스트 수정

### 24. 검색 기능
![그림](/assets/img/spring/web/86.png)
페이징 후 repository에 관련된 함수를 실행한다.
where 절에는 and를 통하여 독립적으로 keyword를 검색할 수 있게 하였다.

### 25. 게시글 마감하기
Service계층에서 영속성 컨테이너로 해결

### 30. ~ 34. 각 게시글의 카테고리별 단독 조회 + ParticipantsDto
6. ~ 10. 참고 Service계층에서 해결


### 35 ~ 39. 각 게시글의 카테고리별 단독 조회 + ParticipantsDto + ApplicationDto
6. ~ 10. 참고 Service계층에서 해결

---
## Application RepositoryCustomImpl 구현

---
Post 뿐만 아니라 Application의 CRUD도 필요하기 때문에 구현하였다.

### 26. 신청자 신청하기
![그림](/assets/img/spring/web/72.png)
JPA 로 구현

### 27. 신청 취소하기
![그림](/assets/img/spring/web/73.png)
![그림](/assets/img/spring/web/87.png)
findByUserName만 QueryDsl로 구현
delete JPA 로 구현

### 28. 신청 수정하기
![그림](/assets/img/spring/web/74.png)
영속성 컨테이너로 Service계층에서 구현


### 29. 신청 수락하기
![그림](/assets/img/spring/web/75.png)
save JPA로 구현


---
## 전체 코드(Front + Back)
---
https://github.com/salmon2/SIY

