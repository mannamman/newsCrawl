# 간단한 크롤링 함수

## TODO
    1. 콘솔로 했던 작업들을 스크립트로 할 수 있게 만들기(cloudRun생성, build트리거 생성...)

## 실행환경
    1. GCP cloudRun
    2. AWS EC2

## 데이터베이스 및 언어
    1. python3.8
    1. MongoDB

## 배포 및 호출
    1. GCP scheduler(호출)
    2. GCP build(빌드)

### 빌드, 배포 작업흐름
    1. github의 두 브랜치(deploy, main)에 push가 된다면 GCP build 실행
    2. GCP build에서 Dockerfile을 바탕으로 빌드 후
    3. GCP cloudRun으로 배포
    4. 일정한 시간마다 GCP scheduler가 cloudRun을 호출
## 흐름도
![flow1](https://user-images.githubusercontent.com/38392519/146722965-c8855634-95b7-4946-9963-fc9a21e45ba2.jpg)
