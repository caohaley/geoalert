import json

# Helper Functions
def orientation(point1, point2, point3):
	'''
	The three points can only be in 3 types of orientation.

	The orientations are defined based on slopes. More information can be found on:
	https://www.geeksforgeeks.org/orientation-3-ordered-points/
	'''

	check = float(point2[1]-point1[1]) * float(point3[0]-point2[0]) - float(point2[0] - point1[0]) * float(point3[1]-point2[1])

	if check == 0 or abs(check) <= 1.0E-8: # Can be adjusted
		return 0 # collinear
	elif check > 0:
		return 1 # clockwise
	else:
		return 2 # counter-clockwise

def checkOnLine(point, lineA, lineB) -> bool:
	'''
	Check if the point in on the line (where the line is defined by points lineA, lineB) where
	the point is already collinear with lineA and lineB.
	'''

	if (point[0] <= max(lineA[0], lineB[0])) and (point[0] >= min(lineA[0], lineB[0])) and (point[1] <= max(lineA[1], lineB[1])) and (point[1] >= min(lineA[1], lineB[1])):
		return True
	else:
		return False

def checkIntersection(line1A, line1B, line2A, line2B) -> bool:
	'''
	Check if line 1 (pointA, pointB) intersects with line 2 (pointA, pointB).

	You may determine if two lines will cross using orientations. More information can be found
	on: https://www.geeksforgeeks.org/check-if-two-given-line-segments-intersect/
	'''

	orientation1 = orientation(line1A, line1B, line2A)
	orientation2 = orientation(line1A, line1B, line2B)
	orientation3 = orientation(line2A, line2B, line1A)
	orientation4 = orientation(line2A, line2B, line1B)

	if orientation1 != orientation2 and orientation3 != orientation4:
		return True

	# Collinear and lies on line
	if orientation1 == 0 and checkOnLine(line2A, line1A, line1B):
		return True

	if orientation2 == 0 and checkOnLine(line2B, line1A, line1B):
		return True

	if orientation3 == 0 and checkOnLine(line1A, line2A, line2B):
		return True

	if orientation4 == 0 and checkOnLine(line1B, line2A, line2B):
		return True

	return False

def checkPointInsidePolygon(point, polygons) -> bool:
	'''
	Check if point is inside any of the polygons.
	
	Use the method where we know a point is inside a polygon if we cross polygon borders
	an odd number of times drawing any line from the point in any direction to infinite.
	'''
	numIntersections = 0

	line1A = point
	line1B = [point[0], 1000.0] # Use a number larger than both max longitude and max latitude

	for polygon in polygons:
		numPoints = len(polygon)

		if numPoints < 4: # In geojson, you must add the last coordinate to be same as the beginning coordinate
			continue

		for i in range(1, numPoints):
			line2A = polygon[i-1]
			line2B = polygon[i]

			if checkIntersection(line1A, line1B, line2A, line2B):
				numIntersections += 1

	return (numIntersections % 2 == 1)

def parseJson(jsonObject):
	'''
	Parse geojson object to extract clinician location point(point) and bounding zones(polygons).
	'''
	point = None
	polygons = None

	if len(jsonObject["features"]) != 0:
		for feature in jsonObject["features"]:
			if feature["geometry"] and feature["geometry"]["type"]:
				if feature["geometry"]["type"] == "Point":
					point = feature["geometry"]["coordinates"]

				if feature["geometry"]["type"] == "Polygon":
					if polygons == None:
						polygons = []
					for coord in feature["geometry"]["coordinates"]:
						polygons.append(coord)

	return point, polygons
