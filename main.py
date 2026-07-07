# -*- coding: utf-8 -*-
import streamlit as st
import numpy as np
import pandas as pd
import time
import matplotlib.pyplot as plt
import math

# 1. 페이지 전체 기본 설정
st.set_page_config(page_title="반도체 이송 공정 통합 디지털 트윈 시스템", layout="wide")

st.title("🏭 반도체 이송공정 실증 및 물리 통합 디지털 트윈")
st.caption("물리학Ⅰ 물질의 자성 및 힘의 평형 단원 연계 탐구 - 산업공학적 경제성 대조 모델")
st.markdown("---")

# 2. 전역 시스템 제어 매개변수를 사이드바에 통합 배치
st.sidebar.header("🎛️ 공동 공장 매개변수 설정")
st.sidebar.markdown("두 라인의 베이스 환경 조건을 설정합니다.")

global_lanes = st.sidebar.slider("공통 레일 차선 수 (줄)", 1, 4, 1, 1, key="g_lanes")
global_clean = st.sidebar.slider("공통 클린룸 청정도 (단계)", 1, 10, 7, 1, key="g_clean")

if 'ani_frame' not in st.session_state:
    st.session_state.ani_frame = 0

if 'dust_base' not in st.session_state:
    # 최초 1회 파티클 기본 분포 생성
    num_dust_particles = 60
    map_width = 160.0
    x_step = map_width / num_dust_particles
    dust_data = []
    for i in range(num_dust_particles):
        x_pos = i * x_step
        if np.random.rand() < 0.9:
            y_pos = np.random.uniform(12, 25)
        else:
            y_pos = np.random.uniform(25, 85)
        dust_data.append({'id': i, 'base_x': x_pos, 'y': y_pos})
    st.session_state.dust_base = pd.DataFrame(dust_data)

# -----------------------------------------------------------------
# 상단 대시보드용 고정 물리 경제성 연산 함수
# -----------------------------------------------------------------
def run_normal_calc(speed, lanes, cleanliness):
    ITEM_VALUE = 200000             
    RAW_MATERIAL_COST = 50000       
    CAPACITY_PER_SPEED_LANE = 1000 
    total_produced = int(speed * lanes * CAPACITY_PER_SPEED_LANE)

    vibration = speed * 2.0 * math.sqrt(lanes)
    final_dust = max(0.1, (11 - cleanliness) * 4.0 + (speed * 1.2))
    damage_rate = min(100.0, (vibration * 0.1) + ((final_dust ** 1.8) * 0.12))
    
    damaged_count = int(total_produced * (damage_rate / 100.0))
    perfect_count = total_produced - damaged_count

    base_facility_cost = 500000
    cleanliness_cost_per_lane = (cleanliness ** 2.0) * 120000  
    total_management_cost = float((base_facility_cost + cleanliness_cost_per_lane) * lanes)

    total_revenue = perfect_count * ITEM_VALUE
    total_raw_cost = total_produced * RAW_MATERIAL_COST
    
    waste_penalty = damaged_count * 30000
    net_profit = float(total_revenue - total_raw_cost - total_management_cost - waste_penalty)
    
    return total_produced, perfect_count, damaged_count, vibration, final_dust, damage_rate, total_management_cost, net_profit

def run_ice_calc(speed, lanes, cleanliness):
    ITEM_VALUE = 200000             
    RAW_MATERIAL_COST = 50000       
    CAPACITY_PER_SPEED_LANE = 800  
    total_produced = int(speed * lanes * CAPACITY_PER_SPEED_LANE)

    vibration = (speed ** 1.1) * 0.005
    final_dust = max(0.05, float(11 - cleanliness) * 3.5)
    damage_rate = min(100.0, (vibration * 0.01) + ((final_dust ** 1.6) * 0.08))
    
    damaged_count = int(total_produced * (damage_rate / 100.0))
    perfect_count = total_produced - damaged_count

    base_cooling_cost = 1500000
    cleanliness_cost_per_lane = (cleanliness ** 3.2) * 45000  
    total_management_cost = float((base_cooling_cost + cleanliness_cost_per_lane) * lanes)

    total_revenue = perfect_count * ITEM_VALUE
    total_raw_cost = total_produced * RAW_MATERIAL_COST
    
    waste_penalty = damaged_count * 30000
    net_profit = float(total_revenue - total_raw_cost - total_management_cost - waste_penalty)
    
    return total_produced, perfect_count, damaged_count, vibration, final_dust, damage_rate, total_management_cost, net_profit


# 3. 레이아웃 분할: 상단 경제성 대시보드
st.markdown("### 📊 1. 공정 경제성 실증 대시보드")
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("⚙️ LINE A: 기계식 컨베이어")
    normal_dashboard_speed = st.slider("LINE A 가동 속도 설정 (m/s)", 0.5, 3.0, 1.5, 0.1, key="n_dash_speed")
    
    n_prod, n_perf, n_dam, n_vib, n_dust, n_rate, n_cost, n_profit = run_normal_calc(normal_dashboard_speed, global_lanes, global_clean)
    
    st.metric(label="LINE A 최종 순이익", value=f"{n_profit:,} 원")
    st.write(f"- 부품 파손 불량률: `{n_rate:.3f} %` | 최종 먼지량: `{n_dust:.1f} %`")
    st.write(f"- 합격품: `{n_perf:,} 장` / 불량품: `{n_dam:,} 장` | 총 관리비: `{n_cost:,} 원`")

with col_right:
    st.subheader("🧲 LINE B: 초전도 자기부상")
    ice_dashboard_speed = st.slider("LINE B 가동 속도 설정 (m/s)", 0.5, 8.0, 4.0, 0.1, key="i_dash_speed")
    
    i_prod, i_perf, i_dam, i_vib, i_dust, i_rate, i_cost, i_profit = run_ice_calc(ice_dashboard_speed, global_lanes, global_clean)
    
    profit_diff = i_profit - n_profit
    st.metric(label="LINE B 최종 순이익", value=f"{i_profit:,} 원", delta=f"LINE A 대비 {profit_diff:+,} 원")
    st.write(f"- 부품 파손 불량률: `{i_rate:.3f} %` | 최종 먼지량: `{i_dust:.1f} %`")
    st.write(f"- 합격품: `{i_perf:,} 장` / 불량품: `{i_dam:,} 장` | 총 관리비: `{i_cost:,} 원`")

st.markdown("---")

# 4. 하단 레이아웃: 독립적인 2D 파티클 거동 물리 시뮬레이터 구성
st.markdown("### 🎦 2. 디지털 트윈 물리 거동 시뮬레이션 (독립 제어)")
st.caption("※ 상단 대시보드와 무관하게 고속 주행 시 기계식의 마찰 붕괴(3~5 m/s)와 초전도 무마찰 안정성(최대 15 m/s)을 직접 조작하며 대조합니다.")

# 하단 전용 독립 슬라이더 배치
sim_control_col1, sim_control_col2 = st.columns(2)
with sim_control_col1:
    # 기계식 컨베이어는 딱 임계점 한계가 연출되는 5.0 m/s까지로 세팅
    sim_speed_a = st.slider("시뮬레이션 LINE A 컨베이어 속도 (m/s)", 0.5, 5.0, 2.0, 0.1, key="sim_speed_a")
with sim_control_col2:
    # 초전도 부상선은 시원하게 15.0 m/s 초고속 영역까지 관측
    sim_speed_b = st.slider("시뮬레이션 LINE B 초전도 부상 속도 (m/s)", 0.5, 15.0, 6.0, 0.5, key="sim_speed_b")

vis_col1, vis_col2 = st.columns(2)
plot_container_a = vis_col1.empty()
plot_container_b = vis_col2.empty()

map_width = 160.0
frame = st.session_state.ani_frame

# -----------------------------------------------------------------
# 5. 실시간 독립 속도 연동 애니메이션 루프
# -----------------------------------------------------------------
while True:
    # [LINE A 독립 애니메이션 연산]
    offset_a = (frame * sim_speed_a * 1.5) % map_width
    current_x_a, current_y_a, colors_a = [], [], []
    
    for _, row in st.session_state.dust_base.iterrows():
        cur_x = (row['base_x'] - offset_a) % map_width
        cur_y = row['y']
        if cur_x <= 100:
            if np.random.rand() > 0.4:
                # 일반 기계식은 속도가 올라갈수록 주변 먼지 요동 범위가 넓어짐
                cur_y = cur_y + (np.sin(frame + row['id']) * (sim_speed_a * 0.8))
            cur_y = max(11, min(95, cur_y))
            current_x_a.append(cur_x)
            current_y_a.append(cur_y)
            colors_a.append("#FF4B4B")

    fig_a, ax_a = plt.subplots(figsize=(6, 3))
    ax_a.set_xlim(0, 100)
    ax_a.set_ylim(0, 100)
    ax_a.axis('off')
    fig_a.patch.set_facecolor('#0E1117')
    ax_a.set_facecolor('#161A24')
    ax_a.axhline(y=10, color='#4A5568', linestyle='-', linewidth=6)

    wafer_y_a = 10
    wafer_color_a = '#63B3ED' 
    
    # ⭐ [고정 기계 한계 현실화]: 속도가 3.0 m/s 이상부터 덜덜 떨리기 시작하여 5.0으로 갈수록 진동이 극대화됨
    if sim_speed_a >= 3.0:
        # 3.0~5.0 사이의 과속 가중치에 따라 떨림(vibration_intensity)이 점진적으로 증가
        vibration_intensity = (sim_speed_a - 2.8) * 2.0
        wafer_y_a += np.random.uniform(-vibration_intensity, vibration_intensity)
        wafer_color_a = '#E53E3E' # 한계 위험 경고 (붉은색 변색)
        ax_a.text(50, 85, "⚠️ MECHANICAL FRICTION LIMIT", color='#E53E3E', weight='bold', ha='center', fontsize=9)

    rect_a = plt.Rectangle((42, wafer_y_a), 16, 12, color=wafer_color_a, zorder=5)
    ax_a.add_patch(rect_a)
    ax_a.text(50, wafer_y_a + 6, "WAFER A", color='black', weight='bold', ha='center', va='center', zorder=6)
    ax_a.scatter(current_x_a, current_y_a, color=colors_a, s=12, alpha=0.6, zorder=3)
    ax_a.set_title(f"LINE A 운송 시뮬레이션 (구동속도: {sim_speed_a:.1f} m/s)", color='white', fontsize=10)

    # [LINE B 독립 애니메이션 연산]
    offset_b = (frame * sim_speed_b * 1.5) % map_width
    current_x_b, current_y_b, colors_b = [], [], []
    
    for _, row in st.session_state.dust_base.iterrows():
        cur_x = (row['base_x'] - offset_b) % map_width
        cur_y = row['y']
        if cur_x <= 100:
            if 35 <= cur_x <= 65:
                # 초전도는 먼지들이 기류에 쓸려 나가는 현상 연출
                disturbance = np.sin(frame * 0.5 + row['id']) * (sim_speed_b * 0.4)
                cur_y = row['y'] + disturbance
            cur_y = max(11, min(95, cur_y))
            current_x_b.append(cur_x)
            current_y_b.append(cur_y)
            colors_b.append("#A0AEC0")

    fig_b, ax_b = plt.subplots(figsize=(6, 3))
    ax_b.set_xlim(0, 100)
    ax_b.set_ylim(0, 100)
    ax_b.axis('off')
    fig_b.patch.set_facecolor('#0E1117')
    ax_b.set_facecolor('#161A24')
    ax_b.axhline(y=10, color='#4A5568', linestyle='-', linewidth=6)

    # ⭐ 초전도 부상선은 속도를 최대 15.0 m/s까지 끝까지 올려도 어떠한 요동이나 미세 떨림도 없이 수평 유지!
    rect_b = plt.Rectangle((42, 43), 16, 12, color='#9AE6B4', zorder=5)
    ax_b.add_patch(rect_b)
    ax_b.text(50, 49, "WAFER B", color='black', weight='bold', ha='center', va='center', zorder=6)
    ax_b.text(50, 22, "Levitation Gap (Perfect Stable)", color='#9AE6B4', fontsize=8, ha='center')
    ax_b.scatter(current_x_b, current_y_b, color=colors_b, s=12, alpha=0.6, zorder=3)
    ax_b.set_title(f"LINE B 운송 시뮬레이션 (구동속도: {sim_speed_b:.1f} m/s)", color='white', fontsize=10)

    # 렌더링 화면 갱신
    plot_container_a.pyplot(fig_a)
    plot_container_b.pyplot(fig_b)
    plt.close(fig_a)
    plt.close(fig_b)

    time.sleep(0.03)
    frame += 1
    st.session_state.ani_frame = frame