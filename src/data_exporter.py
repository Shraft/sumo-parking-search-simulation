from datetime import datetime
import time
import os
import shutil
import csv
import statistics
from vehicle_manager import VehicleManager
from parking_area_manager import ParkingAreaManager
from simconfig import SimConfig
import traci
import json

class DataExporter():
    def __init__(self, simconfig: SimConfig, simconfig_file, vehicle_manager: VehicleManager, parking_area_manager: ParkingAreaManager):
        
        self.simconfig_file = simconfig_file
        self.simconfig = simconfig
        self.vehicle_manager = vehicle_manager
        self.parking_area_manger = parking_area_manager
        self.arrived_vehicles = []
        self.global_metrics = []
        self.live_metrics = {}
        self.simulation_start_timestamp = datetime.now()

        self.base_path = "sim_results/"
        time_string = self.simulation_start_timestamp.strftime("%H:%M:%S_%d-%m-%Y")
        self.simulation_name = self.simconfig.get_sim_name() + "_" + time_string + "_pid" + str(os.getpid())
        self.export_path = self.base_path + self.simulation_name + "/"

        # check if dir already exists
        if os.path.isdir(self.export_path):
            print("DataExporter: target directory already exists, abording")
            exit()

        # create dir
        try:
            os.makedirs(self.export_path)
        except:
            print(f"DataExporter: Error while creating results directory")

        # copy simconfig to results
        target_file = self.export_path + "simconfig.json"
        shutil.copyfile(self.simconfig_file, target_file)
        print("DataExporter: results directory prepared")

    def get_export_path(self):
        return(str(self.export_path))

    def add_arrived_vehicle(self, vid, travel_time, cruising_time, remaining_distance, cruising_time_share, 
                            track_length, departure_timestamp, arrival_timestamp):
        if not any(v["vehicle_id"] == vid for v in self.arrived_vehicles):
            self.arrived_vehicles.append({
                "vehicle_id": vid,
                "arrival_timestamp": arrival_timestamp,
                "departure_timestamp": departure_timestamp,
                "travel_time": travel_time,
                "cruising_time": cruising_time,
                "remaining_distance": remaining_distance,
                "cruising_time_share": cruising_time_share,
                "track_length": track_length
            })
             
        
    def add_global_metric(self, timestamp):
        local_time = time.strftime("%H:%M", time.gmtime(timestamp))
        cruising_traffic_share = self.vehicle_manager.get_cruising_traffic_share()
        vehicle_count = traci.vehicle.getIDCount()
        vehicles_added = self.vehicle_manager.get_vehicles_added()
        basic_data = {"timestamp": timestamp, 
                "local_time": local_time, 
                "cruising_traffic_share": cruising_traffic_share, 
                "vehicles_added": vehicles_added,
                "total_vehicle_count": vehicle_count,
                "arrived_vehicles": len(self.arrived_vehicles)}
        
        parking_area_data = self.parking_area_manger.get_overall_parking_area_occupacity()

        data = basic_data | parking_area_data

        self.global_metrics.append(data)

        self.vehicle_manager.clear_vehicles_added()
        

    def export_vehicle_metrics(self):
        # prepare export
        data = self.arrived_vehicles
        filename = "vehicle_metrics.csv"
        path = self.export_path + filename

        key_map = {
                "vehicle_id": "VehicleID",
                "departure_timestamp": "Timestamp of departure",
                "arrival_timestamp": "Timestamp of arrival",
                "travel_time": "Travel-Time (min)",
                "cruising_time": "Cruising-Time (min)",
                "track_length": "Track Length (meter)",
                "remaining_distance": "Remaining-Distance (meters)",
                "cruising_time_share": "Cruising-Time-Share (%)"
                }

        csv_fieldnames = list(key_map.values())

        # automatisch umformatieren
        formatted_data = [
            {csv_name: entry[key] for key, csv_name in key_map.items()}
            for entry in data
        ]

        with open(path, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=csv_fieldnames)
            writer.writeheader()
            writer.writerows(formatted_data)


    def export_global_metrics(self):
        # prepare
        data = self.global_metrics
        filename = "global_metrics.csv"
        path = self.export_path + filename
        key_map = {
                "timestamp": "Timestamp",
                "local_time": "local time",
                "cruising_traffic_share": "Cruising-Traffic-Share (%)",
                "vehicles_added": "vehicles added",
                "total_vehicle_count": "current vehicle count",
                "arrived_vehicles": "arrived vehicles",
                "on_street_nominal_max": "on-street capacity",
                "on_street_nominal_occupacity": "on-street occupacity",
                "on_street_occupacity_share": "on-street occupacity-share (%)",
                "off_street_nominal_max": "off-street  capacity",
                "off_street_nominal_occupacity": "off-street occupacity",
                "off_street_occupacity_share": "off-street occupacity (%)",
                "global_nominal_max": "global capacity",
                "global_nominal_occupacity": "global occupacity",
                "global_occupacity_share": "global occupacity (%)"
                }

        csv_fieldnames = list(key_map.values())

        formatted_data = [
            {csv_name: entry[key] for key, csv_name in key_map.items()}
            for entry in data
        ]

        with open(path, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=csv_fieldnames)
            writer.writeheader()
            writer.writerows(formatted_data)

    
    def export_live_metrics(self, progress):
        now = datetime.now()
        time_running = round(((now - self.simulation_start_timestamp).seconds), 2)
        running_hours = int(time_running // 3600)
        running_minutes = int((time_running % 3600) // 60)
        running_seconds = int(time_running % 60)
        running_str = f"{running_hours} h {running_minutes} min {running_seconds} sec"

        vehicle_count = traci.vehicle.getIDCount()
        
        eta = round(time_running / (progress / 100) - time_running, 2)

        eta_hours = int(eta // 3600)
        eta_minutes = int((eta % 3600) // 60)
        eta_seconds = int(eta % 60)
        ETA_str = f"{eta_hours} h {eta_minutes} min {eta_seconds} sec"
        
        live_info = {"progress": str(progress) + "%",
                    "running_for": running_str,
                    "ETA": ETA_str,
                    "vehicle_count": vehicle_count}
        self.live_metrics["simulation name"] = self.simulation_name
        self.live_metrics["simulation description"] = self.simconfig.get_sim_description()
        self.live_metrics["live_info"] = live_info
        self.live_metrics["global"] = self.global_metrics[-1]

        live_info_path = self.export_path + "live_info.json"
        with open(live_info_path, "w", encoding="utf-8") as f:
            json.dump(self.live_metrics, f, indent=4, ensure_ascii=False)