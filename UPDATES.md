# 📋 최신 업데이트

> 최근 4주간의 주요 변경사항을 확인할 수 있습니다.

전체 변경 이력은 [CHANGELOG.md](CHANGELOG.md)를 참고하세요.

---

## 2026년 2월 1주차 (02.03 - 02.04)

### 🔧 서버 개발자 회의 2차 내용 반영

**플랜 구조 확정 및 Actor 개념 정립**
- 5단계 티어 체계 확정 (Free/Starter/Pro/Studio/Enterprise)
- "방 최대 인원" → "세션 최대 Actor"로 용어 변경
- 개인 Actor 수와 세션 최대 Actor 구분 명확화
- Actor 수 확정: Free/Starter 1개, Pro 2개, Studio 4개, Enterprise 6개+

**Manager 및 Free/Starter 정책 확정**
- Manager도 1 Actor로 계산 (아바타 없이 참여해도 세션 Actor 수에 포함)
- Free/Starter 세션 참가 제한: 멀티플레이어 세션에서 Manager로만 참여 가능
- 세션 권한 이전 정책: Creator/Manager 역할 무관, Pro 이상 플랜이면 세션 유지

**저장 및 용량 정책**
- 아바타 슬롯 50개, 200MB/개 제한 명시
- 월드 용량 제한: Starter 300MB, Pro 이상 800MB
- 서버 전용 저장 정책 명시 (로컬 저장 제거)

### 📄 API 명세 문서 신규 작성
- 현행 Firebase Functions API 정리
- 전환 검토 중인 Spring Boot REST API (인증, 아바타, 세션, Webhook)
- Signed URL 보안 정책, 에러 응답 형식

### 🔧 서버 개발자 회의 1차 내용 반영
- 서버 아키텍처 전환 검토 (Spring Boot 4.0 + PostgreSQL + Cloudflare R2)
- 인증 흐름 전환 검토 (Steam OAuth → Firebase Auth → JWT)
- 테넌트 내 권한 체계 검토 (Owner/Admin/Member)
- Photon Custom Authentication 및 Webhook 흐름 추가

---

## 2026년 1월 5주차 (01.30 - 02.02)

### 📝 문서 시스템 개선
- CHANGELOG.md 추가: 전체 변경 이력 추적
- UPDATES.md 추가: 최근 4주 업데이트 요약
- `_updates/` 폴더: 주간 상세 리포트
- HTML 온보딩 문서 자동 생성 시스템 (`generate_onboarding.py`)
- 통합 HTML 문서 뷰어 (`VIRDY_Onboarding.html`)

### 💰 비용 분석 문서 신규 작성
- 사용자별 월간 원가 산출 (Light/Heavy/Worst Case)
- 플랜별 마진 분석 (Starter 96%, Pro 56%)
- 손익분기점(BEP) 분석 (서버 비용 기준 56명)
- 5단계 비용 방어 체계 상세 명세
- Photon/GCP/R2 비용 구성 요소 상세 분석

### 🔄 용어 통일
- "Photon Fusion 2" → "Photon Fusion" 전체 문서 용어 통일

---

## 2026년 1월 4주차 (01.23 - 01.29)

### 📄 초기 문서 작성 완료
- 17개 기획 문서 초안 완성
- 5개 카테고리별 구조화 (Product, Features, Operations, Design, Technical)
- 표준 문서 형식 확립 (개요, 핵심 기획, 설계 고려사항, 엣지 케이스, 향후 확장)
- 문서 버전, 최종 수정일, 작성자 메타데이터 포함

---

## 업데이트 확인 방법

### 📌 빠른 확인
이 파일에서 최근 4주간의 주요 변경사항을 확인하세요.

### 📚 상세 확인
`_updates/YYYY-MM-weekX.md` 파일에서 주간 회의 내용과 상세 변경 이유를 확인하세요.

### 📖 전체 이력
[CHANGELOG.md](CHANGELOG.md)에서 프로젝트 전체 변경 이력을 확인하세요.

### 🌐 HTML 뷰어
`VIRDY_Onboarding_v2.html`을 열면 사이드바에서 최신 업데이트를 확인할 수 있습니다.

---

**마지막 업데이트**: 2026.02.04
