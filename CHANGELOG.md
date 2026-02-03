# 변경 이력

모든 주요 변경사항이 이 파일에 기록됩니다.

형식은 [Keep a Changelog](https://keepachangelog.com/ko/1.0.0/)를 따르며,
이 프로젝트는 [Semantic Versioning](https://semver.org/lang/ko/)을 준수합니다.

---

## [미배포] - 2026-02-02

### 추가됨
- **03_Operations/07_Cost_Analysis.md**: 비용 분석 및 수익성 문서 신규 작성
  - 사용자별 월간 원가 산출 (Light/Heavy/Worst Case)
  - 플랜별 마진 분석 (Starter 96%, Pro 56%)
  - 손익분기점(BEP) 분석 (서버 비용 기준 56명)
  - 5단계 비용 방어 체계 상세 명세
  - 시나리오별 비용 시뮬레이션 (정상/헤비/악용 패턴)
  - Photon/GCP/R2 비용 구성 요소 상세 분석
- CHANGELOG.md: 전체 변경 이력 추적 시스템 도입
- HTML 온보딩 문서 생성기 (`generate_onboarding.py`)
- 통합 HTML 문서 뷰어 (`VIRDY_Onboarding.html`)

### 수정됨
- **02_License_System.md**: 비용 분석 문서 링크 추가 (3.1절)
- **05_Risk_Management.md**: 비용 분석 문서 링크 추가 (R1 리스크)
- **전체 문서**: "Photon Fusion 2" → "Photon Fusion" 용어 통일

---

## [1.0.0] - 2026-01-30

### 추가됨
- 초기 기획 문서 17개 작성 완료
  - 01_Product: 제품 개요, 사용자 플로우
  - 02_Features: 아바타, 트래커, 카메라, 월드, 네트워크, SDK
  - 03_Operations: 사용자 역할, 라이선스, 보안, 데이터 생명주기, 리스크 관리, 계정
  - 04_Design: UI 기획
  - 05_Technical: 아키텍처, 개발 현황

### 문서 형식
- 모든 문서는 표준 구조를 따름 (개요, 핵심 기획, 설계 고려사항, 엣지 케이스, 향후 확장)
- 문서 버전, 최종 수정일, 작성자 메타데이터 포함

---

## 범례

- `추가됨`: 새로운 기능, 문서, 섹션
- `수정됨`: 기존 기능/문서의 변경
- `제거됨`: 삭제된 기능/문서
- `수정 예정`: 향후 변경 예정 사항
- `보안`: 보안 관련 변경사항
