# 월드 시스템

> **문서 버전**: 1.1
> **최종 수정일**: 26.02.03 20:00
> **작성자**: 임경섭

---

## 1. 개요

월드(World)는 VIRDY에서 사용자들이 실시간으로 모여 방송하고 협업하는 가상 공간이다. 사용자는 VIRDY SDK로 Unity 씬을 월드로 빌드하여 업로드하고, 다른 사용자와 공유할 수 있다. 월드는 AssetBundle로 패키징되어 서버(클라우드)에 저장되며, Photon 세션을 통해 멀티유저 환경을 제공한다.

> 🚧 모든 월드 데이터는 **서버(클라우드)에만 저장**되며, 로컬 저장 방식은 사용하지 않는다. 클라이언트는 서버에서 다운로드 받아 사용하고, 로컬 캐시는 성능 최적화 목적으로만 사용한다.

---

## 2. 핵심 기획

### 2.1 월드 구성요소

| 구성요소 | 설명 |
|----------|------|
| **WorldData** | 월드 메타데이터 (제목, 설명, 공개설정, 버전 등) |
| **AssetBundle** | Unity 씬이 패키징된 번들 파일 |
| **VIRDYWorldDescriptor** | 월드 설정 컴포넌트 (스폰 포인트, 라이팅, 렌더러) |
| **Photon Session** | 실시간 멀티유저 세션 |

### 2.2 월드 데이터 구조

#### 기본 정보

| 필드 | 설명 |
|------|------|
| worldId | 고유 식별자 (형식: vw_{GUID}) |
| title | 월드 이름 |
| author | 제작자 이름 |
| authorId | 제작자 사용자 ID |
| description | 월드 설명 |
| sceneName | AssetBundle 내 씬 경로 |
| fileSize | 파일 크기 (표시용) |

#### 버전 및 통계

| 필드 | 설명 |
|------|------|
| version | 버전 번호 (업데이트 시 증가) |
| create | 생성 시간 |
| update | 수정 시간 |
| visits | 방문 횟수 |

#### 썸네일

| 항목 | 설명 |
|------|------|
| 개수 | 3장 |
| 포맷 | png, jpg 등 |
| 저장 | Firebase Storage |

### 2.3 월드 공개 설정

| 유형 | 설명 | 접근 가능 사용자 |
|------|------|----------------|
| **Public** | 모든 사용자에게 공개 | 전체 |
| **Private** | 제작자만 접근 가능 | 제작자 |
| **Private+** | 제작자 + 지정 사용자 | 제작자 + 공유 대상 |

### 2.4 월드 로딩 파이프라인

| 단계 | 동작 | 설명 |
|------|------|------|
| 1 | 메타데이터 다운로드 | Firebase Functions로 월드 데이터 요청 |
| 2 | AssetBundle 다운로드 | Firebase Storage에서 다운로드 (또는 로컬 캐시 사용) |
| 3 | AssetBundle 로드 | 메모리에 번들 로드 |
| 4 | 씬 로드  | 월드 씬 로드 |
| 5 | 렌더링 설정 | 월드 렌더러 Feature 병합, 필수 기능(NiloToon, ToonLit 등) 보장 |
| 7 | SDK 컴포넌트 초기화 | VIRDYBehaviour, VIRDYNetworkBehaviour 초기화 호출 |

#### 씬 초기화 시 자동 처리

| 항목 | 동작 |
|------|------|
| EventSystem | 자동 비활성화 (VIRDY 메인 EventSystem과 충돌 방지) |
| Camera | 자동 비활성화 (VIRDY 카메라 시스템 사용) |
| AudioListener | 자동 비활성화 (메인 AudioListener 사용) |
| 레이어 > 29 | 자동 재설정 (예약 레이어) |
| 오디오 소스 | AudioMixer "Master/World" 연결 |

### 2.6 월드 업로드 및 관리

#### 업로드 제한

| 항목 | 값 | 비고 |
|------|-----|------|
| 월드 용량 제한 | Starter: 300MB / Pro 이상: 800MB | 플랜별 상이 |
| 저장 위치 | 서버 (클라우드) | 로컬 저장 미지원 |
| 로컬 캐시 | 성능 최적화용 | 원본은 서버에만 존재 |

> Free 플랜은 월드 업로드가 불가능하다. 상세 내용은 [라이선스 체계](../03_Operations/02_License_System.md) 참조.

#### 신규 월드 업로드

| 단계 | 동작 |
|------|------|
| 1 | 파일 다이얼로그로 AssetBundle 파일 선택 |
| 2 | 씬 경로 및 파일 크기 추출 |
| 3 | **용량 검증 (플랜별 제한 초과 시 업로드 실패)** |
| 4 | 썸네일 3장 업로드 |
| 5 | AssetBundle을 서버 Storage에 업로드 |
| 6 | DB에 월드 메타데이터 저장 |
| 7 | 버전 번호 초기화 (version = 1) |

#### 월드 업데이트

| 변경 사항 | 동작 |
|----------|------|
| 메타데이터만 변경 (제목, 설명, 공개설정) | Firestore 직접 업데이트 |
| 파일 변경 | 썸네일/AssetBundle 재업로드 + version 증가 |
| 공유 대상 변경 | shared 관련 DB Collection만 업데이트 |

#### 월드 삭제

Firestore 메타데이터 + Storage 파일 + 로컬 캐시(?)를 모두 삭제한다.

### 2.7 월드 목록 관리

| 목록 | 설명 |
|------|------|
| 전체 공개 월드 | worlds_public 컬렉션의 모든 월드 |
| 내 월드 | 내가 제작한 월드 |
| 공유받은 월드 | 다른 사용자가 나에게 공유한 월드 |
| 즐겨찾기 월드 | 즐겨찾기에 추가한 월드 |

#### 정렬 옵션

| 옵션 | 기준 |
|------|------|
| 최신순 | update 내림차순 |
| 오래된순 | update 오름차순 |
| 인기순 | visits 내림차순 |
| 비인기순 | visits 오름차순 |

### 2.8 VIRDYWorldDescriptor

월드 씬에 필수적인 SDK 컴포넌트로, 아래 설정을 포함한다.

| 항목 | 설명 |
|------|------|
| SpawnPoint | 플레이어 스폰 위치 (미설정 시 Descriptor 위치 사용) |
| RendererData | 월드 전용 렌더러 설정 (오버라이드 가능) |
| GlobalVolume | 포스트 프로세싱 볼륨 |
| CustomDirectionalLight | 월드 방향광 (선택) |
| UnityVersion / URPVersion | 빌드 환경 버전 정보 |

렌더러 오버라이드 시, VIRDY는 월드의 렌더러 기능을 적용하되 NiloToon/ToonLit(아바타 렌더링)과 HighlightPlus(하이라이트)는 반드시 보장한다.

### 2.9 런타임 커스터마이징

월드 진입 후 실시간으로 조절할 수 있는 항목이다. 세션 내 모든 유저가 Slider UI를 통해 조작할 수 있으며, 변경 사항은 세션 전체에 실시간으로 동기화된다.

#### 방향광(Directional Light) 제어

| 파라미터 | 범위 | UI | 설명 |
|----------|------|-----|------|
| Intensity | 0~10 | Slider | 광원 강도 |
| Rotation X | 0°~360° | Slider | 수직 회전 (태양 고도) |
| Rotation Y | 0°~360° | Slider | 수평 회전 (태양 방위) |

#### 포스트 프로세싱 제어

| 효과 | 조절 항목 | UI |
|------|----------|-----|
| **Bloom** | Threshold, Intensity, Scatter, Enable | Slider + Toggle |
| **Color Adjustments** | Post Exposure, Contrast, Saturation, Enable | Slider + Toggle |

#### 멀티유저 동기화 플로우

세션 내 Light/PostProcess 값은 **모든 유저에게 공유되는 단일 상태**이다. 누구든 값을 변경하면 세션 전체에 즉시 반영된다.

| 단계 | 동작 | 설명 |
|------|------|------|
| 1 | 유저가 Slider를 조작 | 방향광 Intensity, Rotation 또는 PostProcess 파라미터 변경 |
| 2 | 로컬에 즉시 적용 | 조작한 유저의 화면에 변경값이 즉시 반영 |
| 3 | RPC로 전체 전파 | StateAuthority → 모든 Proxy에 Reliable RPC 전송 |
| 4 | 전체 유저에게 적용 | 세션 내 모든 유저의 화면에 동일한 값이 반영 |

**시나리오 예시:**

> 유저 A, B, C, D가 같은 세션에 접속해 있다.
>
> 1. 유저 A가 Directional Light의 Intensity를 5로 조절한다 → A, B, C, D 모두 Intensity 5가 적용된다.
> 2. 이후 유저 C가 Light의 Rotation X를 45°로 변경한다 → A, B, C, D 모두 Rotation X 45°가 적용된다.
> 3. 유저 B가 Bloom의 Intensity를 높인다 → A, B, C, D 모두 동일한 Bloom Intensity가 적용된다.
>
> 즉, **마지막으로 조작한 유저의 값이 세션 전체의 현재 상태**가 된다.

#### 동기화 특성

| 항목 | 설명 |
|------|------|
| 제어 권한 | 세션 내 모든 유저가 조작 가능 (역할 제한 없음) |
| 동기화 방식 | RPC (StateAuthority → Proxies, Reliable) |
| 적용 범위 | 세션 전체 (모든 접속자에게 동일하게 반영) |
| 충돌 처리 | 마지막 조작값이 최종값 |
| 후속 참가자 | 세션 참가 시 현재 상태값을 수신하여 동기화 |

### 2.10 세션 관리

#### 세션 생성

유저가 월드를 선택하고 "월드 생성" 버튼을 누르면 본인은 세션으로 이동, 4자리 숫자 세션 코드가 생성된다.

#### 세션 참가

| 방법 | 설명 |
|------|------|
| 세션 코드 입력 | 4자리 코드를 입력하여 참가 |
| 친구 초대/따라가기 | 소셜 기능을 통해 참가 |

### 2.11 월드 언로드

월드에서 나갈 때 데이터 및 메모리 정리에 대한 순서가 필요할지 개발팀 문의 예정.

### 2.12 월드 제작 가이드라인

#### 필수 구성요소

| 구성요소 | 필수 여부 | 설명 |
|----------|----------|------|
| VIRDYWorldDescriptor | 필수 | 월드 설정 앵커 |
| Spawn Point Transform | 필수 | 플레이어 스폰 위치 |
| Directional Light | 권장 | 주 광원 |
| Volume (Post Processing) | 권장 | 포스트 프로세싱 |

#### 성능 권장사항

| 항목 | 권장 값 |
|------|---------|
| Draw Calls | 300 미만 |
| 폴리곤 수 | 50만 미만 |
| 텍스처 메모리 | 개별 텍스처 2048 미만 사용 권장 |
| 실시간 광원 | 4개 미만 |
| 라이트맵 | 사용 권장 |

#### 제작 시 주의사항

| 항목 | 설명 |
|------|------|
| Cinemachine Camera 추가 금지 | VIRDY 카메라 시스템과 충돌 |
| AudioListener 추가 금지 | 메인 AudioListener와 충돌 |
| 레이어 30 이상 사용 자제 | 예약된 레이어 |
| 오디오 소스 | AudioMixer "Master/World" 사용 |

---

## 3. 설계 시 고려사항

### 3.1 AssetBundle 호환성

- 월드 AssetBundle은 Streamed Scene AssetBundle이어야 함 (1개 씬)
- Unity 버전 및 URP 버전이 VIRDY 클라이언트와 호환되어야 함
- VIRDYWorldDescriptor에 빌드 환경 버전 정보를 기록하여 호환성 추적

### 3.2 메모리 관리

- AssetBundle 로드 시 메모리 급증 가능 (특히 텍스처가 많은 월드)
- 언로드 시 `Unload(true)`로 완전 해제 필수
- 월드 + 아바타가 동시에 로드되므로 총 메모리 예산 관리 필요

### 3.3 렌더러 병합 시 필수 기능 보장

월드가 커스텀 렌더러를 사용할 경우에도 NiloToon/ToonLit(아바타 셰이더)와 HighlightPlus(상호작용 하이라이트)가 반드시 포함되어야 한다.

### 3.4 네트워크 동기화 범위

메인 라이트 및 포스트 프로세싱 설정 변경은 RPC를 통해 모든 접속자에게 동기화된다. 세션 내 어떤 유저든 Slider를 조작하면 모든 참가자에게 동일하게 적용된다.

- **동기화 대상**: Directional Light (Intensity, Rotation X/Y) + PostProcess (Bloom, Color Adjustments)
- **동기화 단위**: 세션 전체 (개별 유저 단위가 아님)
- **충돌 정책**: Last-Write-Wins — 여러 유저가 동시에 조작할 경우 마지막 RPC가 최종값이 됨
- **늦은 참가자 처리**: 세션에 나중에 참가한 유저도 현재 Light/PostProcess 상태를 수신받아 동기화된 상태로 시작
- **Local 상태 on/off?**: 월드 내 유저들과 동기화되지 않고, 혼자 Local로 전환하여 쓸 수 있는 상태를 만들 것인가? 고민

---

## 4. 엣지 케이스 및 예외 처리

| 상황 | 대응 |
|------|------|
| AssetBundle이 Streamed Scene이 아닌 경우 | 업로드 시 검증 실패, 오류 안내 |
| VIRDYWorldDescriptor가 누락된 월드 | 기본값으로 동작 (스폰 포인트 = 원점) |
| 월드 다운로드 중 네트워크 끊김 | 타임아웃 후 오류 표시, 로비 복귀 |
| 캐시된 월드의 버전이 서버와 불일치 | 서버 버전 다운로드 후 캐시 갱신 |
| 월드 언로드 시 메모리 누수 | Unload(true)로 강제 해제, 이후 GC 호출 |
| 삭제된 월드에 접속 시도 | "월드를 찾을 수 없습니다" 오류, 로비 복귀 |
| 공유 권한이 취소된 월드 접근 | Firestore 보안 규칙으로 차단, 목록에서 자동 제거 |
| 동일 월드 중복 업로드 | 기존 월드 업데이트로 처리 (version 증가) |
| 월드 내 EventSystem/Camera 존재 | 자동 비활성화 처리 |

---

## 5. 향후 확장 가능성

| 항목 | 설명 | 우선순위 |
|------|------|---------|
| **Steam Workshop 연동** | Steam Workshop을 통한 월드 배포 | 중간 |
| **월드 태그/카테고리** | 월드 검색을 위한 태그 시스템 | 중간 |
| **월드 버전 관리** | 이전 버전 롤백 기능 | 낮음 |
| **월드 마켓플레이스** | 커뮤니티 월드 공유/판매 플랫폼 | 장기 |

---

## 관련 문서

- [카메라 시스템](./03_Camera_System.md)
- [네트워크 시스템](./05_Network_System.md)
- [SDK](./06_SDK.md)
- [사용자 플로우](../01_Product/02_User_Flow.md)
- [기술 아키텍처](../05_Technical/01_Architecture.md)
