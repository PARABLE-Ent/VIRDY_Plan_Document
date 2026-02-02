# 기술 아키텍처

> **문서 버전**: 1.0
> **최종 수정일**: 26.01.30 13:20
> **작성자**: 임경섭

---

## 1. 개요

VIRDY는 Unity 2022.3 LTS 기반의 Windows x64 전용 클라이언트 애플리케이션이다. 서버 로직은 Firebase (Auth, Firestore, Storage, Functions)와 Photon Fusion 2에 위임하며, 클라이언트는 3개 씬 구조(Sign → Lobby → World)와 Context 서비스 로케이터 패턴을 중심으로 설계된다.

---

## 2. 핵심 기획

### 2.1 기술 스택

#### 핵심 기술

| 영역 | 기술 | 버전/모드 |
|------|------|-----------|
| 게임 엔진 | Unity | 2022.3.62f3 LTS |
| 렌더 파이프라인 | Universal Render Pipeline (URP) | 14.0.12 |
| 렌더링 모드 | Forward+ | - |
| 네트워킹 | Photon Fusion 2 | Shared Mode |
| 백엔드 | Firebase | Auth, Firestore, Storage, Functions |
| 채팅 | Photon Chat | - |

#### 주요 패키지

| 패키지 | 용도 |
|--------|------|
| UniTask | 비동기/await 유틸리티 |
| UniVRM | VRM 아바타 로딩 |
| Cinemachine | 카메라 시스템 |
| Final IK | 인버스 키네마틱스 |
| Animancer | 애니메이션 상태 머신 |
| MessagePack | 직렬화 |
| Newtonsoft.Json | JSON 파싱 |
| Klak.Spout | Spout 텍스처 공유 (Windows) |
| DOTween | 트윈 애니메이션 |

#### 외부 플러그인

| 플러그인 | 용도 |
|----------|------|
| ParrelSync | 멀티 인스턴스 테스팅 |
| RuntimeTransformHandle | 월드 내 오브젝트 조작 |
| uOSC | OSC 프로토콜 (VMC, VRChat OSC) |
| uWindowCapture | 가상 배경용 윈도우 캡처 |
| VSF SDK | VSeeFace 통합 |

### 2.2 서비스 로케이터 패턴 (Context)

VIRDY는 Context 싱글톤을 통해 전역 서비스에 접근하는 서비스 로케이터 패턴을 사용한다.

#### Context에 등록된 서비스

| 서비스 | 역할 |
|--------|------|
| SceneService | 씬 수명주기 관리, 씬 전환 |
| FirebaseService | Firebase 인증/데이터/스토리지 통합 |
| FusionService | Photon Fusion 세션 관리 |
| Database | 로컬 데이터 캐시 |
| ActorManager | 액터 생성/삭제/관리 |
| ChatService | Photon Chat 메시징 |
| Cache | 에셋(아바타, 월드) 캐싱 |
| KeyBinder | 전역 키보드 단축키 |
| AppSettings | 앱 설정 (그래픽, 사운드 등) |
| HubSettings | 모션캡처 허브 설정 |

모든 서비스는 Context의 static 필드로 접근하며, 씬 전환과 무관하게 유지된다.

### 2.3 씬 구조

VIRDY는 3개의 핵심 씬과 추가 로드(Additive)되는 월드 씬으로 구성된다.

| 씬 | 빌드 인덱스 | 역할 |
|----|-------------|------|
| SignScene | 0 | 인증 (로그인, 회원가입, 비밀번호 리셋) |
| LobbyScene | 1 | 설정 (액터, 아바타, 트래커, 월드 선택) |
| WorldScene | 2 | 실시간 방송 (카메라, 채팅, 멀티유저) |
| AssetBundle 월드 | Additive | WorldScene 위에 Additive 로드되는 사용자 월드 |

#### 씬 전환 이벤트

| 이벤트 | 발생 시점 |
|--------|-----------|
| OnLobbyConnected | 로비 씬 로드 완료 |
| OnWorldConnected | 월드 씬 + 네트워크 접속 완료 |
| OnWorldDisconnected | 월드에서 로비로 복귀 |
| OnWorldConnectionFailed | 월드 접속 실패 |

### 2.4 엔티티 시스템

VIRDY 내부의 데이터 모델은 3개 계층으로 구성된다.

| 계층 | 역할 | 주요 클래스 |
|------|------|-------------|
| Entity | GUID 기반 식별, 생명주기 관리 | EntityManager 자동 등록 |
| StructuredData | 복잡한 런타임 데이터 | AvatarData, TrackerData, ChannelData |
| Asset | 직렬화 가능한 씬 오브젝트 | ActorAsset (JSON 저장/로드) |

#### StructuredData 세부 구조

| 데이터 클래스 | 하위 클래스 |
|---------------|-------------|
| TrackerData (추상) | FacialTrackerData, MotionTrackerData, HandTrackerData |
| FacialTrackerData | iFacialMocap, VTubeStudio, Facemotion3D, OpenSeeFace |
| MotionTrackerData | SteamVR, VMCProtocol, Xsens, Vicon, MOVIN |
| HandTrackerData | LeapMotion, Manus, Mollisen, StretchSense |

#### FieldData 시스템

StructuredData는 리플렉션 기반 속성 시스템(FieldData)을 사용한다. `[FieldData]` 어트리뷰트가 적용된 필드는 동적 get/set이 가능하며, 값 변경 시 `OnFieldDataChanged` 이벤트가 트리거된다.

### 2.5 네트워크 오브젝트 계층

Photon Fusion 2 Shared Mode로 동작하며, 네트워크 오브젝트는 아래 구조를 따른다.

| 네트워크 오브젝트 | 역할 | 주요 데이터 |
|-------------------|------|-------------|
| NetworkGame | 세션 루트 | Players[255], Channels[255], Actors[] |
| NetworkPlayer | 사용자당 1개 | UserId, Username, IsCreator, HandlePosition/Rotation |
| NetworkChannel | 사용자당 1개 | 10개 가상 카메라 데이터, Channel Link 상태, 포스트 프로세싱 |
| NetworkActor | 아바타당 1개 | 22개 본 회전, 40개 손가락 포즈, 100개 BlendShape, Props |

#### 데이터 압축

| 데이터 | 원본 크기 | 압축 후 | 절감률 |
|--------|----------|--------|--------|
| Quaternion | 16 bytes (float×4) | 8 bytes (short×4) | 50% |
| BlendShape | 4 bytes (float) | 1 byte (sbyte) | 75% |
| Position | float3 | Accuracy(0.1f) 양자화 | 가변 |

#### 네트워크 최적화 기법

| 기법 | 설명 |
|------|------|
| 분산 업데이트 | 프레임당 최대 3명 액터만 업데이트 (라운드 로빈) |
| 히스토리 보간 | 2프레임 히스토리 버퍼를 사용한 보간 |
| 변경 감지 | 변경된 데이터만 전송 |
| 양자화 | [Networked, Accuracy()] 속성으로 데이터 양자화 |

### 2.6 Firebase 통합 구조

Firebase 서비스는 4개 하위 모듈로 구성된다.

| 모듈 | 역할 | 주요 기능 |
|------|------|-----------|
| Auth (FBAuth) | 인증 | 이메일 로그인, 사용자명 로그인, 회원가입, 비밀번호 리셋 |
| Firestore (FBFirestore) | 데이터 | 사용자/월드 데이터 CRUD, 친구 관리, 실시간 리스너 |
| Storage (FBStorage) | 파일 저장 | 아바타/월드 업로드/다운로드 |
| Functions | 서버 로직 | signUpV2, resetPasswordV2, saveWorld, deleteWorld, getEmailByUsername |

#### Firestore 데이터 구조

| 컬렉션 | 주요 필드 |
|--------|-----------|
| users/{userId} | username, email, isCreator |
| users/{userId}/avatars/{avatarId} | 아바타 메타데이터 |
| users/{userId}/friends/{friendId} | 친구 관계 |
| users/{userId}/requests/{requestId} | 친구 요청 |
| users/{userId}/favorites/{worldId} | 즐겨찾기 월드 |
| users/{userId}/shared/{worldId} | 공유받은 월드 |
| users/{userId}/worlds_private/{worldId} | 비공개 월드 |
| worlds_public/{worldId} | title, author, authorId, description, sceneName, isPublic, sharedWith, version, visits, urls[] |

### 2.7 빌드 변형

| 스크립팅 심볼 | 설명 |
|---------------|------|
| VIRDY_CORE | 프레임워크 빌드 |
| VIRDY_DOTWEEN | DOTween 애니메이션 활성화 |

### 2.8 프로젝트 폴더 구조

| 폴더 | 역할 |
|------|------|
| Assets/Repack/Scripts/Data/ | 데이터 모델 (Entity, StructuredData, Asset) |
| Assets/Repack/Scripts/Database/ | 로컬 캐시 |
| Assets/Repack/Scripts/Lobby/ | 로비 씬 로직 |
| Assets/Repack/Scripts/Network/Firebase/ | Firebase 통합 |
| Assets/Repack/Scripts/Network/Photon/ | Photon Fusion/Chat |
| Assets/Repack/Scripts/Scene/ | 씬 관리 |
| Assets/Repack/Scripts/Sign/ | 인증 UI |
| Assets/Repack/Scripts/Utility/ | 유틸리티 (Context 포함) |
| Assets/Repack/Scripts/World/ | 월드 씬 로직 |
| Assets/VIRDY-SDK/ | SDK (Editor, Runtime, Samples) |
| Assets/ExternalPlugins/ | 외부 플러그인 |

### 2.9 배포 플랫폼

| 플랫폼 | 상태 | 비고 |
|--------|------|------|
| Windows x64 | ✅ 지원 | 주요 플랫폼 |
| Steam | 📋 계획 | 상용화 시 출시 예정 |
| macOS | ❌ 미지원 | Spout, 일부 트래커 미지원 |

---

## 3. 설계 시 고려사항

### 3.1 성능 최적화

#### 아바타

| 항목 | 권장 사항 |
|------|-----------|
| BlendShape 수 | 제한 권장 (프레임당 CPU 비용 높음) |
| 메시 LOD | 원거리 액터에 적용 검토 |
| 애니메이션 | 절차적 IK 대신 베이킹 우선 |

#### 네트워크 대역폭

| 항목 | 설명 |
|------|------|
| 주요 소비 | 액터 본 업데이트 |
| 대규모 세션 | 액터 수 감소 권장 |
| 고정 카메라 | FreeCam보다 전송 빈도 낮음 |

#### 렌더링

| 항목 | 설명 |
|------|------|
| 렌더 스케일 | 카메라별 조절 가능 |
| 포스트 프로세싱 | 모니터링 카메라에서는 비활성화 권장 |
| Spout 모드 | 별도 렌더 타겟 사용 (메모리 집약적) |

#### 메모리 관리

| 항목 | 조치 |
|------|------|
| AssetBundle | 월드 퇴장 후 Unload(true) 호출 |
| 아바타 캐시 | 주기적 정리 |
| 텍스처 메모리 | 모니터링 필요 (아바타 텍스처 용량이 큼) |

### 3.2 Context 패턴의 장단점

| 장점 | 단점 |
|------|------|
| 서비스 접근이 간편 | 테스트 시 mock 주입 어려움 |
| 씬 전환 시에도 서비스 유지 | 의존성이 명시적이지 않음 |
| 초기 설정이 단순 | 서비스 간 순환 참조 가능성 |

향후 의존성 주입(DI) 컨테이너로의 전환을 고려할 수 있다.

### 3.3 Shared Mode의 특성

Photon Fusion 2 Shared Mode는 서버 권한(Server Authority) 없이 클라이언트 간 데이터를 동기화한다. 각 클라이언트가 자신의 NetworkObject에 대한 State Authority를 갖는다.

| 특성 | 설명 |
|------|------|
| 서버 권한 | 없음 (각 클라이언트가 자체 객체 권한) |
| 장점 | 구현 단순, 지연 시간 낮음 |
| 단점 | 치트 방지 어려움, 서버 측 검증 불가 |
| 적합 | 협업/방송 환경 (경쟁적 요소 적음) |

---

## 4. 엣지 케이스 및 예외 처리

| 상황 | 대응 |
|------|------|
| Context 초기화 전 서비스 접근 | null 체크 또는 초기화 순서 보장 |
| 씬 전환 중 비동기 작업 | UniTask CancellationToken으로 취소 처리 |
| AssetBundle 로드 실패 | 에러 다이얼로그 표시, 로비로 복귀 |
| Photon 세션 연결 실패 | 재시도 로직 + 사용자 알림 |
| Firebase 서비스 장애 | 오프라인 캐시 활용 (제한적), 에러 안내 |
| 네트워크 오브젝트 소유권 충돌 | State Authority 기반 충돌 해소 |
| 대규모 세션에서 성능 저하 | 프레임당 액터 업데이트 수 제한 (라운드 로빈) |

---

## 5. 향후 확장 가능성

| 항목 | 설명 | 우선순위 |
|------|------|----------|
| **DI 컨테이너 도입** | Context 서비스 로케이터를 DI 컨테이너로 교체 | 중간 |
| **ECS 전환** | 대규모 액터 처리를 위한 Entity Component System 검토 | 장기 |
| **서버 권한 모드** | 경쟁적 기능 추가 시 Host Mode 전환 검토 | 장기 |
| **자동 테스트 파이프라인** | CI/CD 연동 자동 빌드 및 테스트 | 중간 |
| **코드 모듈화** | 패키지 매니저 기반 모듈 분리 | 낮음 |

---

## 관련 문서

- [개발 현황](./02_Development_Status.md)
- [네트워크 시스템](../02_Features/05_Network_System.md)
- [보안 시스템](../03_Operations/03_Security.md)
- [제품 개요](../01_Product/01_Product_Overview.md)
