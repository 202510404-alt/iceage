import streamlit as st
import numpy as np
import pandas as pd
import time
import matplotlib.pyplot as plt

# 1. 페이지 기본 설정 (최초 1회만 렌더링)
st.set_page_config(page_title="반자성 부상 이송 시스템 시뮬레이터", layout="wide")
st.title("🏭 반자성 부상 기반 파티클 프리(Particle-free) 이송 시스템 물리 시뮬레이터")
st.caption("물리학Ⅰ 물질의 자성 및 힘의 평형 단원 연계 탐구 - 산업공학적 디지털 트윈 모델")

# 2. 사이드바 입력 변수 제어
st.sidebar.header("🎛️ 시스템 제어 매개변수")

mode = st.sidebar.radio(
    "1. 이송 시스템 모드 선택",
    ["일반 마찰식 컨베이어 벨트", "반자성 자기부상 레일"]
)

bg_dust_density = st.sidebar.slider(
    "2. 공장 환경 청결도 (배경 파티클 밀도)",
    min_value=10, max_value=100, value=50, step=10,
    help="기본 공기 중에 존재하는 상시 파티클의 양을 조절합니다."
)

object_mass = st.sidebar.slider(
    "3. 이송 물체(반도체 자재) 질량 (g)",
    min_value=100, max_value=1000, value=500, step=50
)

move_speed = st.sidebar.slider(
    "4. 물체 이송 속도 (v)",
    min_value=1, max_value=10, value=4, step=1,
    help="물체가 이동하는 속도입니다. 속도가 빠를수록 주변 공기를 밀어내는 유체 저항이 강해집니다."
)

if mode == "반자성 자기부상 레일":
    laminar_flow = st.sidebar.checkbox("층류(Laminar Flow) 공조 시스템 가동", value=False)
else:
    laminar_flow = False

# 3. 2D 물리 시뮬레이션 전용 화면 배치
st.header("🎦 2D 물리 기반 이송 공정 시뮬레이션")
st.caption("설정하신 속도($v$)에 비례하여 하단 레일이 흐르며, 물체 주변을 지나가는 파티클들의 유체 밀림 현상이 실시간으로 시각화됩니다.")
plot_container = st.empty()

# 4. 현실적인 파티클 초기 분포 데이터 생성 (90% 바닥 밀집, 10% 공중 부유)
num_dust_particles = int(bg_dust_density)
map_width = 160.0
x_step = map_width / num_dust_particles

if 'dust_base' not in st.session_state or len(st.session_state.dust_base) != num_dust_particles:
    dust_data = []
    for i in range(num_dust_particles):
        x_pos = i * x_step
        
        # 현실적인 90% vs 10% 파티클 분포 로직
        if np.random.rand() < 0.9:
            # 90%는 바닥 및 레일 근처(y축 12~25 사이)에 낮게 깔림
            y_pos = np.random.uniform(12, 25)
        else:
            # 10%는 공장 공기 중 공중 부유(y축 25~85 사이)에 랜덤 배치
            y_pos = np.random.uniform(25, 85)
            
        dust_data.append({'id': i, 'base_x': x_pos, 'y': y_pos})
    st.session_state.dust_base = pd.DataFrame(dust_data)

# 5. 실시간 그래픽 업데이트 무한 루프
frame = 0

while True:
    # --- 유체역학 파티클 거동 계산 ---
    offset = (frame * move_speed) % map_width
    current_x_list = []
    current_y_list = []
    color_list = []

    for _, row in st.session_state.dust_base.iterrows():
        cur_x = (row['base_x'] - offset) % map_width
        cur_y = row['y']
        
        if cur_x <= 100:
            if mode == "일반 마찰식 컨베이어 벨트":
                # 마찰식: 마찰에 의해 기존 입자들이 불규칙하게 튀어오르는 무작위 거동 가속
                if np.random.rand() > 0.4:
                    cur_y = cur_y + (np.sin(frame + row['id']) * (move_speed * 0.6))
                color_list.append("#FF4B4B") # 마찰식 오염 파티클 (빨간색)
            else:
                # 자기부상 모드
                if laminar_flow:
                    # 공조 가동: 공중 부유 중이던 10%를 포함하여 기류가 하방 압착
                    cur_y = np.random.uniform(10, 20)
                    color_list.append("#00F0FF") # 공조 억제 파티클 (하늘색)
                else:
                    # 유체역학 공기 밀림 현상 (물체 부근 통과 시 속도 비례 진동)
                    if 35 <= cur_x <= 65:
                        disturbance = np.sin(frame * 0.5 + row['id']) * (move_speed * 2.2)
                        cur_y = row['y'] + disturbance
                        color_list.append("#A0AEC0") # 기류 교란 반응 파티클 (노란색)
                    else:
                        color_list.append("#A0AEC0") # 상시 대기 파티클 (회색)
                    
            # 화면 경계 이탈 제한
            cur_y = max(11, min(95, cur_y))
            current_x_list.append(cur_x)
            current_y_list.append(cur_y)

    # --- Matplotlib 그래프 드로잉 ---
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')
    fig.patch.set_facecolor('#0E1117')
    ax.set_facecolor('#161A24')

    # 하단 레일 라인 그리기
    ax.axhline(y=10, color='#4A5568', linestyle='-', linewidth=6)

    # 중앙 고정 물체 배치 (모드별 부상 높이 시각화 대조)
    if mode == "일반 마찰식 컨베이어 벨트":
        rect = plt.Rectangle((42, 10), 16, 12, color='#63B3ED', zorder=5)
        ax.text(50, 16, "WAFER", color='black', weight='bold', ha='center', va='center', zorder=6)
    else:
        rect = plt.Rectangle((42, 44), 16, 12, color='#9AE6B4', zorder=5)
        ax.text(50, 38, "WAFER", color='black', weight='bold', ha='center', va='center', zorder=6)
        ax.text(50, 18, f"Levitation Gap (v={move_speed})", color='#A0AEC0', fontsize=8, ha='center')

    ax.add_patch(rect)
    ax.scatter(current_x_list, current_y_list, color=color_list, s=15, alpha=0.7, zorder=3)

    # --- 화면 스왑 교체 ---
    plot_container.pyplot(fig)
    plt.close(fig)

    # 프레임 전환 딜레이 및 카운트
    time.sleep(0.01)
    frame += 1