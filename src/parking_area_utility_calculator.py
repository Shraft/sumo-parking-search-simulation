import math
from models import VehicleState
from simconfig import SimConfig


class ParkingAreaCostCalculator():
    def __init__(self, simconfig: SimConfig):
        self.simconfig = simconfig
        self.f_price = self.simconfig.get_cost_distribution_price_weigth()
        self.f_distance = self.simconfig.get_cost_distribution_distance_weigth()


    def _normalize_distance(self, distance):
        return 1 - min(distance / self.simconfig.get_search_radius(), 1)

    def _normalize_price(self, price):
        return 1 - min(price / self.simconfig.get_max_parking_price(), 1)



    def _calc_propability_parking_area_incomming(self, x, scoutings, observation_length, vehicle_state):
        if vehicle_state == VehicleState.CRUISING_TO_TARGET:
            return(1)
        elif vehicle_state == VehicleState.CRUISING_FOR_PARKING:
            if observation_length == 0 or scoutings == 0:
                return(0)
            else:
                return(round(1-math.exp(-(scoutings/observation_length)*x), 2))


    def _calc_parking_area_utility(self, price, distance):
        normalized_price = self._normalize_price(price)
        normalized_distance = self._normalize_distance(distance)

        return(self.f_price * normalized_price + self.f_distance * normalized_distance)


    def _calc_parking_area_improvement(self, scoutings, price_obersvations, distance_obervations, observation_length, 
                                       distance_to_target, vehicle_state):
        # get propability that a parking area will come at all
        propability_parking_area_incomming = self._calc_propability_parking_area_incomming(x=distance_to_target, 
                                                                                           scoutings=scoutings, 
                                                                                           observation_length=observation_length,
                                                                                           vehicle_state=vehicle_state)
        #print(f"probability pa incoming {propability_parking_area_incomming}")

        # calculate average expected utility of parking areas
        average_price = sum(price_obersvations) / len(price_obersvations)
        average_distance = sum(distance_obervations) / len(distance_obervations)
        average_expected_parking_area_utility = self._calc_parking_area_utility(price=average_price, 
                                                                                distance=average_distance)
        
        #print(f"avg utility {average_expected_parking_area_utility}")

        return(propability_parking_area_incomming * average_expected_parking_area_utility)


    def evaluate_parking_area(self, parking_area_price, parking_area_distance,
                              price_obersvations, distance_obervations,
                              scoutings, observation_length, distance_to_target,
                              vehicle_state):
        # get utility value of current parking spot
        current_utility = self._calc_parking_area_utility(price=parking_area_price, 
                                                          distance=parking_area_distance)
        current_utility = round(current_utility, 2)

        #print(f"current utility {current_utility}")

        # get propability of bether paring area
        improvement_utility = self._calc_parking_area_improvement(scoutings=scoutings, price_obersvations=price_obersvations, 
                                                                  distance_obervations=distance_obervations, 
                                                                  observation_length=observation_length, 
                                                                  distance_to_target=distance_to_target,
                                                                  vehicle_state=vehicle_state)
        improvement_utility = round(improvement_utility, 2)

        #print(f"Compare U_now={current_utility} with U_inc={improvement_utility}")

        # compare and decide between stay or continue search
        if current_utility >= improvement_utility:
            return True
        else:
            return False
