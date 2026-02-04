# 변경 이력

모든 주요 변경사항이 이 파일에 기록됩니다.

형식은 [Keep a Changelog](https://keepachangelog.com/ko/1.0.0/)를 따르며,
이 프로젝트는 [Semantic Versioning](https://semver.org/lang/ko/)을 준수합니다.

---

## [미배포] - 2026-02-03

### 추가됨
- **05_Technical/03_API_Specification.md**: API 명세 문서 신규 작성
  - 현행 Firebase Functions API 정리
  - 전환 검토 중인 Spring Boot REST API (인증, 아바타, 세션, Webhook)
  - Signed URL 보안 정책, 에러 응답 형식
  - 향후 추가 예정 API 영역 정리

### 수정됨 (서버 개발자 회의 2차 내용 반영)
- **03_Operations/02_License_System.md** (v1.1 → v1.2): 플랜 구조 확정 및 제한 정책 구체화
  - 5단계 티어 체계 확정 (Free/Starter/Pro/Studio/Enterprise)
  - 아바타 슬롯 50개, 200MB/개 제한 명시
  - 월드 용량 제한 명시 (Starter 300MB, Pro 이상 800MB)
  - Actor 수 확정 (Free/Starter 1개, Pro 2개, Studio 4개, Enterprise 6개+)
  - 동시 방 보유 1개 정책 확정 (Pro/Studio)
  - Free → Starter 전환 유도 전략 섹션 추가 (워터마크/시간제한/기능잠금 옵션)
  - Studio 조직 시트(Organization Sheet) 검토 중 표기
  - 서버 전용 저장 정책 명시 (로컬 저장 제거)
  - **Actor 개념 정립**: "방 최대 인원" → "세션 최대 Actor"로 용어 변경, 개인 Actor 수와 세션 최대 Actor 구분 명확화
  - **Manager도 1 Actor로 계산**: 아바타 없이 참여해도 세션 Actor 수에 포함
  - **Free/Starter 세션 참가 제한**: 멀티플레이어 세션에서 Manager로만 참여 가능
  - **세션 권한 이전 정책**: Creator/Manager 역할 무관, Pro 이상 플랜이면 세션 유지
- **03_Operations/01_User_Roles.md** (v1.1 → v1.2): 플랜별 역할 제한 반영
  - Manager도 1 Actor로 계산됨 명시
  - 플랜별 역할 제한 테이블 추가 (Free/Starter는 세션에서 Manager로만 참여)
- **02_Features/01_Avatar_System.md** (v1.1 → v1.2): 저장 정책 구체화
  - 아바타 슬롯 50개, 200MB/개 제한 테이블 추가
  - Actor 수 라이선스 체계와 동기화 (Studio 4개, Enterprise 6개+)
  - Actor 개념 설명 추가 (1명이 여러 Actor 운용 가능, 세션은 Actor 수로 제한)
  - 서버 전용 저장 정책 명시 (로컬 저장 제거)
  - 엣지 케이스에 슬롯/용량 초과 대응 추가
- **02_Features/04_World_System.md** (v1.0 → v1.1): 업로드 제한 구체화
  - 월드 용량 제한 테이블 추가 (Starter 300MB, Pro 이상 800MB)
  - 서버 전용 저장 정책 명시 (로컬 저장 제거)
  - 업로드 흐름에 용량 검증 단계 추가
- **02_Features/05_Network_System.md** (v1.1 → v1.2): Actor 기반 세션 제한 개념 반영
  - 최대 플레이어 100명 → n명 (검토 중)으로 변경
  - 플레이어 vs Actor 개념 구분 설명 추가
  - 세션 최대 Actor (호스트 플랜 기준) 개념 명시
- **01_Product/01_Product_Overview.md** (v1.0 → v1.1): 5티어 플랜 및 Actor 개념 반영
  - 라이선스 항목에 Starter 플랜 추가
  - "최대 100명" → "플랜별 세션 최대 Actor 제한"으로 변경
- **01_Product/02_User_Flow.md** (v1.1 → v1.2): Actor 기반 제한 반영
  - 월드 참가 시 "인원 확인" → "세션 Actor 수 확인"으로 변경
  - 엣지 케이스 "100명 초과" → "세션 최대 Actor 초과"로 변경

### 수정됨 (서버 개발자 회의 1차 내용 반영)
- **05_Technical/01_Architecture.md**: 서버 아키텍처 전환 검토 섹션 추가 (2.7절)
  - Spring Boot 4.0 + PostgreSQL + Cloudflare R2 전환 검토안
  - JWT 토큰 구조, 데이터 흐름 정리
  - 미확정 사항 (Refresh Token 기간, Firebase 유지 범위 등)
- **03_Operations/06_Account_System.md**: 인증 흐름 전환 검토 섹션 추가 (2.5절)
  - Steam OAuth → Firebase Auth → JWT 흐름
  - Tenant 개념 도입, 계정 복구 흐름
- **03_Operations/03_Security.md**: 보안 아키텍처 전환 검토 섹션 추가 (2.8절)
  - JWT 기반 인증 보안, Photon Custom Auth
  - Photon Webhook Secret 검증, R2 Signed URL 보안
- **02_Features/01_Avatar_System.md**: 아바타 저장/관리 전환 검토 내용 추가
  - R2 Signed URL 기반 업로드/다운로드 흐름
  - fileHash 캐시 검증, Resolve API 검토
- **02_Features/05_Network_System.md**: 세션 관리 전환 검토 섹션 추가 (2.16절)
  - Backend 경유 세션 생성/종료 흐름
  - Photon Webhook 이벤트, 세션 데이터 모델
  - Photon Custom Authentication
- **03_Operations/01_User_Roles.md**: 테넌트 내 권한 체계 검토 섹션 추가 (2.6절)
  - Owner/Admin/Member 관리 권한과 Creator/Manager 프로덕션 역할 분리
- **03_Operations/02_License_System.md**: Actor/Seat 개념 섹션 추가 (2.5절)
  - 플랜별 Actor 수 제한 확정 (서버 측 검증)
  - Seat 기반 멤버 초대 개념 (검토 중)
- **01_Product/02_User_Flow.md**: 로그인/로비 흐름 전환 검토 추가
  - Steam 주 인증 전환 흐름 (2.2.4절)
  - 로비 데이터 로딩 전략 (Pre-load/Lazy Load) (2.3.2절)

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
