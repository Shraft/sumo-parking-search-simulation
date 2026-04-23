import traci
import math


def get_edge_vektor(edge):
    from_junction = traci.edge.getFromJunction(edgeID=edge)
    to_junction = traci.edge.getToJunction(edgeID=edge)

    from_pos = traci.junction.getPosition(junctionID=from_junction)
    to_pos = traci.junction.getPosition(junctionID=to_junction)

    edge_vektor = (
            to_pos[0] - from_pos[0],
            to_pos[1] - from_pos[1]
        )
    
    return(edge_vektor)
    

def get_vektor_of_two_points(p1, p2):
    vektor = (
            p2[0] - p1[0],
            p2[1] - p1[1]
        )
    return(vektor)


def calc_crossproduct(v1, v2):
    norm_v1 = math.hypot(*v1)
    norm_v2 = math.hypot(*v2)

    # no division by zero
    if norm_v1 == 0 or norm_v2 == 0:
        return 0.0  

    # Skalarprodukt
    angle = math.acos((v1[0]*v2[0] + v1[1]*v2[1]) / (norm_v1 * norm_v2))

    return round(math.degrees(angle), 2)


def get_middle_of_edge_position(edge):
    from_junction = traci.edge.getFromJunction(edgeID=edge)
    to_junction = traci.edge.getToJunction(edgeID=edge)

    from_pos = traci.junction.getPosition(junctionID=from_junction)
    to_pos = traci.junction.getPosition(junctionID=to_junction)

    position  = (
                int(((to_pos[0] - from_pos[0]) / 2) + from_pos[0]),
                int(((to_pos[1] - from_pos[1]) / 2) + from_pos[1])
                )
    
    return(position)


def get_distance_between_points(p1, p2):
    return(round(math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)))


def get_distance_between_edges(edge1, edge2):
    middle_of_edge1 = get_middle_of_edge_position(edge=edge1)
    middle_of_edge2 = get_middle_of_edge_position(edge=edge2)

    return(get_distance_between_points(p1=middle_of_edge1, p2=middle_of_edge2))

def check_if_edge_in_city(edge, city_center):
    pos_of_edge = get_middle_of_edge_position(edge=edge)
    city_center_pos = (city_center[0], city_center[1])
    city_center_radius = city_center[2]
    distance = get_distance_between_points(p1=city_center_pos, p2=pos_of_edge)
    if distance < city_center_radius:
        return(True)
    else:
        return(False)