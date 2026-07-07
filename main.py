# -*- coding: utf-8 -*-
import streamlit as st
import numpy as np
import pandas as pd
import time
import matplotlib.pyplot as plt

# 외부 공장 연산 함수 임포트
from normal_factory import calculate_normal_factory
from ice_factory import calculate_ice_factory

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

if 'dust_base' not in st.session_state:
    # 최초 1회 파티클 기본 분포 생성 (90% 바닥 밀집, 10% 공중 부유)
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

# 3. 레이아웃 분할: 상단은 경제성 대시보드 정보 출력
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("⚙️ LINE A: 기계식 컨베이어")
    # 현실적인 기계식 물류 제한 속도 반영 (최대 3.0 m/s)
    normal_speed = st.slider("LINE A 이송 속도 (m/s)", 0.5, 3.0, 1.5, 0.1, key="n_speed", 
                             help="기계식은 레일 마찰과 관성 한계로 인해 최대 속도가 3.0 m/s로 제한됩니다.")
    normal_res = calculate_normal_factory(normal_speed, global_lanes, global_clean)
    
    st.metric(label="LINE A 최종 순이익", value=f"{normal_res['net_profit']:,} 원")
    st.markdown("**🔹 물리/품질 수치**")
    st.write(f"- 레일 마찰 진동수: `{normal_res['vibration']:.1f} Hz` | 최종 먼지량: `{normal_res['final_dust']:.1f} %`")
    st.write(f"- 부품 파손 불량률: `{normal_res['damage_rate']:.3f} %` (물리 진동 치명타)")
    st.markdown("**🔹 생산/재무 수치**")
    st.write(f"- 시간당 총 투입량: `{normal_res['total_produced']:,} 장` | 합격: `{normal_res['perfect_count']:,} 장` / 불량: `{normal_res['damaged_count']:,} 장`")

with col_right:
    st.subheader("🧲 LINE B: 초전도 자기부상")
    # 공기 저항(와류 현상)을 고려한 영리한 클린룸 상한 속도 반영 (최대 8.0 m/s)
    ice_speed = st.slider("LINE B 이송 속도 (m/s)", 0.5, 8.0, 4.0, 0.1, key="i_speed",
                           help="초전도 레일은 무마찰이나, 클린룸 내부 공기 교란(와류)을 억제하기 위해 공정 한계 속도를 8.0 m/s로 제어합니다.")
    ice_res = calculate_ice_factory(ice_speed, global_lanes, global_clean)
    
    profit_diff = ice_res['net_profit'] - normal_res['net_profit']
    st.metric(label="LINE B 최종 순이익", value=f"{ice_res['net_profit']:,} 원", delta=f"LINE A 대비 {profit_diff:+,} 원")
    st.markdown("**🔹 물리/품질 수치**")
    st.write(f"- 초전도 미세 진동수: `{ice_res['vibration']:.3f} Hz` | 최종 먼지량: `{ice_res['final_dust']:.1f} %`")
    st.write(f"- 부품 파손 불량률: `{ice_res['damage_rate']:.3f} %` (초정밀 수율 반영)")
    st.markdown("**🔹 생산/재무 수치**")
    st.write(f"- 시간당 총 투입량: `{ice_res['total_produced']:,} 장` | 합격: `{ice_res['perfect_count']:,} 장` / 불량: `{ice_res['damaged_count']:,} 장`")

st.markdown("---")
st.subheader("🎦 실시간 2D 디지털 트윈 시뮬레이션 (동시 비교)")
st.caption("※ 현실적 속도 상한선 내에서 기계식의 한계(진동 변색)와 초전도 방식의 무마찰 고속 안정성을 시각적 대조 환경으로 관측합니다.")

# 그래픽 배치를 위한 컬럼 분할
vis_col1, vis_col2 = st.columns(2)
plot_container_a = vis_col1.empty()
plot_container_b = vis_col2.empty()

frame = 0
map_width = 160.0

while True:
    # -----------------------------------------------------------------
    # 1. LINE A (기계식 컨베이어) 파티클 & 웨이퍼 물리 거동 연산
    # -----------------------------------------------------------------
    offset_a = (frame * normal_speed) % map_width
    current_x_a = []
    current_y_a = []
    colors_a = []
    
    for _, row in st.session_state.dust_base.iterrows():
        cur_x = (row['base_x'] - offset_a) % map_width
        cur_y = row['y']
        if cur_x <= 100:
            if np.random.rand() > 0.4:
                cur_y = cur_y + (np.sin(frame + row['id']) * (normal_speed * 0.6))
            cur_y = max(11, min(95, cur_y))
            current_x_a.append(cur_x)
            current_y_a.append(cur_y)
            colors_a.append("#FF4B4B") # 마찰 오염 빨간 먼지

    fig_a, ax_a = plt.subplots(figsize=(6, 3))
    ax_a.set_xlim(0, 100)
    ax_a.set_ylim(0, 100)
    ax_a.axis('off')
    fig_a.patch.set_facecolor('#0E1117')
    ax_a.set_facecolor('#161A24')
    ax_a.axhline(y=10, color='#4A5568', linestyle='-', linewidth=6)

    # 기계식 속도 제한에 가까워질 때 변색 및 진동 임계점 조정 (2.0 m/s 이상 시 페널티 연출)
    wafer_y_a = 10
    wafer_color_a = '#63B3ED' 
    
    if normal_speed >= 2.0:
        vibration_intensity = (normal_speed - 1.5) * 1.2
        wafer_y_a += np.random.uniform(-vibration_intensity, vibration_intensity)
        wafer_color_a = '#E53E3E' # 파손 위험 알림 경고색
        ax_a.text(50, 85, "⚠️ MECHANICAL FRICTION LIMIT", color='#E53E3E', weight='bold', ha='center', fontsize=9)

    rect_a = plt.Rectangle((42, wafer_y_a), 16, 12, color=wafer_color_a, zorder=5)
    ax_a.add_patch(rect_a)
    ax_a.text(50, wafer_y_a + 6, "WAFER A", color='black', weight='bold', ha='center', va='center', zorder=6)
    ax_a.scatter(current_x_a, current_y_a, color=colors_a, s=12, alpha=0.6, zorder=3)
    ax_a.set_title("LINE A 물리 거동 (Max 3.0m/s)", color='white', fontsize=10)

    # -----------------------------------------------------------------
    # 2. LINE B (초전도 자기부상) 파티클 & 웨이퍼 물리 거동 연산
    # -----------------------------------------------------------------
    offset_b = (frame * ice_speed) % map_width
    current_x_b = []
    current_y_b = []
    colors_b = []

    for _, row in st.session_state.dust_base.iterrows():
        cur_x = (row['base_x'] - offset_b) % map_width
        cur_y = row['y']
        if cur_x <= 100:
            if 35 <= cur_x <= 65:
                disturbance = np.sin(frame * 0.5 + row['id']) * (ice_speed * 1.5)
                cur_y = row['y'] + disturbance
            cur_y = max(11, min(95, cur_y))
            current_x_b.append(cur_x)
            current_y_b.append(cur_y)
            colors_b.append("#A0AEC0") # 기류 추종 회색 먼지

    fig_b, ax_b = plt.subplots(figsize=(6, 3))
    ax_b.set_xlim(0, 100)
    ax_b.set_ylim(0, 100)
    ax_b.axis('off')
    fig_b.patch.set_facecolor('#0E1117')
    ax_b.set_facecolor('#161A24')
    ax_b.axhline(y=10, color='#4A5568', linestyle='-', linewidth=6)

    # 초전도 부상 웨이퍼는 지정 범위(최대 8.0 m/s) 내에서 완벽한 수평 유지
    rect_b = plt.Rectangle((42, 43), 16, 12, color='#9AE6B4', zorder=5)
    ax_b.add_patch(rect_b)
    ax_b.text(50, 49, "WAFER B", color='black', weight='bold', ha='center', va='center', zorder=6)
    ax_b.text(50, 22, "Levitation Gap (Stable)", color='#A0AEC0', fontsize=8, ha='center')
    ax_b.scatter(current_x_b, current_y_b, color=colors_b, s=12, alpha=0.6, zorder=3)
    ax_b.set_title("LINE B 물리 거동 (Max 8.0m/s)", color='white', fontsize=10)

    # -----------------------------------------------------------------
    # 3. 실시간 화면 전송 및 메모리 리셋
    # -----------------------------------------------------------------
    plot_container_a.pyplot(fig_a)
    plot_container_b.pyplot(fig_b)
    plt.close(fig_a)
    plt.close(fig_b)

    time.sleep(0.02)
    frame += 1