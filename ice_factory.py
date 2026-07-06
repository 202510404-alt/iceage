# -*- coding: utf-8 -*-
import math

def calculate_ice_factory(speed, lanes, cleanliness):
    """
    초전도 자기부상(ICE) 컨베이어 공정의 물리 및 산업공학 지표를 동적으로 계산하는 함수
    """
    # [통제 변수: 일반 공장과 완전히 동일한 기본 상수 설정]
    TOTAL_DELIVERY_DISTANCE = 4500  # 공장 내 격자 레일 총연장 길이 (4.5km)
    ITEM_VALUE = 200000             # 웨이퍼 1장당 가치 (20만 원)
    RAW_MATERIAL_COST = 50000       # 1장당 순수 원자재 원가 (5만 원)
    
    # [동적 생산량 계산]
    # 초전도 시스템은 기본 물리적 수송 능력이 기계식보다 뛰어남 (시속 1m/s당 600장 투입 가능으로 설정)
    CAPACITY_PER_SPEED_LANE = 600 
    total_produced = int(speed * lanes * CAPACITY_PER_SPEED_LANE)

    # [물리학적 특성 반영: 완전 반자성(마이스너 효과)]
    # 공중에 부상하여 이동하므로 속도와 차선이 늘어나도 물리적 마찰 진동은 '0'입니다.
    vibration = 0.0
    
    # 비접촉 주행이므로 기계 마찰 분진은 0입니다. 
    # 오직 클린룸 자체의 청정도 설정에 의해서만 미세 먼지량이 결정됩니다.
    final_dust = max(0.1, float(10 - cleanliness))

    # [품질 지표 계산]
    # 마이스너 효과로 진동 파손율은 0%입니다. 
    # 오직 공기 중 미세 먼지가 흡착되어 발생하는 오염 불량률만 아주 미세하게 존재합니다.
    damage_rate = min(100.0, final_dust * 0.05)

    # [산업공학적 비용 및 제약 조건 계산 (민석 학생 아이디어 반영)]
    # 1. 청정실 기본 유지비 (일반 공장과 동일하게 제곱 비선형 적용)
    clean_cost = (cleanliness ** 2) * 15000  
    
    # 2. 기계 마모 정비비 소멸
    # 비접촉식이므로 마찰 마모에 따른 부품 정비 비용은 0원입니다.
    wear_cost = 0 

    # 3. 민석's 현실 반영 제약: 초전도 냉각비 및 면적 차지 비용
    # 레일 전체를 액체질소 및 극저온으로 유지하는 냉각 비용은 차선 수(면적)에 비례하여 증가합니다.
    # 또한 레일이 차지하는 면적 비용과 기본 차선 고정 설비비가 합산됩니다.
    base_cooling_per_lane = 250000  # 차선당 기본 극저온 냉각 전력/밀봉 비용
    space_cost_per_lane = 150000    # 차선 증가에 따른 공장 면적 점유 기회비용
    
    # 민석's 현실 반영 보너스: 차선 수가 많아지면 물류가 분산되어 개별 레일의 열 부하가 미세하게 감소함
    lane_efficiency_bonus = max(0.8, 1.0 - (lanes - 1) * 0.05) 
    
    # 최종 초전도 관련 고정/운영 비용 계산
    total_ice_system_cost = (base_cooling_per_lane + space_cost_per_lane) * lanes * lane_efficiency_bonus
    
    # 전체 관리 비용 합산
    total_management_cost = clean_cost + wear_cost + total_ice_system_cost
    
    # 4.5km 주행 이동 시간 계산 (초전도는 고속 주행이 원활하므로 시간이 극단적으로 단축됨)
    delivery_time_minutes = (TOTAL_DELIVERY_DISTANCE / speed) / 60

    # [최종 수율 및 재무적 순이익 계산]
    damaged_count = int(total_produced * (damage_rate / 100.0))
    perfect_count = total_produced - damaged_count

    gross_revenue = perfect_count * ITEM_VALUE
    loss_by_damage = damaged_count * RAW_MATERIAL_COST
    total_raw_material_cost = total_produced * RAW_MATERIAL_COST
    
    # 최종 순이익 계산
    net_profit = gross_revenue - total_raw_material_cost - loss_by_damage - total_management_cost

    # 결과를 딕셔너리로 반환 (main.py 연동용)
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
    결과 시각화를 위한 출력 함수
    """
    print("\n" + "=" * 60)
    print(f" [{res['factory_type']} 결과 대시보드] ")
    print("=" * 60)
    print(f"■ 공장 운영 설정: 이송속도 {res['speed']}m/s | 레일 {res['lanes']}줄 | 청정설정 {res['cleanliness']}단계")
    print(f"■ 물리 환경 지표: 레일 진동수 {res['vibration']:.1f} Hz (마이스너 효과) | 자체분진 제거 완료")
    print(f"■ 물류 배달 시간: 4.5km 구간 이동 시 평균 {res['delivery_time']:.1f}분 소요")
    print("-" * 60)
    print(f"■ [품질] 반도체 부품 파손율 : {res['damage_rate']:.2f} % (오직 환경 불량만 존재)")
    print(f"■ [생산] 시간당 총 투입량   : {res['total_produced']} 장 (초전도 수송력 향상 반영)")
    print(f"■ [결과] 최종 합격품 수량   : {res['perfect_count']} 장 / 불량품: {res['damaged_count']} 장")
    print("-" * 60)
    print(f"▶ 초전도 냉각/면적 및 관리비: {res['management_cost']:,.0f} 원 (차선 제약 비용 반영)")
    print(f"▶ 공장 최종 재무적 순이익 : {res['net_profit']:,.0f} 원")
    print("=" * 60)
    
    print(" [산업공학적 의사결정 인사이트] ")
    if res['net_profit'] < 0:
        print("결과 분석: [초기 과도기] 냉각비와 면적 비용에 비해 이송 속도가 너무 느려 생산량이 비용을 충당하지 못합니다.")
    else:
        print("결과 분석: [혁신 달성] 높은 냉각 비용 제약을 극복할 만큼 고속 대량 수송을 통해 압도적인 순이익을 창출했습니다.")
    print("=" * 60)

if __name__ == '__main__':
    # 단독 테스트 실행
    result = calculate_ice_factory(speed=4.5, lanes=1, cleanliness=7)
    print_ice_dashboard(result)