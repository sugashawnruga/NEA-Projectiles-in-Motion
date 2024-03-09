import math
from Constants import *

class Projectile():
    def __init__(self, window, projectile_pos, horizontal_velocity, vertical_velocity, angle):
        self.window = window # Used to set up the pygame window
        self.projectile_pos = projectile_pos
        self.horizontal_velocity = horizontal_velocity
        self.vertical_velocity = vertical_velocity
        self.angle = angle
    
    def update_projectile_pos(self, projectile_pos, draw_projectile=True): # Updates the position of the projectile
        self.projectile_pos = projectile_pos

    def calculate_angle(self, current_mouse_pos): # Calculates the angle between the position of the mouse and the center of the ball 
        x1, y1, x2, y2 = [*self.projectile_pos, *current_mouse_pos]
        angle = math.atan(abs(y1 - y2) / -(x1 - x2)) *180 / math.pi
        if x1 - x2 == 0: # this is because the trigonometric function, tan does not cross 90 degrees, so tan(90) doesn't exist
            angle = 90
        return angle

    def shoot(self, time, current_mouse_pos, acceleration_time = ACCELERATION_MULTIPLIER ): # Calculate the horizontal and vertical velocity
        self.angle = self.calculate_angle(current_mouse_pos)
        if self.angle < 0 :
            self.angle = self.angle + 180
        start_time = pg.time.get_ticks()
        acceleration = time * 100
        self.horizontal_velocity = round(acceleration_time * acceleration * math.cos(math.radians(self.angle))) #Horizontal velocity, Speed = Acceleration x Time Spent Accelerating x Cosine
        self.vertical_velocity = round(abs(acceleration_time * acceleration * math.sin(math.radians(self.angle)))) #Vertical velocity, Speed = Acceleration x Time Spent Accelerating x Sine

        return start_time, self.horizontal_velocity, self.vertical_velocity
    
    def getHorizontalVelocity(self): # Returns the Horizontal Velocity
        return self.horizontal_velocity

    def getVerticalVelocity(self): # Returns the Vertical Velocity
        return self.vertical_velocity

    def getAngle(self): # Returns the Angle
        return self.angle