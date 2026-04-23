import argparse
from simconfig import SimConfig
from data_exporter import DataExporter
from models import ParkingAreaType, VehicleState
import traci
from parking_area import ParkingArea
from vehicle import Vehicle
from vehicle_manager import VehicleManager
from sumo_step_listener import SumoStepListener
from parking_area_manager import ParkingAreaManager
import random


if __name__ == "__main__":
    # Parse Arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--sumo-mode", help='cli or gui', default="gui")
    parser.add_argument("--sim-config", help='Simulation configuration', default="simconfig.json")
    parser.add_argument("--sumo-config", help='Sumo config file', default="./MoSTScenario/scenario/most.sumocfg")
    parser.add_argument("--debug", help="set debug mode", default=False)
    parser.add_argument("--debug-vehicle", help="choose vehicle to show debug messages", default=None)
    parser.add_argument("--seed", help="choose vehicle to show debug messages", default=None)
    args = parser.parse_args()

    if args.sumo_mode == "gui":
        sumo_mode = "sumo-gui"
    elif args.sumo_mode =="cli":
        sumo_mode = "sumo"
    else:
        print("Parser: mode not accepted")
        exit()

    # load simconfig
    simconfig = SimConfig(path=args.sim_config, debug=bool(args.debug))
    simconfig.load_configuration()

    # create vehicle_manager
    vehicle_manager = VehicleManager(simconfig=simconfig)
    parking_area_manager = ParkingAreaManager(simconfig=simconfig)

    # create exporter
    exporter = DataExporter(simconfig=simconfig, simconfig_file=args.sim_config,
                            vehicle_manager=vehicle_manager, parking_area_manager=parking_area_manager)
    
    print(f"Starting Simulation: {simconfig.get_sim_name()}")

    # run simulation
    seed = random.randint(0, 2**31 - 1)
    sumo_cmd = [sumo_mode, "-c", args.sumo_config, 
                    "--step-length", "0.25", 
                    "--delay", "100", "--start",
                    "--begin", str(simconfig.get_sim_start()),
                    "--end", str(simconfig.get_sim_end()),
                    "--no-warnings", "--log", "sumo.log", 
                    "--error-log", "sumo_error.log",
                    "--quit-on-end", "--seed", str(seed)]
    traci.start(sumo_cmd)
    traci.addStepListener(SumoStepListener(simconfig=simconfig, vehicle_manager=vehicle_manager, 
                                           parking_area_manager=parking_area_manager, exporter=exporter,
                                           debug_vehicle=args.debug_vehicle))

    # init parking areas
    parking_area_manager.init_parking_areas()

    while traci.simulation.getTime() < simconfig.get_sim_end():
        traci.simulationStep()

    # end simulation
    traci.close()

    # export metrics
    exporter.export_vehicle_metrics()
    exporter.export_global_metrics()