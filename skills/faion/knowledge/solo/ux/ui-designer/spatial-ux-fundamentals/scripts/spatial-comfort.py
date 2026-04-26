#!/usr/bin/env python3
"""
spatial-comfort.py — compute XR element sizing requirements at a given placement distance.
Input: distance in meters, minimum visual angle in degrees (default 0.5 for text)
Output: minimum element size, interaction target size, comfort zone classification
Usage: python spatial-comfort.py <distance_meters> [min_visual_angle_degrees]
"""
import sys
import math

distance = float(sys.argv[1]) if len(sys.argv) > 1 else 1.0
min_angle_deg = float(sys.argv[2]) if len(sys.argv) > 2 else 0.5  # 0.5 deg min for readable text

min_angle_rad = math.radians(min_angle_deg)
min_size_m = 2 * distance * math.tan(min_angle_rad / 2)
min_size_cm = min_size_m * 100

# Interaction target minimum: 1.5 degrees visual angle
interact_angle_rad = math.radians(1.5)
interact_size_m = 2 * distance * math.tan(interact_angle_rad / 2)
interact_size_cm = interact_size_m * 100

if distance < 1:
    zone = "Near field (<1m) — primary interactions, menus, immediate feedback"
elif distance < 3:
    zone = "Mid field (1-3m) — work surfaces, content consumption (RECOMMENDED DEFAULT)"
else:
    zone = "Far field (3m+) — navigation anchors, environmental context only"

print(f"Distance:          {distance}m")
print(f"Comfort zone:      {zone}")
print(f"Min text size:     {min_size_cm:.2f}cm  ({min_angle_deg}° visual angle)")
print(f"Min touch target:  {interact_size_cm:.2f}cm  (1.5° visual angle)")

if distance < 0.5:
    print("WARNING: Below 0.5m — vergence-accommodation conflict zone, avoid interactive elements")
elif distance > 25:
    print("WARNING: Above 25° vertical limit — risk of neck strain for persistent UI")
