# -*- coding: utf-8 -*-
import streamlit as st
import numpy as np
import pandas as pd
import time
import matplotlib.pyplot as plt

# 외부 공장 연산 함수 임포트 (기존 기능 보존)
from normal_factory import calculate_normal_factory
from ice_factory import calculate_ice_factory

# 1. 페이지 전체 기본 설정 (통합 구조에 맞춰 기본 와이드 설정)
st.set_page_config(page_title="반도체 이송 공정 통합 디지털 트윈 시스템", layout="wide")

# 2. 사이드바 최상단에 [시뮬레이션 모드 전환 메인 메뉴] 배치
st.sidebar.markdown("# 🧭 메인 내비게이션")
app_mode = st.sidebar.radio(
    "실행할 시뮬레이터를 선택하세요:",
    ["📊 팩토리 경제성 대조 시뮬레이터", "🎦 2D 파티클 거동 물리 시뮬레이터"]
)
st.sidebar.markdown("---")


# =========================================================================
# [모드 1] 📊 팩토리 경제성 대조 시뮬레이터 (기존 main.py 기능 100% 보존)
# =========================================================================
if app_mode == "📊 팩토리 경제성 대조 시뮬레이터":
    st.title("📊 반도체 이송공정 실증 시뮬레이터")
    st.markdown("### 각각의 공장 제어 매개변수를 조절하여 효율성을 대조하세요.")
    st.markdown("---")

    # 2단 컬럼으로 나누어 왼쪽/오른쪽에 각각 독립된 게이지 바와 결과 배치
    col_left, col_right = st.columns(2)

    # --- [좌측: 기계식 컨베이어 공정 제어 및 결과] ---
    with col_left:
        st.subheader("⚙️ LINE A: 기계식 컨베이어")
        
        # 기계식 전용 게이지 바 (볼륨 조절 바)
        normal_speed = st.slider("LINE A 이송 속도 (m/s)", 0.5, 5.0, 2.5, 0.1, key="n_speed")
        normal_lanes = st.slider("LINE A 레일 차선 수 (줄)", 1, 4, 1, 1, key="n_lanes")
        normal_clean = st.slider("LINE A 클린룸 청정도 (단계)", 1, 10, 7, 1, key="n_clean")
        
        # 계산 실행
        normal_res = calculate_normal_factory(normal_speed, normal_lanes, normal_clean)
        
        st.markdown("---")
        st.metric(label="LINE A 최종 순이익", value=f"{normal_res['net_profit']:,} 원")
        
        st.markdown("**🔹 물리 및 품질 수치**")
        st.write(f"- レ일 마찰 진동수: `{normal_res['vibration']:.1f} Hz`")
        st.write(f"- 공정 내 최종 먼지량: `{normal_res['final_dust']:.1f} %`")
        st.write(f"- 부품 파손 불량률: `{normal_res['damage_rate']:.3f} %` (물리 진동 치명타)")
        
        st.markdown("**🔹 생산 및 재무 수치**")
        st.write(f"- 시간당 총 투입량: `{normal_res['total_produced']:,} 장`")
        st.write(f"- 최종 합격품: `{normal_res['perfect_count']:,} 장` / 불량품: `{normal_res['damaged_count']:,} 장`")
        st.write(f"- 시스템 총 관리비: `{normal_res['management_cost']:,} 원`")


    # --- [우측: 초전도 자기부상 공정 제어 및 결과] ---
    with col_right:
        st.subheader("🧲 LINE B: 초전도 자기부상")
        
        # 초전도체 전용 게이지 바 (속도 범위를 15.0 m/s까지 대폭 확장)
        ice_speed = st.slider("LINE B 이송 속도 (m/s)", 0.5, 15.0, 7.0, 0.1, key="i_speed")
        ice_lanes = st.slider("LINE B 레일 차선 수 (줄)", 1, 4, 1, 1, key="i_lanes")
        ice_clean = st.slider("LINE B 클린룸 청정도 (단계)", 1, 10, 7, 1, key="i_clean")
        
        # 계산 실행
        ice_res = calculate_ice_factory(ice_speed, ice_lanes, ice_clean)
        
        st.markdown("---")
        profit_diff = ice_res['net_profit'] - normal_res['net_profit']
        st.metric(
            label="LINE B 최종 순이익", 
            value=f"{ice_res['net_profit']:,} 원", 
            delta=f"기존 대비 {profit_diff:+,} 원"
        )
        
        st.markdown("**🔹 물리 및 품질 수치**")
        st.write(f"- 초전도 미세 진동수: `{ice_res['vibration']:.3f} Hz` (고속 주행 시 미세 진동)")
        st.write(f"- 공정 내 최종 먼지량: `{ice_res['final_dust']:.1f} %` (외부 유입 먼지)")
        st.write(f"- 부품 파손 불량률: `{ice_res['damage_rate']:.3f} %` (초정밀 물리 공식 반영)")
        
        st.markdown("**🔹 생산 및 재무 수치**")
        st.write(f"- 시간당 총 투입량: `{ice_res['total_produced']:,} 장` (고속 수송 극대화)")
        st.write(f"- 최종 합격품: `{ice_res['perfect_count']:,} 장` / 불량품: `{ice_res['damaged_count']:,} 장`")
        st.write(f"- 냉각 및 면적 관리비: `{ice_res['management_cost']:,} 원`")

    st.markdown("---")
    st.caption("본 시뮬레이터는 독립된 제어 변수를 바탕으로 구동되며, 초전도체의 초고속 영역에서의 미세 불량률까지 정밀 연산합니다.")


# =========================================================================
# [모드 2] 🎦 2D 파티클 거동 물리 시뮬레이터 (기존 particle_simulation.py 기능 통합)
# =========================================================================
elif app_mode == "🎦 2D 파티클 거동 물리 시뮬레이터":
    st.title("🏭 반자성 부상 기반 파티클 프리(Particle-free) 이송 시스템 물리 시뮬레이터")
    st.caption("물리학Ⅰ 물질의 자성 및 힘의 평형 단원 연계 탐구 - 산업공학적 디지털 트윈 모델")

    # 2. 사이드바 제어 매개변수 노출
    st.sidebar.header("🎛️ 파티클 시스템 제어")

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
    st.caption("설정하신 속도($v$)에 비례하여 하단 레일이 흐며, 물체 주변을 지나가는 파티클들의 유체 밀림 현상이 실시간으로 시각화됩니다.")
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
                y_pos = np.random.uniform(12, 25)
            else:
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
                    if np.random.rand() > 0.4:
                        cur_y = cur_y + (np.sin(frame + row['id']) * (move_speed * 0.6))
                    color_list.append("#FF4B4B")
                else:
                    if laminar_flow:
                        cur_y = np.random.uniform(10, 20)
                        color_list.append("#00F0FF")
                    else:
                        if 35 <= cur_x <= 65:
                            disturbance = np.sin(frame * 0.5 + row['id']) * (move_speed * 2.2)
                            cur_y = row['y'] + disturbance
                            color_list.append("#A0AEC0") # 이전 요청대로 노란색 대신 회색 처리
                        else:
                            color_list.append("#A0AEC0")
                        
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

        ax.axhline(y=10, color='#4A5568', linestyle='-', linewidth=6)

        if mode == "일반 마찰식 컨베이어 벨트":
            rect = plt.Rectangle((42, 10), 16, 12, color='#63B3ED', zorder=5)
            ax.text(50, 16, "WAFER", color='black', weight='bold', ha='center', va='center', zorder=6)
        else:
            # 이전 질문에서 요청하신 1.5배 높아진 부상 높이(43) 그대로 세팅 완료
            rect = plt.Rectangle((42, 43), 16, 12, color='#9AE6B4', zorder=5)
            ax.text(50, 49, "WAFER", color='black', weight='bold', ha='center', va='center', zorder=6)
            ax.text(50, 22, f"Levitation Gap (v={move_speed})", color='#A0AEC0', fontsize=8, ha='center')

        ax.add_patch(rect)
        ax.scatter(current_x_list, current_y_list, color=color_list, s=15, alpha=0.7, zorder=3)

        plot_container.pyplot(fig)
        plt.close(fig)

        time.sleep(0.01)
        frame += 1