---
layout: post
title: springMVC + mybatis 게시판 만들기
category: spring
tags: [spring, board]
---
## 목차

---
- 기술스택
- 프로젝트 생성하기
- DB 연결하기
- mybatis 연결하기
- 게시글 리스트 보기(R)
- 게시글 자세히 보기(R)
- 게시글 생성하기(C)
- 게시글 수정하기(U)
- 게시글 삭제하기(D)
---
## 기술 스택

---
개발환경 : IntelliJ
빌드 : Gradle
애플리케이션 프레임워크 : Spring
탬플릿 : Thymeleaf
ORM : Mybtis
DB : H2-Database

---
## 프로젝트 생성하기

---
![그림](/assets/img/spring/01.png)

Spring Initializr를 이용하여 쉽게 관련된 라이브러리들을 설치할 수 있다.

---
## DB 연결하기

---
### application.properties
```java
spring.datasource.url=jdbc:h2:mem:testdb
spring.datasource.driverClassName=org.h2.Driver
spring.datasource.username=sa
spring.datasource.password=
```
h2 db의 url과, username, password, driver를 설정해준다.

### schema.sql
db연결을 확인해야함으로 초기 더미데이터를 넣어 확인한다.
```resources/schema.sql``` 파일을 만들고 아래와 같이 query문을 작성한다.

```
DROP TABLE IF EXISTS tbl_board;
CREATE TABLE tbl_board(
    boardId Long auto_increment,
    title varchar (30) not null,
    content varchar (30) not null,
    name varchar (30) not null,
    read integer default 0,
    primary key(boardId)
);

INSERT INTO tbl_board(title, content, name) VALUES('title1', 'content1', 'name1');
INSERT INTO tbl_board(title, content, name) VALUES('title2', 'content2', 'name2');
INSERT INTO tbl_board(title, content, name) VALUES('title3', 'content3', 'name3');
INSERT INTO tbl_board(title, content, name) VALUES('title4', 'content4', 'name4');
INSERT INTO tbl_board(title, content, name) VALUES('title5', 'content5', 'name5');
INSERT INTO tbl_board(title, content, name) VALUES('title6', 'content6', 'name6');
INSERT INTO tbl_board(title, content, name) VALUES('title7', 'content7', 'name7');
INSERT INTO tbl_board(title, content, name) VALUES('title8', 'content8', 'name8');
```
![그림](/assets/img/spring/board/02.png)

---
## mybatis 연결하기

---
### Board.class 생성
보통은 entity는 entity대로 생성하고 db접근은 dao 또는 dto를 사용하지만 이 프로젝트는 entity그대로를 사용한다.
```java
@Setter
@Getter
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class Board {
    private Long boardId;
    private String title;
    private String content;
    private LocalDateTime createDate;
    private Integer read;
    private String name;

    private Long memberId;


    public Board(String title, String content, String name) {
        this.title = title;
        this.content = content;
        this.name = name;
    }

}
```
게시글의 필요한 기능들과 lombok을 활용하여 getter, setter, 생성자들을 구현하였다.

### BoardMapper
com/example/blog_board/mapper/BoardMapper.java 파일 생성
Board클래스와 DB의 tbl_board을 연결해준다. Mapper 안에는 tbl_board와 관련된 select, insert, update, delete문과 같은 query문이 맵핑된다.

```java
@Repository
public interface BoardMapper{

    int boardCount();

    List<Board> findAll();
}
```
@Repository를 통해 스프링 bean에 등록
mybatis같은 경우 함수에 대응하는 query문을 작성하여 맵핑해야한다.
맵핑한 query 문은 resources/com/example/blog_board/mapper/BoardMapper.xml 파일을 만들고 맵핑한다. 
이름을 봐서 알겠지만 위의 BoardMapper와 resource파일 하위에 위치와 이름이 같아야한다.

```
repository : com/example/blog_board/mapper/BoardMapper.java
xml : resources/com/example/blog_board/mapper/BoardMapper.xml
```

```
<?xml version="1.0" encoding="UTF-8" ?>
<!DOCTYPE mapper PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN"
        "http://mybatis.org/dtd/mybatis-3-mapper.dtd">
<mapper namespace="com.example.blog_board.mapper.BoardMapper">

    <select id="boardCount" resultType="int">
        SELECT count(BoardId) AS cbt FROM tbl_board;
    </select>

    <select id="findAll" resultType="com.example.blog_board.domain.Board">
        SELECT
        *
        FROM tbl_board;
    </select>
</mapper>
```
id 는 BoardMapper.interface의 함수명을 동일하게 맞춰주고 리턴 타입이 만약 class라면 경로 또한 적어주어 맵핑한다.

id : BoardMapper.interface 의 대응되는 함수와 매칭
resultType : class라면 전체 이름을 적어주기, 원시타입이라면 그냥 적어도된다. ex) resultType="int"
parameterTyp : 맵핑한 함수의 파라미터의 타입명을 매칭
ex) parameterTyp="Long"

---
## 게시글 리스트 보기

---
### BoardController
모든 사용자는 일단 Controller로 들어오고, 들어온 url에 따라서 기능이 사용된다.
```java
@Controller
@RequestMapping("/boards")
@RequiredArgsConstructor
public class BoardController {

    private final BoardService boardService;

    @GetMapping("/hello")
    public String Hello(){
        return "/board/hello";
    }

    @GetMapping("/test")
    public String test(Model model){
        model.addAttribute("cnt", boardService.boardCount());
        model.addAttribute("test", boardService.boardList());

        return "/board/hello";
    }

    @GetMapping
    public String main(Model model){
        model.addAttribute("boards", boardService.boardList());

        return "/board/boards";
    }
}
```
```@Controller``` : spring의 controller 계층을 암시, bean을 생성한다.
```@RequestMapping("/boards")``` : 하위 url은 /boards + 로 시작된다.

```@RequiredArgsConstructor``` : ```private final BoardService boardService;``` spring DI를 이용하기 위해서 사용, 자동으로 BoardService interface에 적절한 Bean이 주입된다.

```java
    @GetMapping("/test")
    public String test(Model model){
        model.addAttribute("cnt", boardService.boardCount());
        model.addAttribute("test", boardService.boardList());

        return "/board/hello";
    }
```
```return "/board/hello"``` : resources/templates/board/hello.html 파일로 이동된다.
```model.addAttribute("key", value)``` : 이동 시 "key", "value"를 통해 파라미터로 데이터를 들고 갈 수 있다.

```java
<!DOCTYPE html>
<html lang ="en" xmlns:th="http://www.thymeleaf.org">
<head>
    <meta charset="UTF-8">
    <link   th:href="@{/css/bootstrap.min.css}"
            href="../css/bootstrap.min.css" rel="stylesheet">
    <title>테스트 페이지</title>
</head>
<body>
    <h1>
        테스트 페이지!
    </h1>

    <h1>
        [[${cnt}]]
    </h1>
    <h1>
        [[${test}]]
    </h1>
</body>
</html>
```
```model.addAttribute("cnt", value)``` 를 통해서 가져온 cnt 변수를 `[[$cnt]]`로 화면에 출력할 수 있다. `[[$]]`는 타임리프 문법이다.

![그림](/assets/img/spring/board/03.png)



- 기술스택
- 프로젝트 생성하기
- DB 연결하기
- mybatis 연결하기
- 게시글 리스트 보기(R)
- 게시글 자세히 보기(R)
- 게시글 생성하기(C)
- 게시글 수정하기(U)
- 게시글 삭제하기(D)