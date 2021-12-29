<h1 align="center">
  newsCrawl
</h1>

<p align="center">
  <strong>
    단어 빈도 수 측정
  </strong>
</p>
<p align="center">
  <a href="https://github.com/mannamman/newsCrawl/blob/main/LICENSE">
    <img src="https://img.shields.io/badge/license-MIT-blue.svg"/>
  </a>
</p>

## 💡 개요
특정 주제에대한 뉴스에서 단어들의 빈도를 측정, 저장을 함

- **여러개의 언어로 번역** <br>
  함수를 호출시 target_lanuage에 따라서 원하는 언어로 번역 가능   
  * target_lanuage의 경우에는 Google Translation api가 지원하는 언어까지 가능

- **여러나라의 뉴스를 수집** <br>
  source_language를 기반으로 특정 국가의 뉴스를 바탕으로 단어를 수집   
  * source_language는 현재 eng,fr,jp,kr 존재하며 계속 추가할 예정

- **단어 빈도 통계 및 시각화 지원(예정)**<br>
  언어-주제별로 단어들의 빈도수를 통계 및 시각화

## 🏷️ 문서 목록

- [실행 환경](#-실행-환경)
- [흐름도](#-흐름도)
- [License](#-license)

## 🧰 실행 환경

모든 작업은 클라우드 상에서 실행이 되며,   
크롤링, 통계는 구글 클라우드(GCP)에서 진행,   
EC2에는 데이터베이스가 존재하며, 추후에 시각화를 해야하는 부분에서, 추가로 사용할 수도 있음.

### 1. **플랫폼**
  * GCP<br>
  Container 실행을 위한 cloudRun, 지속적인 배포를 위한 cloudBuild, 주기적인 실행을 위한 cloudScheduler을 사용
  * AWS<br>
  24/7 돌아가야하는 상황에 맞추어 VM을 생성(EC2)

### 2. **언어**
   * Python(3.8)

### 3. **데이터베이스 및 프레임워크**
  * MongoDB
  * Flask

### 4. **번역**
  * Google Translation api

### 5. **빌드 및 배포**
  * github
  * GCP BUILD

## 📷 흐름도
![flow1](https://user-images.githubusercontent.com/38392519/146722965-c8855634-95b7-4946-9963-fc9a21e45ba2.jpg)


## 📝 License

Licensed under the [MIT License](./LICENSE).