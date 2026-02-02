# VIRDY 기획 문서

> VIRDY 솔루션의 기획, 설계, 운영 문서를 통합 관리하는 리포지토리

이 리포지토리는 VIRDY의 제품 기획, 기술 설계, 운영 전략을 체계적으로 정리한 문서 허브입니다. 제품 개발의 모든 단계에 걸친 상세한 명세를 제공합니다.

## 개요

VIRDY는 버추얼 크리에이터를 위한 올인원 모션캡처 라이브 스트리밍 솔루션입니다. 이 리포지토리는 5개의 주요 카테고리로 구성된 전체 기획 문서를 포함합니다:

- **Product**: 제품 정의 및 사용자 플로우
- **Features**: 핵심 기능 상세 명세
- **Operations**: 사용자 관리, 라이선스, 보안 정책
- **Design**: UI/UX 명세 및 디자인 가이드라인
- **Technical**: 시스템 아키텍처 및 개발 현황

## 리포지토리 구조

```
VIRDY_Plan_Document/
├── 01_Product/
│   ├── 01_Product_Overview.md
│   └── 02_User_Flow.md
├── 02_Features/
│   ├── 01_Avatar_System.md
│   ├── 02_Tracker_System.md
│   ├── 03_Camera_System.md
│   ├── 04_World_System.md
│   ├── 05_Network_System.md
│   └── 06_SDK.md
├── 03_Operations/
│   ├── 01_User_Roles.md
│   ├── 02_License_System.md
│   ├── 03_Security.md
│   ├── 04_Data_Lifecycle.md
│   ├── 05_Risk_Management.md
│   └── 06_Account_System.md
├── 04_Design/
│   └── 01_UI_Specification.md
└── 05_Technical/
    ├── 01_Architecture.md
    └── 02_Development_Status.md
```

## 최신 업데이트

최근 4주간의 주요 변경사항은 [UPDATES.md](UPDATES.md)에서 확인하세요.
전체 변경 이력은 [CHANGELOG.md](CHANGELOG.md)를 참고하세요.

---

## 빠른 시작

### 문서 확인 방법

**방법 1: HTML 뷰어 (권장)**

`VIRDY_Onboarding.html` 파일을 브라우저에서 열면 사이드바 네비게이션과 최신 업데이트 섹션이 포함된 통합 문서를 확인할 수 있습니다.

```bash
# HTML 파일 열기
start VIRDY_Onboarding.html  # Windows
open VIRDY_Onboarding.html   # macOS
xdg-open VIRDY_Onboarding.html  # Linux
```

**방법 2: 마크다운 파일**

각 카테고리 폴더 내의 개별 `.md` 파일을 직접 확인할 수 있습니다.

**방법 3: Notion**

VIRDY Notion 워크스페이스와 동기화되어 있어 협업 편집 및 댓글 기능을 사용할 수 있습니다.

## 문서 카테고리

### 01_Product (제품 정의)
제품 비전, 타겟 사용자, 핵심 가치 제안을 정의합니다. 인증부터 프로덕션까지 전체 사용자 여정 플로우를 포함합니다.

### 02_Features (핵심 기능)
다음 기능들의 기술 명세를 포함합니다:
- 아바타 시스템 (VRM 지원, BlendShape 설정)
- 트래커 연동 (14종 이상 장비)
- 카메라 시스템 (10채널 가상 카메라)
- 월드 관리 (AssetBundle, 공유 정책)
- 네트워크 동기화 (Photon Fusion)
- SDK (커스텀 콘텐츠 제작)

### 03_Operations (운영 기획)
운영 정책을 다룹니다:
- 사용자 역할 정의 (Creator vs Manager)
- SaaS 라이선스 티어 (Free/Pro/Studio/Enterprise)
- 보안 프로토콜 및 데이터 보호
- 세션 생명주기 관리
- 리스크 완화 전략
- 계정 시스템 아키텍처

### 04_Design (UI/UX)
UI/UX 명세 및 디자인 시스템 가이드라인을 포함합니다.

### 05_Technical (기술 설계)
시스템 아키텍처 문서 및 현재 개발 현황을 추적합니다.

## 문서 형식

모든 기획 문서는 다음의 표준화된 구조를 따릅니다:

```markdown
# 문서 제목

> **문서 버전**: X.X
> **최종 수정일**: YY.MM.DD HH:MM
> **작성자**: 이름

## 1. 개요
## 2. 핵심 기획
## 3. 설계 시 고려사항
## 4. 엣지 케이스 및 예외 처리
## 5. 향후 확장 가능성
```

## 기여하기

이 리포지토리는 VIRDY Studio에서 관리합니다. 기여 또는 제안 사항이 있는 경우:

1. 기존 문서를 먼저 확인하여 맥락을 파악합니다
2. 정해진 문서 형식을 따릅니다
3. 로컬 `.md` 파일과 Notion 워크스페이스 모두에 변경사항이 반영되도록 합니다
4. `generate_onboarding.py`를 실행하여 `VIRDY_Onboarding.html`을 업데이트합니다

## HTML 문서 생성

통합 HTML 문서를 재생성하려면:

```bash
cd VIRDY_Plan_Document
python generate_onboarding.py
```

이 명령은 모든 문서가 통합된 단일 페이지 뷰어인 `VIRDY_Onboarding.html`을 생성합니다.

## 관련 리소스

- **VIRDY Framework**: [Unity 클라이언트 리포지토리](https://github.com/PARABLE-Ent/VIRDY-Framework-Dev)
- **VIRDY Docs**: [공식 문서 사이트](https://parable-ent.github.io/VIRDY-Docs/)
- **Notion 워크스페이스**: VIRDY Planning (내부용)

## 라이선스

Copyright © 2026 VIRDY Studio. All rights reserved.

---

**관리**: VIRDY Studio
**문의**: 공식 채널을 통해 연락주세요
