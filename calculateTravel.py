import math
import utilities

"""
This is the function that calculates the distance travelled by both robots
The output will be the longest distance travelled by the robots
If simulate is True, the function returns a tuple of info needed for the simulation
"""
def calculateTravel(diskPos, radius, r1StartPos, r2StartPos, exitPos, simulate=False):
    """
    Both robots start in the center of disk
    Both robots must travel a distance of radius to reach same point on disk edge
    """
    r1TravelToEdge = radius
    r2TravelToEdge = radius
    pointOnCircleAtAngleZero = utilities.getPointOnCircleEdgeFromAngle(diskPos, radius, 0)
    startPointOnEdge = pointOnCircleAtAngleZero
    r1TravelOnCircleEdge = 0
    r2TravelOnCircleEdge = 0
    whichRobotDidntFindExit = 0
    posOfRobotWhoDidntFindExit = (0,0)

    """
    One or both robots do not start on center position
    Find which robot is closest to edge of circle and find closest point to reach it
    Calculate distance from both robots to point on the edge
    """
    if(r1StartPos != diskPos or r2StartPos != diskPos):
        startPointOnEdge = getClosestPointOnEdge(r1StartPos, r2StartPos, diskPos, radius)
        print('startPointOnEdge:', startPointOnEdge)

        r1TravelToEdge = utilities.getDistanceBetweenTwoPoints(r1StartPos, startPointOnEdge)
        r2TravelToEdge = utilities.getDistanceBetweenTwoPoints(r2StartPos, startPointOnEdge)
        print('r1TravelToEdge:', r1TravelToEdge)
        print('r2TravelToEdge:', r2TravelToEdge)
        print('------------------------------')

    """
    We now need to find which robot will find exit first
    R1 always goes CCW and R2 always goes CW
    CCW is positive and CW is negative
    """
    angleBetweenStartAndEnd = utilities.getAngleBetweenPointsOnCircle(diskPos, startPointOnEdge, exitPos)
    print('angleBetweenStartAndEnd:', math.degrees(angleBetweenStartAndEnd))

    r1Angle = angleBetweenStartAndEnd
    r2Angle = angleBetweenStartAndEnd

    if(r1Angle < 0):
        r1Angle = 2 * math.pi + r1Angle
    if(r2Angle > 0):
        r2Angle = 2 * math.pi - r2Angle
    print('r1Angle:', r1Angle, math.degrees(r1Angle))
    print('r2Angle:', r2Angle, math.degrees(r2Angle))

    r1TravelOnCircleEdge = utilities.getArcLength(r1Angle, radius)
    r2TravelOnCircleEdge = utilities.getArcLength(r2Angle, radius)

    """Robot with shortest travel must find exit first"""
    if(r1TravelOnCircleEdge + r1TravelToEdge <= r2TravelOnCircleEdge + r2TravelToEdge):
        r2TravelOnCircleEdge = r1TravelOnCircleEdge - (r2TravelToEdge - r1TravelToEdge)
        whichRobotDidntFindExit = 2
    else:
        r1TravelOnCircleEdge = r2TravelOnCircleEdge - (r1TravelToEdge - r2TravelToEdge)
        whichRobotDidntFindExit = 1

    if(r1TravelOnCircleEdge < 0):
        r1TravelOnCircleEdge = 0
    if(r2TravelOnCircleEdge < 0):
        r2TravelOnCircleEdge = 0
    print('r1TravelOnCircleEdge:', r1TravelOnCircleEdge)
    print('r2TravelOnCircleEdge:', r2TravelOnCircleEdge)
    print('------------------------------')
    print('whichRobotDidntFindExit:', whichRobotDidntFindExit)

    if(whichRobotDidntFindExit == 1 and r2TravelToEdge + r2TravelOnCircleEdge < r1TravelToEdge):
        r1TravelToEdge = r2TravelToEdge + r2TravelOnCircleEdge
        r1TravelOnCircleEdge = 0
    elif(whichRobotDidntFindExit == 2 and r1TravelToEdge + r1TravelOnCircleEdge < r2TravelToEdge):
        r2TravelToEdge = r1TravelToEdge + r1TravelOnCircleEdge
        r2TravelOnCircleEdge = 0

    """Find position of robot when exit is found by the other robot"""
    if(whichRobotDidntFindExit == 1):
        tempAngle = -1 * utilities.getAngleFromArcLength(r1TravelOnCircleEdge, radius)
        posOfRobotWhoDidntFindExit = utilities.getPointOnCircleEdgeFromAngle(diskPos, radius, tempAngle - utilities.getAngleBetweenPointsOnCircle(diskPos, pointOnCircleAtAngleZero, startPointOnEdge))
    else:
        tempAngle = utilities.getAngleFromArcLength(r2TravelOnCircleEdge, radius)
        posOfRobotWhoDidntFindExit = utilities.getPointOnCircleEdgeFromAngle(diskPos, radius, tempAngle - utilities.getAngleBetweenPointsOnCircle(diskPos, pointOnCircleAtAngleZero, startPointOnEdge))
    print('posOfRobotWhoDidntFindExit:', posOfRobotWhoDidntFindExit)

    """Distance traveled for second robot to exit"""
    travelToEnd = utilities.getDistanceBetweenTwoPoints(posOfRobotWhoDidntFindExit, exitPos)
    print('travelToEnd:', travelToEnd)

    if(whichRobotDidntFindExit == 1):
        totalTravel = r1TravelToEdge + r1TravelOnCircleEdge + travelToEnd
    else:
        totalTravel = r2TravelToEdge + r2TravelOnCircleEdge + travelToEnd

    print('r1Travel:', r1TravelToEdge + r1TravelOnCircleEdge)
    print('r2Travel:', r2TravelToEdge + r2TravelOnCircleEdge)

    if(simulate):
        return(
            startPointOnEdge,
            r1TravelToEdge,
            r2TravelToEdge,
            r1TravelOnCircleEdge,
            r2TravelOnCircleEdge,
            totalTravel
        )
    else:
        return totalTravel


def getClosestPointOnEdge(point1Pos, point2Pos, originPos, radius):
    point1DistanceFromEdge = (radius - utilities.getDistanceBetweenTwoPoints(point1Pos, originPos))
    point2DistanceFromEdge = (radius - utilities.getDistanceBetweenTwoPoints(point2Pos, originPos))
    angleToEdge = 0
    print('Distances from edge of circle', point1DistanceFromEdge, point2DistanceFromEdge)

    """Need to find angle that creates point on edge with shortest distance from closest point"""
    if(point1DistanceFromEdge <= point2DistanceFromEdge):
        angleToEdge = utilities.getAngleBetweenPointsOnCircle(originPos, point1Pos, utilities.getPointOnCircleEdgeFromAngle(originPos, radius, 0))
        print('angleToEdge point1:', angleToEdge, math.degrees(angleToEdge))
    else:
        angleToEdge = utilities.getAngleBetweenPointsOnCircle(originPos, point2Pos, utilities.getPointOnCircleEdgeFromAngle(originPos, radius, 0))
        print('angleToEdge point2:', angleToEdge, math.degrees(angleToEdge))

    return utilities.getPointOnCircleEdgeFromAngle(originPos, radius, angleToEdge)
