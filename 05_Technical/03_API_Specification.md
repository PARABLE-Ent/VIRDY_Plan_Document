# API 명세

> **문서 버전**: 1.0
> **최종 수정일**: 26.02.03 18:00
> **작성자**: 임경섭

---

## 1. 개요

이 문서는 VIRDY 서버 아키텍처 전환 검토(서버 개발자 회의, 2026.02)에서 논의된 API 엔드포인트를 정리한다. 현행 Firebase Functions 기반 API와 전환 검토 중인 Spring Boot REST API를 모두 포함한다.

> 🚧 전환 검토 중인 API는 비용 및 기술적 타당성에 따라 변동될 수 있다. 확정 시 본 문서를 최종 명세로 갱신한다.

---

## 2. 핵심 기획

### 2.1 현행 API (Firebase Functions)

현재 클라이언트에서 사용 중인 Firebase Functions 기반 서버 함수이다.

| 함수명 | 용도 | 호출 방식 |
|--------|------|----------|
| signUpV2 | 회원가입 (계정 생성 + Firestore 저장) | Firebase Functions 직접 호출 |
| getEmailByUsername | 사용자명 → 이메일 조회 | Firebase Functions 직접 호출 |
| saveWorld | 월드 메타데이터 저장 | Firebase Functions 직접 호출 |
| deleteWorld | 월드 삭제 (Firestore + Storage 정리) | Firebase Functions 직접 호출 |
| getWorldData | 월드 메타데이터 조회 | Firebase Functions 직접 호출 |
| resetPasswordV2 | 비밀번호 리셋 이메일 발송 | Firebase Functions 직접 호출 |

### 2.2 전환 검토 중인 API (Spring Boot REST)

> 🚧 아래 내용은 서버 개발자 회의(2026.02) 기반 검토 사항이다. 비용 및 기술적 타당성에 따라 변동될 수 있다.

서버 아키텍처 전환 시 도입 예정인 REST API 목록이다. 모든 API는 `Authorization: Bearer {access_token}` 헤더로 인증한다 (인증 API 제외).

#### 2.2.1 인증 API

| Method | Endpoint | 설명 | 인증 |
|--------|----------|------|------|
| POST | `/api/v1/auth/login` | 로그인 (Firebase Token → JWT 발급) | Firebase Token |
| POST | `/api/v1/auth/refresh` | Access Token 갱신 | Refresh Token |
| POST | `/api/v1/auth/logout` | 로그아웃 (토큰 무효화) | JWT |

**로그인 요청/응답 흐름:**

| 단계 | 동작 |
|------|------|
| 요청 | Firebase Token을 Body에 포함하여 전송 |
| Backend 처리 | Firebase에 Token 검증 요청 → 신규 사용자면 Account/Tenant 자동 생성 |
| 응답 | JWT (Access Token + Refresh Token) 반환 |

**JWT Payload 포함 정보:**
- userId (VIRDY 내부 ID)
- tenantId
- role (Owner / Admin / Member)
- subscriptionPlan

#### 2.2.2 아바타 API

| Method | Endpoint | 설명 |
|--------|----------|------|
| GET | `/api/v1/avatars` | 아바타 목록 조회 (이름, 크기, hash, 수정일) |
| POST | `/api/v1/avatars/upload/init` | 업로드 Signed URL 발급 요청 |
| POST | `/api/v1/avatars/upload/complete` | 업로드 완료 알림 → 메타데이터 DB 저장 |
| POST | `/api/v1/avatars/download` | 다운로드 Signed URL 발급 (배치, avatarId 목록) |
| DELETE | `/api/v1/avatars/{id}` | 아바타 삭제 |

**아바타 목록 응답 구조 (검토 중):**

| 필드 | 타입 | 설명 |
|------|------|------|
| id | Long | 아바타 고유 ID |
| name | String | 아바타 이름 |
| fileSize | Long | 파일 크기 (bytes) |
| fileHash | String | 캐시 비교용 해시 |
| createdAt | DateTime | 생성일 |
| updatedAt | DateTime | 수정일 |

**향후 최적화: Resolve API (검토 중)**

| Method | Endpoint | 설명 |
|--------|----------|------|
| POST | `/api/v1/avatars/resolve` | 클라이언트 캐시 hash 목록 전송 → 변경분만 Signed URL 반환 |

클라이언트가 보유한 `[avatarId: hash]` 목록을 서버에 전송하면, 서버가 변경된 아바타만 Signed URL과 함께 반환한다. 불필요한 URL 발급과 조회를 줄이는 최적화 방안이다.

#### 2.2.3 세션 API

| Method | Endpoint | 설명 |
|--------|----------|------|
| POST | `/api/v1/sessions` | 세션 생성 (joinCode 발급) |
| GET | `/api/v1/sessions/{joinCode}` | 세션 정보 조회 |
| POST | `/api/v1/sessions/{id}/close` | 세션 종료 요청 |

#### 2.2.4 Photon Webhook 수신

Backend가 Photon으로부터 수신하는 Webhook 엔드포인트이다. Webhook Secret으로 요청 무결성을 검증한다.

| Method | Endpoint | 설명 |
|--------|----------|------|
| POST | `/webhook/photon/room-created` | Room 생성 이벤트 → photonRoomId 매핑 저장 |
| POST | `/webhook/photon/room-closed` | Room 종료 이벤트 → 세션 상태 CLOSED |
| POST | `/webhook/photon/player-joined` | 플레이어 입장 → currentParticipants 증가 |
| POST | `/webhook/photon/player-left` | 플레이어 퇴장 → currentParticipants 감소 |

#### 2.2.5 기타 API (향후 추가 예정)

| 영역 | 예상 엔드포인트 | 상태 |
|------|----------------|------|
| 친구 관리 | `/api/v1/friends` | 📋 미설계 |
| 구독 관리 | `/api/v1/subscription` | 📋 미설계 |
| Actor 설정 | `/api/v1/actors` | 📋 미설계 |
| 장비 프리셋 | `/api/v1/presets` | 📋 미설계 |
| 월드 관리 | `/api/v1/worlds` | 📋 미설계 |
| 테넌트 전환 | `/api/v1/auth/switch-tenant` | 📋 미설계 |
| 로비 통합 | `/api/v1/lobby/init` | 📋 미설계 (로비 진입 시 병렬 호출 최적화) |

---

## 3. 설계 시 고려사항

### 3.1 API 버전 관리

모든 API는 `/api/v1/` 접두사를 사용하여 버전 관리한다. 호환성이 깨지는 변경 시 `/api/v2/`로 새 버전을 추가하고, 기존 버전은 일정 기간 유지한다.

### 3.2 인증 및 권한 검증

| 항목 | 설명 |
|------|------|
| 인증 방식 | JWT Bearer Token (Authorization 헤더) |
| 권한 검증 | JWT Payload의 role, subscriptionPlan으로 엔드포인트별 접근 제어 |
| 테넌트 격리 | JWT의 tenantId로 데이터 격리 보장 |

### 3.3 에러 응답 형식

| 필드 | 설명 |
|------|------|
| success | false |
| error.code | 에러 코드 (예: AUTH_EXPIRED, FORBIDDEN) |
| error.message | 사용자 표시용 메시지 |

### 3.4 Signed URL 보안

| 항목 | 설명 |
|------|------|
| 유효 기간 | 시간 제한 (업로드: 30분, 다운로드: 1시간 등) |
| 단방향 | 업로드용 URL로 다운로드 불가, 그 반대도 불가 |
| 권한 확인 | URL 발급 전 JWT로 소유권 확인 |

---

## 4. 엣지 케이스 및 예외 처리

| 상황 | 대응 |
|------|------|
| Access Token 만료 | 401 응답 → 클라이언트가 Refresh Token으로 갱신 |
| Refresh Token 만료 | 401 응답 → Steam 재로그인 유도 |
| 권한 부족 (무료 플랜에서 세션 생성) | 403 응답 + 업그레이드 안내 |
| Signed URL 만료 후 업로드 시도 | 403 응답 → 새 URL 발급 요청 유도 |
| Webhook Secret 불일치 | 401 응답 → 이벤트 무시 |
| 동시 세션 한도 초과 | 429 응답 → 기존 세션 종료 유도 |

---

## 5. 미결정 쟁점

| 항목 | 상태 | 비고 |
|------|------|------|
| Access Token 만료 시 자동 갱신 타이밍 | 📋 논의 필요 | 만료 5분 전 자동 갱신 vs 만료 후 갱신 |
| Resolve API 도입 시점 | 📋 논의 필요 | MVP에서 도입 vs 이후 최적화 |
| 로비 통합 API 도입 여부 | 📋 논의 필요 | 개별 API 병렬 호출 vs 통합 API |
| 월드 관리 API 상세 설계 | 📋 미설계 | 월드 기획 확정 후 |
| 장비 프리셋 저장 방식 | 📋 논의 필요 | 서버 저장 vs 로컬 저장 |
| Rate Limiting 정책 | 📋 미설계 | API별 호출 제한 |

---

## 6. 향후 확장 가능성

| 항목 | 설명 | 우선순위 |
|------|------|---------|
| **인증/아바타/세션 API 구현** | 서버 개발자 회의에서 확정된 핵심 API | 높음 |
| **Webhook 연동 구현** | Photon Webhook 수신 및 처리 | 높음 |
| **친구/소셜 API** | 친구 관리, 온라인 상태 | 중간 |
| **구독/결제 API** | Stripe 연동, 구독 상태 관리 | 중간 |
| **월드 관리 API** | 월드 업로드/다운로드/공유 | 중간 |
| **Resolve API** | 아바타 캐시 최적화 | 낮음 |
| **로비 통합 API** | 로비 진입 시 단일 호출로 필요 데이터 수신 | 낮음 |

---

## 관련 문서

- [기술 아키텍처](./01_Architecture.md)
- [개발 현황](./02_Development_Status.md)
- [아바타 시스템](../02_Features/01_Avatar_System.md)
- [네트워크 시스템](../02_Features/05_Network_System.md)
- [보안 시스템](../03_Operations/03_Security.md)
- [계정 시스템](../03_Operations/06_Account_System.md)
