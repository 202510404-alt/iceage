# -*- coding: utf-8 -*-
import streamlit as st
from normal_factory import calculate_normal_factory
from ice_factory import calculate_ice_factory

st.set_page_config(page_title="반도체 이송공정 시뮬레이터", layout="wide")

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
    st.write(f"- 레일 마찰 진동수: `{normal_res['vibration']:.1f} Hz`")
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