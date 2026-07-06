# -*- coding: utf-8 -*-
import math

def calculate_ice_factory(speed, lanes, cleanliness):
    """
    초전도 자기부상(ICE) 컨베이어 공정의 물리 및 산업공학 지표를 동적으로 계산하는 함수
    (안전 방재 시스템 비용 및 초고속 미세 불량률 현실화 버전)
    """
    # [통제 변수: 일반 공장과 완전히 동일한 기본 상수 설정]
    TOTAL_DELIVERY_DISTANCE = 4500  # 공장 내 격자 레일 총연장 길이 (4.5km)
    ITEM_VALUE = 200000             # 웨이퍼 1장당 가치 (20만 원)
    RAW_MATERIAL_COST = 50000       # 1장당 순수 원자재 원가 (5만 원)
    
    # [동적 생산량 계산]
    CAPACITY_PER_SPEED_LANE = 600 
    total_produced = int(speed * lanes * CAPACITY_PER_SPEED_LANE)

    # [물리학적 특성 반영]
    # 아무리 초전도 부상이라도 속도가 극단적으로 빠르면 공기 저항 및 자기장 복원력 때문에 미세 진동 발생
    vibration = (speed ** 1.5) * 0.02
    
    # 기계 마찰 분진은 없지만, 외부 유입 미세 먼지는 청정도에 반비례함
    final_dust = max(0.1, float(10 - cleanliness))

    # [품질 지표 계산 - 0.001% 단위 미세 불량률 반영]
    dust_penalty = final_dust * 0.04
    vibration_penalty = vibration * 0.05
    damage_rate = min(100.0, dust_penalty + vibration_penalty)

    # [산업공학적 비용 및 제약 조건 계산]
    # 1. 청정실 기본 유지비 (일반 공장과 동일하게 제곱 비선형 적용)
    clean_cost = (cleanliness ** 2) * 15000  
    wear_cost = 0 

    # 2. 현실 반영 제약: 초기 투자비(CapEx) 감가상각 및 필수 부속 안전 설비 비용
    # (초전도 냉동기 투자비 및 냉매 누출 방지, 센서, 강제 배기 등 방재 시스템 운영비 포함)
    capex_depreciation_per_lane = 600000  
    base_cooling_per_lane = 250000        
    space_cost_per_lane = 150000          
    
    # 차선 효율 보너스
    lane_efficiency_bonus = max(0.8, 1.0 - (lanes - 1) * 0.05) 
    
    # 최종 초전도 관련 고정/운영 비용 계산 (설비투자비/방재비 합산)
    total_ice_system_cost = (capex_depreciation_per_lane + base_cooling_per_lane + space_cost_per_lane) * lanes * lane_efficiency_bonus
    
    # 전체 관리 비용 합산
    total_management_cost = clean_cost + wear_cost + total_ice_system_cost
    
    # 4.5km 주행 이동 시간 계산
    delivery_time_minutes = (TOTAL_DELIVERY_DISTANCE / speed) / 60

    # [최종 수율 및 재무적 순이익 계산]
    damaged_count = int(total_produced * (damage_rate / 100.0))
    perfect_count = total_produced - damaged_count

    gross_revenue = perfect_count * ITEM_VALUE
    loss_by_damage = damaged_count * RAW_MATERIAL_COST
    total_raw_material_cost = total_produced * RAW_MATERIAL_COST
    
    net_profit = gross_revenue - total_raw_material_cost - loss_by_damage - total_management_cost

    return {
        "factory_type": "초전도 자기부상 공정 (LINE B)",
        "speed": speed,
        "lanes": lanes,
        "cleanliness": cleanliness,
        "vibration": vibration,
        "final_dust": final_dust,
        "delivery_time": delivery_time_minutes,
        "damage_rate": damage_rate,
        "total_produced": total_produced,
        "perfect_count": perfect_count,
        "damaged_count": damaged_count,
        "management_cost": total_management_cost,
        "net_profit": net_profit
    }

def print_ice_dashboard(res):
    """
    결과 시각화를 위한 출력 함수 (터미널 테스트용 유지)
    """
    print("\n" + "=" * 60)
    print(f" [{res['factory_type']} 결과 대시보드] ")
    print("=" * 60)
    print(f"■ 공장 운영 설정: 이송속도 {res['speed']}m/s | 레일 {res['lanes']}줄 | 청정설정 {res['cleanliness']}단계")
    print(f"■ 물리 환경 지표: 레일 미세진동 {res['vibration']:.3f} Hz | 최종 먼지량 {res['final_dust']:.1f} %")
    print(f"■ 물류 배달 시간: 4.5km 구간 이동 시 평균 {res['delivery_time']:.1f}분 소요")
    print("-" * 60)
    print(f"■ [품질] 반도체 부품 불량률 : {res['damage_rate']:.3f} % (초정밀 물리 공식 반영)")
    print(f"■ [생산] 시간당 총 투입량   : {res['total_produced']} 장")
    print(f"■ [결과] 최종 합격품 수량   : {res['perfect_count']} 장 / 불량품: {res['damaged_count']} 장")
    print("-" * 60)
    print(f"▶ 시스템 총 유지 관리비    : {res['management_cost']:,.0f} 원 (초기설비/방재/냉각 반영)")
    print(f"▶ 공장 최종 재무적 순이익 : {res['net_profit']:,.0f} 원")
    print("=" * 60)

if __name__ == '__main__':
    result = calculate_ice_factory(speed=4.5, lanes=1, cleanliness=7)
    print_ice_dashboard(result)