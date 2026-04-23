import pytest
from parking_area_utility_calculator import ParkingAreaCostCalculator



def test_normalize_price():
    calc = ParkingAreaCostCalculator(0.6, 0.4, 1000)

    result = calc._normalize_price(2)
    assert result == 2 


def test_normalize_distance():
    calc = ParkingAreaCostCalculator(0.6, 0.4, 1000)

    result = calc._normalize_distance(500)
    assert result == 2 


def test_calc_parking_area_utility():
    calc = ParkingAreaCostCalculator(0.6, 0.4, 1000)

    result = calc._calc_parking_area_utility(distance=500, price=2)

    assert result == pytest.approx(2)


def test_calc_parking_area_improvement():
    calc = ParkingAreaCostCalculator(0.6, 0.4, 1000)

    result = calc._calc_parking_area_improvement(distance_obervations=[500], price_obersvations=[2], scoutings=4)
    result = round(result,2)

    assert result == pytest.approx(1.96)


def test_evaluate_parking_area_pass():
    calc = ParkingAreaCostCalculator(0.6, 0.4, 1000)

    result = calc.evaluate_parking_area(parking_area_distance=300, parking_area_price=3, 
                                        price_obersvations=[2], distance_obervations=[500],
                                        scoutings=4)
    
    result = round(result,2)

    assert result == pytest.approx(0)


def test_evaluate_parking_area_take():
    calc = ParkingAreaCostCalculator(0.6, 0.4, 1000)

    result = calc.evaluate_parking_area(parking_area_distance=200, parking_area_price=1, 
                                        price_obersvations=[2], distance_obervations=[500],
                                        scoutings=4)
    
    result = round(result,2)

    assert result == pytest.approx(1)









