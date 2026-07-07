# -*- coding: utf-8 -*-
import math

def calculate_normal_factory(speed, lanes, cleanliness):
    """
    기존 기계식 컨베이어 공정의 물리 및 산업공학 지표를 동적으로 계산하는 함수
    """
    TOTAL_DELIVERY_DISTANCE = 4500  
    ITEM_VALUE = 200000             
    RAW_MATERIAL_COST = 50000       
    
    CAPACITY_PER_SPEED_LANE = 500 
    total_produced = int(speed * lanes * CAPACITY_PER_SPEED_LANE)

    # [내부 물리 및 환경 지표 계산]
    vibration = speed * 2.0 * math.sqrt(lanes)
    
    # 청정도가 낮을수록 먼지가 훨씬 더 심하게 발생하도록 수식 강화 (최대 10단계)
    # 청정도가 1단계이면 (11-1)*1.5 = 15% 베이스에 마찰 분진 추가
    final_dust = max(0.1, (11 - cleanliness) * 1.5 + (speed * 0.8))

    # [품질 및 불량률 계산] - 먼지가 많을수록 불량률이 더 민감하게 오르도록 수정
    damage_rate = min(100.0, (vibration * 0.03) + (final_dust * 0.05))
    
    damaged_count = int(total_produced * (damage_rate / 100.0))
    perfect_count = total_produced - damaged_count

    # [재무 비용 연산 변동] - 청정단계별 유지비를 현실적으로 대폭 상향
    # 단계당 50,000원 -> 단계당 300,000원으로 조정 (최고 청정 시 전기세 및 필터비 급증)
    base_facility_cost = 450000
    cleanliness_cost_per_lane = cleanliness * 300000 
    total_management_cost = float((base_facility_cost + cleanliness_cost_per_lane) * lanes)

    # 매출 및 순이익 계산
    total_revenue = perfect_count * ITEM_VALUE
    total_raw_cost = total_produced * RAW_MATERIAL_COST
    net_profit = float(total_revenue - total_raw_cost - total_management_cost)

    return {
        "factory_type": "기계식 컨베이어 공정 (LINE A)",
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

def print_normal_dashboard(res):
    """
    결과 시각화를 위한 출력 함수
    """
    print("\n" + "=" * 60)
    print(f" [{res['factory_type']} 결과 대시보드] ")
    print("=" * 60)
    print(f"■ 공장 운영 설정: 이송속도 {res['speed']}m/s | 레일 {res['lanes']}줄 | 청정설정 {res['cleanliness']}단계")
    print(f"■ 물리 환경 지표: 레일 진동수 {res['vibration']:.1f} Hz | 최종 미세먼지량 {res['final_dust']:.1f} %")
    print(f"■ 물류 배달 시간: 4.5km 구간 이동 시 평균 {res['delivery_time']:.1f}분 소요")
    print("-" * 60)
    print(f"■ [품질] 반도체 부품 파손율 : {res['damage_rate']:.2f} %")
    print(f"■ [생산] 시간당 총 투입량   : {res['total_produced']} 장 (속도/차선 동적 반영)")
    print(f"■ [결과] 최종 합격품 수량   : {res['perfect_count']} 장 / 불량품: {res['damaged_count']} 장")
    print("-" * 60)
    print(f"▶ 청정실 및 유지 관리 비용 : {res['management_cost']:,.0f} 원")
    print(f"▶ 공장 최종 재무적 순이익 : {res['net_profit']:,.0f} 원")
    print("=" * 60)
    
    print(" [산업공학적 의사결정 인사이트] ")
    if res['net_profit'] < 0:
        print("결과 분석: [적자] 속도가 빨라 물량은 많이 밀어넣었으나 파손율이 감당 안 되거나 관리비가 너무 큽니다.")
    elif res['damage_rate'] > 10.0:
        print("결과 분석: [품질 위기] 순이익은 남았으나 파손율이 10%를 초과하여 실제 운영은 불가능합니다.")
    else:
        print("결과 분석: [적정 타협] 현재 시스템 조건 안에서 손해와 이익을 나름대로 최적화한 구간입니다.")
    print("=" * 60)

if __name__ == '__main__':
    # 단독 테스트 실행
    result = calculate_normal_factory(speed=2.5, lanes=2, cleanliness=7)
    print_normal_dashboard(result)