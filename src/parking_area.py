from models import ParkingAreaType
import traci
import os
import helper

class ParkingArea():
    def __init__(self, type, costs, capacity, edge, pid, initial_occupacity):
        self.type = type
        self.costs = costs
        self.capacity = capacity
        self.edge = edge
        self.area_id = pid
        self.occupacity = round(capacity * initial_occupacity / 100)
        self.release_timestamps = []     
        self.target_position = helper.get_middle_of_edge_position(edge=edge)


    def get_type(self):
        return self.type

    def get_costs(self):
        return self.costs

    def get_capacity(self):
        return self.capacity
    
    def get_occupacity(self):
        return self.occupacity

    def get_edge(self):
        return self.edge
    
    def get_area_id(self):
        return self.area_id

    def get_vehicle_list(self):
        return self.vehicle_list    
    
    def get_available(self) -> int:
        return(int(self.get_capacity() - self.get_occupacity()))
    
    def reservate_parking_slot(self, release_timestamp):
        self.occupacity +=1
        self.release_timestamps.append(release_timestamp)
        return True
    
    def get_release_timestamps(self):
        return self.release_timestamps
    
    def remove_release_timestamp(self, timestamp):
        self.release_timestamps.remove(timestamp)
    
    def release_parking_slots(self, amount):
        self.occupacity -=amount

    def add_poi(self):
        if self.type == ParkingAreaType.OFF_STREET:
            imgFile=os.path.abspath("./src/img/off_street_parking.png")
            size = 20
            layer = 11
        elif self.type == ParkingAreaType.ON_STREET:
            imgFile=os.path.abspath("./src/img/on_street_parking.png")
            size = 15
            layer = 10

        poi_id = "pid" + str(self.area_id)
        traci.poi.add(color=(100,255,255,255), x=self.target_position[0], y=self.target_position[1], poiID=poi_id, 
                      poiType="parking", width=size, height=size, layer=layer, imgFile=imgFile)
