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

# 애니메이션용 누적 프레임 세션 상태 관리 (뚝뚝 끊김 방지)
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
# 내부 실시간 연산 함수 정의 (경제성 & 페널티 황금 밸런스 셋)
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


# 3. 레이아웃 분할: 상단은 경제성 대시보드 정보 출력
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("⚙️ LINE A: 기계식 컨베이어")
    normal_speed = st.slider("LINE A 이송 속도 (m/s)", 0.5, 3.0, 1.5, 0.1, key="n_speed")
    
    n_prod, n_perf, n_dam, n_vib, n_dust, n_rate, n_cost, n_profit = run_normal_calc(normal_speed, global_lanes, global_clean)
    
    st.metric(label="LINE A 최종 순이익", value=f"{n_profit:,} 원")
    st.markdown("**🔹 물리/품질 수치**")
    st.write(f"- 레일 마찰 진동수: `{n_vib:.1f} Hz` | 최종 먼지량: `{n_dust:.1f} %`")
    st.write(f"- 부품 파손 불량률: `{n_rate:.3f} %` (물리 진동 치명타)")
    st.markdown("**🔹 생산/재무 수치**")
    st.write(f"- 시간당 총 투입량: `{n_prod:,} 장` | 합격: `{n_perf:,} 장` / 불량: `{n_dam:,} 장`")
    st.write(f"- 시스템 총 관리비: `{n_cost:,} 원` (청정도 반영)")

with col_right:
    st.subheader("🧲 LINE B: 초전도 자기부상")
    ice_speed = st.slider("LINE B 이송 속도 (m/s)", 0.5, 8.0, 4.0, 0.1, key="i_speed")
    
    i_prod, i_perf, i_dam, i_vib, i_dust, i_rate, i_cost, i_profit = run_ice_calc(ice_speed, global_lanes, global_clean)
    
    profit_diff = i_profit - n_profit
    st.metric(label="LINE B 최종 순이익", value=f"{i_profit:,} 원", delta=f"LINE A 대비 {profit_diff:+,} 원")
    st.markdown("**🔹 물리/품질 수치**")
    st.write(f"- 초전도 미세 진동수: `{i_vib:.3f} Hz` | 최종 먼지량: `{i_dust:.1f} %`")
    st.write(f"- 부품 파손 불량률: `{i_rate:.3f} %` (초정밀 수율 반영)")
    st.markdown("**🔹 생산/재무 수치**")
    st.write(f"- 시간당 총 투입량: `{i_prod:,} 장` | 합격: `{i_perf:,} 장` / 불량: `{i_dam:,} 장`")
    st.write(f"- 시스템 총 관리비: `{i_cost:,} 원` (초고성능 공조 반영)")

st.markdown("---")
st.subheader("🎦 실시간 2D 디지털 트윈 시뮬레이션 (동시 비교)")
st.caption("※ 상단 슬라이더에서 조절한 각 라인의 속도(m/s)와 먼지 환경이 실시간 흐름 레이트에 완벽하게 연동됩니다.")

vis_col1, vis_col2 = st.columns(2)
plot_container_a = vis_col1.empty()
plot_container_b = vis_col2.empty()

map_width = 160.0
frame = st.session_state.ani_frame

# -----------------------------------------------------------------
# 4. 실시간 먼지 이동 속도 제어 루프
# -----------------------------------------------------------------
while True:
    # 각 슬라이더의 물리적 '속도'에 비례하여 프레임당 이격 거리(offset)를 다르게 연산
    offset_a = (frame * normal_speed * 1.5) % map_width
    current_x_a, current_y_a, colors_a = [], [], []
    
    for _, row in st.session_state.dust_base.iterrows():
        cur_x = (row['base_x'] - offset_a) % map_width
        cur_y = row['y']
        if cur_x <= 100:
            if np.random.rand() > 0.4:
                # 일반 기계식은 속도가 빠를수록 주변 먼지 입자가 심하게 요동침
                cur_y = cur_y + (np.sin(frame + row['id']) * (normal_speed * 0.8))
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
    if normal_speed >= 2.0:
        vibration_intensity = (normal_speed - 1.5) * 1.5
        wafer_y_a += np.random.uniform(-vibration_intensity, vibration_intensity)
        wafer_color_a = '#E53E3E' 
        ax_a.text(50, 85, "⚠️ MECHANICAL FRICTION LIMIT", color='#E53E3E', weight='bold', ha='center', fontsize=9)

    rect_a = plt.Rectangle((42, wafer_y_a), 16, 12, color=wafer_color_a, zorder=5)
    ax_a.add_patch(rect_a)
    ax_a.text(50, wafer_y_a + 6, "WAFER A", color='black', weight='bold', ha='center', va='center', zorder=6)
    ax_a.scatter(current_x_a, current_y_a, color=colors_a, s=12, alpha=0.6, zorder=3)
    ax_a.set_title(f"LINE A 실시간 거동 (유속 연동: {normal_speed:.1f} m/s)", color='white', fontsize=10)

    # -----------------------------------------------------------------
    # LINE B (초전도) 속도 연동 애니메이션
    # -----------------------------------------------------------------
    offset_b = (frame * ice_speed * 1.5) % map_width
    current_x_b, current_y_b, colors_b = [], [], []
    
    for _, row in st.session_state.dust_base.iterrows():
        cur_x = (row['base_x'] - offset_b) % map_width
        cur_y = row['y']
        if cur_x <= 100:
            if 35 <= cur_x <= 65:
                # 초전도는 웨이퍼를 통과할 때만 속도에 비례한 유체(공기) 밀림 현상 구현
                disturbance = np.sin(frame * 0.5 + row['id']) * (ice_speed * 1.2)
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

    rect_b = plt.Rectangle((42, 43), 16, 12, color='#9AE6B4', zorder=5)
    ax_b.add_patch(rect_b)
    ax_b.text(50, 49, "WAFER B", color='black', weight='bold', ha='center', va='center', zorder=6)
    ax_b.text(50, 22, "Levitation Gap (Stable)", color='#A0AEC0', fontsize=8, ha='center')
    ax_b.scatter(current_x_b, current_y_b, color=colors_b, s=12, alpha=0.6, zorder=3)
    ax_b.set_title(f"LINE B 실시간 거동 (유속 연동: {ice_speed:.1f} m/s)", color='white', fontsize=10)

    # 화면에 렌더링 후 메모리 누수 방지 리셋
    plot_container_a.pyplot(fig_a)
    plot_container_b.pyplot(fig_b)
    plt.close(fig_a)
    plt.close(fig_b)

    # 세션 상태 프레임 기록 및 제어
    time.sleep(0.03)
    frame += 1
    st.session_state.ani_frame = frame