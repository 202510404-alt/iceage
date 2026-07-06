# -*- coding: utf-8 -*-
import math

def calculate_normal_factory(speed, lanes, cleanliness):
    """
    기존 기계식 컨베이어 공정의 물리 및 산업공학 지표를 동적으로 계산하는 함수
    """
    # [고정 상수 정의]
    TOTAL_DELIVERY_DISTANCE = 4500  # 공장 내 격자 레일 총연장 길이 (4.5km)
    ITEM_VALUE = 200000             # 웨이퍼 1장당 가치 (20만 원)
    RAW_MATERIAL_COST = 50000       # 1장당 순수 원자재 원가 (5만 원)
    
    # [동적 생산량 계산 방식 적용]
    # 벨트가 한 줄일 때 시속 1m/s당 시간당 500장을 투입할 수 있다고 가정 (공장의 기본 물리적 한계)
    CAPACITY_PER_SPEED_LANE = 500 
    
    # 최종 투입 생산량 = 속도 * 차선수 * 단위 생산력
    # 속도가 빠르고 차선이 많을수록 공장 안으로 들어오는 웨이퍼가 동적으로 증가함
    total_produced = int(speed * lanes * CAPACITY_PER_SPEED_LANE)

    # [내부 물리 및 환경 지표 계산]
    # 속도가 빠를수록, 차선이 많아 교차로가 늘어날수록 물리 진동 증가
    vibration = speed * 10.0 * math.sqrt(lanes)
    
    # 청정도가 높으면 먼지가 줄지만, 기계식은 속도가 빠르면 마찰 분진이 추가 발생
    final_dust = max(0.1, (10 - cleanliness) + (speed * 1.5))

    # [품질 및 비용 페널티 계산]
    # 파손 불량률 (진동과 먼지에 비례, 차선 수가 많으면 분산 효과 반영)
    damage_rate = min(100.0, ((vibration * 0.5) + (final_dust * 0.8)) / lanes)

    # 청정도가 올라갈수록 관리 비용은 제곱(비선형)으로 폭증 (민석 학생 아이디어)
    clean_cost = (cleanliness ** 2) * 15000  
    wear_cost = (speed * 8000) * lanes       # 마찰 마모에 따른 부품 정비비
    fixed_cost = lanes * 100000              # 차선 증설에 따른 고정 설비 유지비
    total_management_cost = clean_cost + wear_cost + fixed_cost
    
    # 4.5km 주행 이동 시간 계산
    delivery_time_minutes = (TOTAL_DELIVERY_DISTANCE / speed) / 60

    # [최종 수율 및 재무적 순이익 계산]
    # 동적으로 결정된 생산량(total_produced)을 기준으로 불량품과 합격품 계산
    damaged_count = int(total_produced * (damage_rate / 100.0))
    perfect_count = total_produced - damaged_count

    gross_revenue = perfect_count * ITEM_VALUE
    loss_by_damage = damaged_count * RAW_MATERIAL_COST
    total_raw_material_cost = total_produced * RAW_MATERIAL_COST
    
    # 최종 순이익 계산
    net_profit = gross_revenue - total_raw_material_cost - loss_by_damage - total_management_cost

    # 결과를 딕셔너리로 반환 (main.py 연동용)
    return {
        "factory_type": "기계식 컨베이어 공정 (LINE A)",
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