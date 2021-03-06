---
layout: post
title: 엔티티
category: jpa
tags: [java]
---
## 목차
- [엔티티](#엔티티)
- [영속성 컨테이너](#영속성-컨테이너)
- [엔티티 매니저 팩토리와 앤티티 매니저](엔티티-매니저-팩토리와-앤티티-매니저)

---
## 엔티티
---
엔티티는 영속성을 가진 객체로 DB 테이블에 보관할 대상입니다. 즉 영속 컨텍스트에 속한 객체를 말합니다. 이러한 엔티티는 특정한 시점에 DB에 영향을 미치는 쿼리를 실행하게 됩니다.
![그림1](https://t1.daumcdn.net/cfile/tistory/99BCFE365C2B116212)

엔티티 설정 방법
1. @Entity 어노테이션 활용
    ```java
        @Entity
        class Mamber{
            @Id @GenerateValue
            private Long id;

            private String name;
        }
    ```
2. xml 설정

출처: https://dev-troh.tistory.com/151 [개발공부블로그]

---
## 영속성 컨테이너
---
- ```엔티티를 영구 저장하는 환경```이라는 뜻

- EntityManager.persist(member)
  - 영속성 컨텍스트를 통해서 엔티티를 영속화 한다는 뜻
  - 엔티티를 영속 상태로 만들어준다.
- EntityManager를 통해 영속성 컨텍스트에 접근하다.

---
## 엔티티 매니저 팩토리와 앤티티 매니저
---
![그림2](data:image/png;base64,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)

- 프로젝트 실행시 EntityManagerFactory 생성
- EntityManagerFactory는 client가 request마다 EntityManager를 생성 후 연결
- EntityMager는 DB의 conn과 연결하여 DB를 사용할 수 있게 해준다.
  