# -*- coding: utf-8 -*-
import math

def calculate_ice_factory(speed, lanes, cleanliness):
    """
    초전도 자기부상(ICE) 컨베이어 공정의 물리 및 산업공학 지표를 동적으로 계산하는 함수
    """
    TOTAL_DELIVERY_DISTANCE = 4500  
    ITEM_VALUE = 200000             
    RAW_MATERIAL_COST = 50000       
    
    CAPACITY_PER_SPEED_LANE = 600 
    total_produced = int(speed * lanes * CAPACITY_PER_SPEED_LANE)

    # [물리학적 특성 반영]
    vibration = (speed ** 1.1) * 0.005
    
    # 초전도라도 청정도가 1~2단계 수준으로 나쁘면 외부 유입 먼지 때문에 오염 발생
    final_dust = max(0.05, float(11 - cleanliness) * 0.6)

    # [품질 지표 계산]
    damage_rate = min(100.0, (vibration * 0.01) + (final_dust * 0.015))
    
    damaged_count = int(total_produced * (damage_rate / 100.0))
    perfect_count = total_produced - damaged_count

    # [재무 비용 연산 변동] - 초전도 클린룸 고단계 청정 유지비를 매우 무겁게 적용
    # 최고 단계(10단계) 가동 시 냉각비와 공조비가 합쳐져 차선당 수백만 원이 들도록 현실화
    base_cooling_cost = 950000
    cleanliness_cost_per_lane = (cleanliness ** 1.8) * 80000  # 지수함수 형태로 청정도가 높을수록 비용 폭증
    total_management_cost = float((base_cooling_cost + cleanliness_cost_per_lane) * lanes)

    # 매출 및 순이익 계산
    total_revenue = perfect_count * ITEM_VALUE
    total_raw_cost = total_produced * RAW_MATERIAL_COST
    net_profit = float(total_revenue - total_raw_cost - total_management_cost)

    return {
        "factory_type": "초전도 자기부상 공정 (LINE B)",
        "speed": speed,
        "lanes": lanes,
        "cleanliness": cleanliness,
        "vibration": vibration,
        "final_dust": final_dust,
        "delivery_time": (TOTAL_DELIVERY_DISTANCE / (speed * 60.0)),
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