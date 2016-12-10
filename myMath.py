import math

""" -----Notes-----
    1. CW returns negative angles
    2. CCW returns positive angles
"""

"""Returns the angle for an arc of given length"""
def getAngleFromArcLength(arcLength, radius):
    return abs(arcLength / radius)

"""Returns the length of an arc that has given angle and radius"""
def getArcLength(angle, radius):
    return abs(angle * radius)

"""Returns amount of pixels between two points"""
def getDistanceBetweenTwoPoints(point1Pos, point2Pos):
    return math.hypot(point2Pos[0] - point1Pos[0], point2Pos[1] - point1Pos[1])

"""Returns the position of a point on a circle with the given angle"""
def getPointOnCircleEdgeFromAngle(originPos, radius, angle):
    x = originPos[0] + radius * math.cos(angle)
    y = originPos[1] + radius * math.sin(angle)
    return (x, y)

"""Calculate a point between two points given a distance"""
def getPointBetweenTwoPoints(point1Pos, point2Pos, distance):
    distanceBetweenPoints = getDistanceBetweenTwoPoints(point1Pos, point2Pos)
    ratio = distance / distanceBetweenPoints

    x = (1 - ratio) * point1Pos[0] + ratio * point2Pos[0]
    y = (1 - ratio) * point1Pos[1] + ratio * point2Pos[1]

    return (x, y)

"""
Returns angles between two points on circle's edge in radians
"""
def getAngleBetweenPointsOnCircle(originPos, point1Pos, point2Pos):
    first  = math.atan2(point1Pos[1] - originPos[1], point1Pos[0] - originPos[0])
    second = math.atan2(point2Pos[1] - originPos[1], point2Pos[0] - originPos[0])
    return first - second
