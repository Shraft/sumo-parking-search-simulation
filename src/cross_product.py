import math

v1 = (1,1)
v2 = (0,1)

angle = math.acos(
    (v1[0]*v2[0] + v1[1]*v2[1]) /
    (math.hypot(*v1) * math.hypot(*v2))
)

print(math.degrees(angle))