import pygame
import math
import myMath

"""
    This class is used to update and draw the robot during the simulation
"""
class Robot:
    def __init__(self, disk, startPosition, exitPos, startPointOnEdge,
                travelToEdge, travelOnCircleEdge, movesClockWise):
        self.speed = 125                     #Amount of pixels moved per second
        self.reachedEdge  = False            #Has robot reached circle edge
        self.reachedAngle = False            #Has robot reached angle when exit is found
        self.reachedExit  = False            #Has robot reached exit
        self.distanceTravelled = 0           #Distance travelled in simulation

        self.origin = disk.getOrigin()       #Origin of the disk
        self.radius = disk.getRadius()       #Radius of disk
        self.x = startPosition[0]            #Starting position of robot, x coordinate
        self.y = startPosition[1]            #Starting position of robot, y coordinate
        self.exitPos = exitPos               #Exit's position
        self.movesClockWise = movesClockWise #Does robot move clockwise?
        self.travelOnCircleEdge = travelOnCircleEdge #Distance travelled on circle edge

        """Need to recalculate this in case exit is found before robot reaches circle edge"""
        self.startPointOnEdge = myMath.getPointBetweenTwoPoints((self.x, self.y), startPointOnEdge, travelToEdge)

        """Calculates angle of the startPointOnEdge"""
        self.angle = myMath.getAngleBetweenPointsOnCircle(self.origin, (self.origin[0] + self.radius, self.origin[1]), self.startPointOnEdge)

        """Calculates the angle robot reaches when exit is found"""
        self.angleOnCircleEdge = myMath.getAngleFromArcLength(self.travelOnCircleEdge, self.radius)
        if(self.movesClockWise):
            self.angleOnCircleEdge = self.angle - self.angleOnCircleEdge
            self.color = (0,0,255)
        else:
            self.angleOnCircleEdge = self.angle + self.angleOnCircleEdge
            self.color = (255,0,0)

    """
    Draw function draws a circle to represent robot
    Called every frame during Main Loop
    """
    def draw(self, screen, font):
        if(self.reachedExit):
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), 10, 0)
        else:
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), 10, 1)

        screen.set_at((int(self.x), int(self.y)), self.color)

        string = 'Robot 1: '
        if(self.movesClockWise):
            string = 'Robot 2: '

        string += str(math.ceil(self.distanceTravelled))
        text = font.render(string, 1, self.color)

        if(self.movesClockWise):
            screen.blit(text, (440, 40))
        else:
            screen.blit(text, (440, 10))

    """
    Update calculates robot's new position
    Called every frame during Main Loop
    """
    def update(self, elapsedTime):
        """Move robot towards point on edge"""
        if(not self.reachedEdge):
            self.reachedEdge = self._moveRobotToStartPointOnEdge(elapsedTime)

        """If other robot finds exit first, skip circle edge movement"""
        if(self.reachedEdge and self.travelOnCircleEdge == 0):
            self.reachedAngle = True

        """Move robot on circle edge"""
        if(self.reachedEdge and not self.reachedAngle):
            self.reachedAngle = self._moveRobotOnCircleEdge(elapsedTime);

        """Move robot to exit"""
        if(self.reachedAngle and not self.reachedExit):
            self.reachedExit = self._moveRobotToExitPoint(elapsedTime)

    """Calls _moveRobotToPoint, to move robot to startPointOnEdge"""
    def _moveRobotToStartPointOnEdge(self, elapsedTime):
        point    = self.startPointOnEdge
        distance = myMath.getDistanceBetweenTwoPoints(point, (self.x, self.y))

        return self._moveRobotToPoint(point, distance, elapsedTime)

    """Calls _moveRobotToPoint, to move robot to exit position"""
    def _moveRobotToExitPoint(self, elapsedTime):
        point    = self.exitPos
        distance = myMath.getDistanceBetweenTwoPoints(point, (self.x, self.y))

        return self._moveRobotToPoint(point, distance, elapsedTime)

    """Moves robot towards point until distance is zero"""
    def _moveRobotToPoint(self, point, distance, elapsedTime):
        """Remerber old position so we calculate distance travelled this frame"""
        oldX = self.x
        oldY = self.y

        if(distance == 0):
            """Distance is zero, stop moving"""
            return True
        elif(abs(distance) <= self.speed * elapsedTime):
            """Robot will reach point this frame, so move it there directly"""
            self.x = point[0];
            self.y = point[1];

            self.distanceTravelled += myMath.getDistanceBetweenTwoPoints((self.x, self.y), (oldX, oldY))

            return True
        else:
            """Calculate robot's new position"""
            directionX = (point[0] - self.x) / distance
            directionY = (point[1] - self.y) / distance

            self.x += directionX * self.speed * elapsedTime
            self.y += directionY * self.speed * elapsedTime

            self.distanceTravelled += myMath.getDistanceBetweenTwoPoints((self.x, self.y), (oldX, oldY))

        return False

    """Moves robot on circle edge until the angle (when exit is found) is reached"""
    def _moveRobotOnCircleEdge(self, elapsedTime):
        angleThatWillBeMoved = (self.speed / self.radius) * elapsedTime

        if(abs(self.angle - self.angleOnCircleEdge) <= angleThatWillBeMoved):
            """Robot will reach angle this frame, so move it there directly"""
            self.angle = self.angleOnCircleEdge
        elif(self.movesClockWise):
            """Move robot clockwise"""
            self.angle -= angleThatWillBeMoved
        else:
            """Move robot counter-clockwise"""
            self.angle += angleThatWillBeMoved

        """Calculate new position"""
        self.x = math.cos(self.angle) * self.radius + self.origin[0]
        self.y = -1 * math.sin(self.angle) * self.radius + self.origin[1] #negate because y goes down

        self.distanceTravelled += myMath.getArcLength(angleThatWillBeMoved, self.radius)

        return (self.angle == self.angleOnCircleEdge)
