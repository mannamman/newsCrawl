<h1 align="center">
  stock advise
</h1>

<p align="center">
  <strong>
    뉴스 헤드라인 이용하여 주식 도움
  </strong>
</p>
<p align="center">
  <a href="https://github.com/mannamman/newsCrawlWeb/blob/main/LICENSE">
    <img src="https://img.shields.io/badge/license-MIT-blue.svg"/>
  </a>
</p>

## 💡 개요
특정 주제에 대한 뉴스의 헤드라인을 분석(sentiment analysis), 주식 도움


- **여러나라의 뉴스를 수집(추가 예정)** <br>
  source_language를 기반으로 특정 국가의 뉴스를 바탕으로 단어를 수집
  * 현재는 en(usa)의 뉴스만 크롤링 중
  


## 🏷️ 문서 목록

- [실행 환경](#-실행-환경)
- [흐름도](#-흐름도)
- [License](#-license)

## 🧰 실행 환경

모든 작업은 클라우드 상에서 실행이 되며,
작업예약(cron), 크롤링, 번역, 감정분석은 GCP상에서 실행,
EC2에는 데이터베이스가 존재하며, 추후에 시각화를 해야하는 부분에서, 추가로 사용할 수도 있음.

### 1. **플랫폼**
  - **GCP**<br>
    - 빌드를 위한 cloud build
    - Container 실행을 위한 cloudRun
    - 지속적인 배포를 위한 cloudBuild
    - 주기적인 실행을 위한 cloudScheduler
  - **AWS**<br>
    - 24/7 돌아가야하는 상황에 맞추어 VM을 생성(EC2)


### 2. **언어**
   * Python(3.8)

### 3. **데이터베이스 및 프레임워크**
  * MongoDB
  * Flask

### 4. **번역**
  * Google Translation api

### 5. **감정분석(sentiment analysis)**
  * https://github.com/ProsusAI/finBERT

### 5. **빌드 및 배포**
  * github
  * GCP BUILD

## 📷 흐름도

### **빌드 및 배포**
![_crawl_build_deploy](https://user-images.githubusercontent.com/38392519/151313001-cae1425b-2801-4686-b857-1b74c2b826ac.jpg)

### **내부 동작**
* 추가 예정

## 📝 License
Licensed under the [MIT License](./LICENSE).