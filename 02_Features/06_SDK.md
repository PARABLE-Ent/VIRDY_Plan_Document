# SDK

> **문서 버전**: 1.0
> **최종 수정일**: 26.01.30 13:20
> **작성자**: 임경섭

---

## 1. 개요

VIRDY SDK는 월드 및 아바타 크리에이터가 커스텀 인터랙티브 콘텐츠를 제작할 수 있도록 제공하는 Unity 패키지이다. SDK를 사용하면 3D 월드를 AssetBundle로 빌드하고, 네트워크 동기화가 가능한 인터랙티브 오브젝트를 추가하며, 자체 확장자 아바타를 빌드할 수 있다.

---

## 2. 핵심 기획

### 2.1 SDK 패키지 정보

| 항목 | 내용 |
|------|------|
| 패키지 이름 | com.parable.virdy-sdk |
| 표시 이름 | VIRDY SDK |
| 지원 Unity | 2022.3 LTS |
| 의존성 | Cinemachine 2.9.7 |
| 배포 상태 | 🚧 개발 중 (외부 배포 예정) |

### 2.2 SDK 구성

| 폴더 | 내용 |
|------|------|
| Editor/ | 에디터 전용 도구 (빌드, 인스펙터) |
| Runtime/ | 핵심 SDK 컴포넌트 |
| Runtime/ShaderController/ | 셰이더 및 비주얼 제어 컴포넌트 |
| Runtime/EX/ | 확장 기능 (PostIt 등) |
| Plugins/uWindowCapture/ | 윈도우 캡처 통합 |
| Samples/ | 예제 씬 및 프리팹 |
| Resources/Settings/ | 기본 설정 |

### 2.3 베이스 클래스

SDK의 모든 인터랙티브 컴포넌트는 아래 2개 베이스 클래스 중 하나를 상속한다.

#### VIRDYBehaviour (비네트워크)

| 항목 | 설명 |
|------|------|
| 용도 | 네트워크 동기화가 필요 없는 인터랙티브 컴포넌트 |
| 생명주기 | Initialize (월드 로드 시) → DeInitialize (월드 언로드 시) |
| 기능 | Transform 위치/회전 원본 저장 및 복원 |
| 사용 예시 | 애니메이션, UI, 조명 효과, 시각 전용 오브젝트 |

#### VIRDYNetworkBehaviour (네트워크)

| 항목 | 설명 |
|------|------|
| 용도 | 네트워크 동기화가 필요한 인터랙티브 컴포넌트 |
| 상속 | Photon Fusion의 NetworkBehaviour |
| 생명주기 | Initialize → DeInitialize (VIRDYBehaviour와 동일) |
| 필수 요구 | NetworkObject 컴포넌트 필요 |
| 기능 | Networked 속성, RPC 메서드 사용 가능 |
| 사용 예시 | 문, 스위치, 동기화 오브젝트, 공유 UI |

### 2.4 VIRDYWorldDescriptor

월드 씬에 필수적인 싱글톤 컴포넌트로, 월드 설정과 초기화를 관리한다.

| 설정 | 설명 |
|------|------|
| SpawnPoint | 아바타 스폰 위치 |
| RendererData | URP 렌더러 설정 (오버라이드 가능) |
| GlobalVolume | 포스트 프로세싱 볼륨 |
| CustomDirectionalLight | 방향광 설정 |
| UnityVersion / URPVersion | 빌드 환경 버전 정보 |

초기화 시 씬 내 모든 VIRDYBehaviour 및 VIRDYNetworkBehaviour를 탐색하여 Initialize를 호출한다.

에디터 생성: Hierarchy 우클릭 → GameObject/VIRDY/VIRDYWorldDescriptor

### 2.5 인터랙티브 컴포넌트

#### VIRDYObjectActivator

| 항목 | 설명 |
|------|------|
| 기능 | 이름으로 오브젝트 그룹 활성화/비활성화 |
| 네트워크 | 불필요 |
| 사용 예시 | 버튼으로 조명/파티클 그룹 토글 |

#### VIRDYGlobalFunction (네트워크)

| 항목 | 설명 |
|------|------|
| 기능 | 키 기반 함수를 모든 플레이어에게 브로드캐스트 |
| 네트워크 | 필요 (RPC) |
| 지원 인자 | 없음 / int / string |
| 사용 예시 | 특수 효과 활성화, 애니메이션 트리거, 이벤트 전파 |

#### VIRDYMultiObjectControl

| 항목 | 설명 |
|------|------|
| 기능 | 오브젝트 배열을 순차적으로 활성화/비활성화 |
| 네트워크 | 불필요 |
| 사용 예시 | 갤러리 이전/다음, 캐러셀 디스플레이 |

#### VIRDYVideoPlayer

| 항목 | 설명 |
|------|------|
| 기능 | 비디오 클립 재생, 페이드 전환, RenderTexture 출력 |
| 네트워크 | 불필요 |
| 구성 | VideoClip + RenderTexture + FadeUI 1:1 매핑 |

#### VIRDYRoulette (네트워크)

| 항목 | 설명 |
|------|------|
| 기능 | 이징 커브 기반 회전 룰렛 |
| 네트워크 | 필요 (동기화된 랜덤 결과) |
| 사용 예시 | 복권, 스핀 게임, 랜덤 결과 표시 |

#### VIRDYInputFieldSync (네트워크)

| 항목 | 설명 |
|------|------|
| 기능 | 텍스트 입력을 여러 UI에 네트워크 브로드캐스트 |
| 네트워크 | 필요 |
| 사용 예시 | 자막 디스플레이, 공유 채팅 |

### 2.6 조명 제어 컴포넌트

#### VIRDYLightController

| 항목 | 설명 |
|------|------|
| 기능 | 포인트 라이트 프리셋 전환, 파티클 효과 토글 |
| 라이트 수 | 최대 3개 포인트 라이트 |
| 프리셋 | 색상(3개), 강도, 범위 조합 |
| 전환 | 부드러운 색상 전환 (Lerp) |

#### VIRDYMirrorBall

| 항목 | 설명 |
|------|------|
| 기능 | HSV 색상 순환 + 회전 + 밝기 제어 |
| 제어 | MusicStart / MusicStop (페이드아웃) |

### 2.7 셰이더 및 VFX 컴포넌트

#### VIRDYMaterialController (네트워크)

| 항목 | 설명 |
|------|------|
| 기능 | 머티리얼 셰이더 속성을 네트워크로 동기화 |
| 입력 | UI 슬라이더(VIRDYMaterialSlider) 또는 직접 float 값 |
| 사용 예시 | 조명 색상/강도 제어, 투명도, 셰이더 파라미터 |

#### VIRDYVFXController (네트워크)

| 항목 | 설명 |
|------|------|
| 기능 | Visual Effect Graph 파라미터를 네트워크로 제어 |
| 지원 속성 | Float, Slider(0~1), Vector2, Gradient(색상 프리셋) |

#### EmissionController

| 항목 | 설명 |
|------|------|
| 기능 | 이름 매칭으로 머티리얼 발광 강도 제어 |
| 사용 예시 | 캐릭터 머티리얼 발광, 네온 효과 |

### 2.8 UI 컴포넌트

#### VIRDYWorldUI

| 항목 | 설명 |
|------|------|
| 기능 | World Space Canvas를 VIRDY 이벤트 카메라에 자동 연결 |
| 설정 | 컴포넌트 추가만으로 자동 설정 |
| 카메라 전환 | 카메라 변경 시 자동 업데이트 |

#### VIRDYScreenUI

| 항목 | 설명 |
|------|------|
| 기능 | Screen Space Camera Canvas 자동 설정 |
| 설정 | 렌더 모드, 레이어, Z-오더 자동 관리 |

#### VIRDYFadeUI

| 항목 | 설명 |
|------|------|
| 기능 | UI 페이드 인/아웃 + 선택적 위치 이동 |
| 애니메이션 | DOTween 기반 (조건부 컴파일: VIRDY_DOTWEEN) |
| 설정 | Duration, Ease In/Out, 위치 시작/끝 |

#### VIRDYCinemachineTrack

| 항목 | 설명 |
|------|------|
| 기능 | Timeline 재생을 활성 카메라 Brain에 자동 바인딩 |
| 사용 예시 | 플레이어 카메라 변경에 적응하는 시네마틱 시퀀스 |

### 2.9 확장 컴포넌트

#### BlendShapeManager

| 항목 | 설명 |
|------|------|
| 기능 | VRM 아바타 BlendShape + 연계 GameObject 제어 |
| 설정 | 대상 인덱스, VRM 메타 타이틀, BlendShape 경로/이름 |
| 사용 예시 | 아바타 커스텀 표정, 바디 모프 |

#### VIRDYPostItController

| 항목 | 설명 |
|------|------|
| 기능 | 물리 기반 포스트잇 부착/분리 시스템 |
| 구성 | PostItStickyController (개별) + VIRDYPaperAero (종이비행기) |
| 연동 | NetworkActor.WriteBuffer에서 틱 호출 |

#### VIRDYVelocity (네트워크)

| 항목 | 설명 |
|------|------|
| 기능 | 네트워크 동기화 물리 힘 (선형 속도 + 토크) |
| 필수 | NetworkObject + NetworkRigidbody + Rigidbody |
| 사용 예시 | 물리 오브젝트, 공, 인터랙티브 소품 |

#### VIRDYTimer

| 항목 | 설명 |
|------|------|
| 기능 | 경과 시간 또는 현재 시간 표시 |
| 출력 | 시/분/초/밀리초 별도 TextMeshPro |
| 제어 | Start / Stop / Reset / GetCurrentTime |

#### OSCReceiver

| 항목 | 설명 |
|------|------|
| 기능 | 외부 OSC 메시지를 VIRDYGlobalFunction으로 라우팅 |
| 연동 | VSeeFace, Resolume 등 OSC 앱 |
| 지원 | 인자 없음, int, string 메시지 |

### 2.10 에디터 도구

#### VIRDYWorldDescriptorEditor

| 기능 | 설명 |
|------|------|
| 렌더러 상태 표시 | URP 기능 목록 (SSAO, HBAO, Volumetric 등) |
| 월드 빌더 | 출력 경로 설정 + 원클릭 AssetBundle 빌드 |
| 빌드 방식 | ChunkBasedCompression, 매니페스트 정리 |

#### 컴포넌트별 에디터

| 에디터 | 기능 |
|--------|------|
| VIRDYFadeUIEditor | 에디터에서 페이드 애니메이션 테스트 |
| VIRDYVideoPlayerEditor | 비디오 클립 재생 테스트 |
| VIRDYLightTransitionEditor | 라이트 프리셋 전환 테스트 |

### 2.11 샘플 프리팹

| 프리팹 | 설명 |
|--------|------|
| VIRDYWorld.prefab | Descriptor 사전 설정된 템플릿 월드 |
| VIRDYMaterialController.prefab | 셰이더 제어 설정 예제 |
| VIRDYUwc.prefab | 윈도우 캡처 통합 예제 |
| uWC Window List Item.prefab | 윈도우 선택 UI |

### 2.12 조건부 컴파일 심볼

| 심볼 | 설명 |
|------|------|
| VIRDY_CORE | 프레임워크 빌드 (Context 접근 가능) |
| VIRDY_DOTWEEN | DOTween 애니메이션 활성화 |
| VIRDY_HORIZONBASEDAMBIENTOCCLUSION | HBAO 렌더러 |
| VIRDY_OCCASOFTWARE_ALTOS | Altos 렌더러 |
| VIRDY_VOLUMETRICLIGHTS | 볼류메트릭 라이트 |
| VIRDY_VOLUMETRICFOGANDMIST2 | 볼류메트릭 포그 |

### 2.13 월드 빌드 워크플로우

| 단계 | 동작 |
|------|------|
| 1 | Unity 씬 생성, VIRDYWorldDescriptor 추가 |
| 2 | 스폰 포인트, Directional Light, GlobalVolume 설정 |
| 3 | 인터랙티브 컴포넌트 추가 (VIRDYBehaviour/VIRDYNetworkBehaviour 상속) |
| 4 | 에디터에서 테스트 |
| 5 | VIRDYWorldDescriptorEditor의 "Build" 클릭 → AssetBundle 생성 |
| 6 | VIRDY 로비에서 AssetBundle 업로드 |

---

## 3. 설계 시 고려사항

### 3.1 SDK 외부 배포

- SDK는 외부 크리에이터에게 웹사이트/문서를 통해 배포 예정
- 월드 빌드 + 아바타 빌드(자체 확장자) 기능 포함
- 외부 배포 시 VIRDY_CORE 심볼 없이 사용 가능해야 함

### 3.2 네트워크 컴포넌트의 NetworkObject 요구

VIRDYNetworkBehaviour를 사용하는 모든 오브젝트는 NetworkObject 컴포넌트가 필수이다. 이를 누락하면 네트워크 동기화가 작동하지 않으므로, RequireComponent 어트리뷰트로 강제한다.

### 3.3 월드 내 충돌 방지

월드 AssetBundle에 포함된 EventSystem, Camera, AudioListener는 VIRDY 메인 시스템과 충돌하므로 자동 비활성화된다. SDK 사용자에게 이 제약을 명확히 안내해야 한다.

### 3.4 프레임워크 통합 포인트

SDK 컴포넌트는 VIRDY 프레임워크와 아래 지점에서 연결된다:

| 연결 | 설명 |
|------|------|
| 카메라 이벤트 | VIRDYWorldUI, VIRDYCinemachineTrack이 카메라 전환을 감지 |
| 생명주기 | VIRDYWorldDescriptor가 월드 로드/언로드 시 모든 컴포넌트 초기화/정리 |
| 네트워크 | VIRDYNetworkBehaviour가 Photon Fusion 세션에 자동 참여 |
| PostIt | VIRDYPostItController가 NetworkActor.WriteBuffer에서 틱 호출 |

---

## 4. 엣지 케이스 및 예외 처리

| 상황 | 대응 |
|------|------|
| VIRDYWorldDescriptor 누락 월드 | 기본값으로 동작 (스폰 포인트 = 원점) |
| NetworkObject 없이 VIRDYNetworkBehaviour 사용 | RequireComponent로 자동 추가 강제 |
| 월드에 EventSystem/Camera/AudioListener 포함 | 자동 비활성화 |
| SDK 버전과 클라이언트 버전 불일치 | VIRDYWorldDescriptor의 UnityVersion/URPVersion으로 감지 |
| DOTween 미설치 상태에서 FadeUI 사용 | VIRDY_DOTWEEN 심볼 미정의 시 DOTween 코드 비활성화 |
| 다수의 VIRDYWorldDescriptor 존재 | 싱글톤으로 하나만 유지 |
| OSC 포트 충돌 | 사용자에게 포트 변경 안내 |

---

## 5. 향후 확장 가능성

| 항목 | 설명 | 우선순위 |
|------|------|---------|
| **외부 SDK 배포** | 웹사이트/문서를 통한 외부 크리에이터 배포 | 높음 |
| **자체 아바타 확장자** | 애니메이션/스크립트 내장 아바타 빌드 기능 | 높음 |
| **SDK 문서화** | API 레퍼런스, 튜토리얼, 예제 프로젝트 | 높음 |
| **커스텀 컴포넌트 추가** | 투표, 리더보드, 미니게임 등 | 중간 |
| **비주얼 스크립팅** | 코드 없이 인터랙션 설정 | 장기 |
| **월드/아바타 마켓플레이스** | 커뮤니티 콘텐츠 공유/판매 | 장기 |

---

## 관련 문서

- [월드 시스템](./04_World_System.md)
- [네트워크 시스템](./05_Network_System.md)
- [아바타 시스템](./01_Avatar_System.md)
