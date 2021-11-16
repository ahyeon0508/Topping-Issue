# 톺핑있슈(Topping-Issue)
2021 ETRI 오픈 API 활용사례 공모전  

-----------------------------------------------------
### 1. 프로젝트의 개요
#### 1-1. 프로젝트 개발 배경
&nbsp;&nbsp;&nbsp;본 공모안의 주제를 정하기 위하여 최근 시사이슈를 탐색하던 도중, 생소한 이슈를 보게 되었다. 조원들 중 그 누구도 해당 이슈에 대하여 상세히 알고있는 사람이 없어, 이에 대한 정보를 찾아보게 되었다.  
&nbsp;&nbsp;&nbsp;그러나, 특정 이슈에 대한 정보가 정리되어 제공되는 서비스가 존재하지 않았고, 웹 검색 만으로 특정 이슈를 둘러 싸고 있는 다양한 파생 주제를 파악하는데 어려움이 있었다. 이에 특정 이슈와 그에 대한 파생주제들을 파악하기 쉽게 사용자에게 제공하는 서비스를 기획하게 되었다.  
&nbsp;&nbsp;&nbsp;파생 주제들을 어떻게 파악할 수 있을 것인가에 대하여 기술적 측면을 고민하던 중, BERT의 CLS토큰이 문맥상의 의미를 어느정도 보유하고 있다는 점에서 착안하여 S-BERT를 기반으로 한 문장 임베딩을 통해 해당 과제를 달성할 수 있을 것이라고 생각하였다.  
&nbsp;&nbsp;&nbsp;따라서, 본 프로젝트에서는 BERT를 기반으로 기간내 이슈의 변화량과 이슈에 대한 파생 주제의 변화를 서비스화 하고자 한다.

#### 1-2. 프로젝트 목표 및 핵심 기술
#### 최종 목표 : 기간내 이슈의 변화량과 이슈에 대한 파생 주제의 변화를 서비스화
#### 핵심 기술
- News Clustering (Cosine similarity based) -> Key-word & Sub-word
- Sentiment Analysis

### 2. 개발 환경 및 개발 언어
|| tool |
| ------ | ------ |
| 개발언어 | ![issue badge](https://img.shields.io/badge/python-3.8-blue.svg) ![issue badge](https://img.shields.io/badge/javascript-blue.svg) |
| 라이브러리 & 프레임워크 | ![issue badge](https://img.shields.io/badge/Flask-2.0.1-green.svg) ![issue badge](https://img.shields.io/badge/jQuery-green.svg) |
| Open API | [ETRI 형태소 인식 API](https://aiopen.etri.re.kr/guide_wiseNLU.php) |
| 학습 모델 | [ETRI KorBERT](https://aiopen.etri.re.kr/service_dataset.php) |
| 개발환경 | Windows10 |
| 데이터베이스 환경 | ![issue badge](https://img.shields.io/badge/SQLite3-lightgrey.svg) |

### 3. 구조도 및 시연
<p align="center" style="color:gray">
  <img style="margin:50px 0 10px 0" src="https://user-images.githubusercontent.com/44939208/141938495-9c3ab6e7-0c6d-46a1-895e-74fcc7e54053.png" alt="구조도" width="50%" height="50%"  />
  <br>[그림 1] 구조도 <br>
</p> <br>

<p align="center" style="color:gray">
  <img style="margin:50px 0 10px 0" src="https://user-images.githubusercontent.com/44939208/141938651-2f5d7ce0-7a3b-4341-9355-1a0be506d933.png" alt="웹페이지 중 일부" width="50%" height="50%"  />
  <br>[그림 2] 웹페이지 중 일부 <br>
</p> <br>

### 4. 기대효과 및 활용방안
&nbsp;&nbsp;&nbsp;본 서비스를 통하여 평소 관심 갖지 않던 분야에 대한 인사이트와 정보를 얻을 수 있다.  
&nbsp;&nbsp;&nbsp;누구나 포털 사이트 메인 페이지에 실린 뉴스 기사를 보던 중 특정 분야의 기사를 처음 접하게 되거나, 생소한 분야에 관심을 갖게 되는 상황이 발생할 수 있다. 이와 같은 경우 새로운 분야에 대한 이전 이슈의 흐름들을 파악하기에는 방대한 양일 것이다. 이에 사용자는 본 서비스를 통하 여 정리된 정보를 제공받고, 빠르게 해당 분야에 대한 흐름을 파악할 수 있을 것이다.  
&nbsp;&nbsp;&nbsp;이와 같은 장점을 토대로 평소 시사에 관심을 두지 않던 대학생, 취업준비생이라면 이 서비스를 활용하여 분야별 원하는 기간에 따른 이슈의 흐름을 파악하여 공모전, 프로젝트 등의 주제에 활용할 수 있고, 해당 분야의 상식을 쌓는 데에 도움을 얻어 면접 등에 활용할 수도 있다. 혹은 특정 프로젝트를 진행하게 되었을 경우를 비롯한 다양한 상황에서 이 서비스를 통해 인사이트를 얻는 데에 도움을 받을 수 있을 것이다.

### 5. 기타
- 자세한 내용은 보고서 및 시연 영상 참고

-----------------------------------------------------
참여자 : 이현준, 이서우, 이아현  
수행 기간 : 2021.09.06 ~ 2021.10.18