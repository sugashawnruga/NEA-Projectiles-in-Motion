import math
from Constants import *
from displayMethodsClass import displayMethods

# The methods of these classes, 1-5 correlate to the suvat equation that is used, so which ever one the user picks is the method that is used.
class suvat_input(displayMethods):
    def __init__(self, option_choice, suvat_variable, variable_value):
        self.option_choice = option_choice
        self.suvat_variable = suvat_variable
        self.variable_value = variable_value
    
    def one(self):
        self.variable_value[2] = round(float(self.variable_value[1]) + (float(self.variable_value[3]) * float(self.variable_value[4])))
        return self.variable_value[2]

    def two(self):
        self.variable_value[0] = (float(self.variable_value[1]) * float(self.variable_value[4])) + (0.5 * float(self.variable_value[3]) * (float(self.variable_value[4])**2))
        return self.variable_value[0]

    def three(self):
        self.variable_value[2] = math.sqrt((float(self.variable_value[1])**2) + (2 * float(self.variable_value[3]) * float(self.variable_value[0])))
        return self.variable_value[2]
    
    def four(self):
        self.variable_value[0] = ((0.5 * (float(self.variable_value[2]) + float(self.variable_value[1]))) * float(self.variable_value[4]))
        return self.variable_value[0]
    
    def five(self):
        self.variable_value[0] = ((float(self.variable_value[2]) * float(self.variable_value[4])) - (0.5 * float(self.variable_value[3]) * (float(self.variable_value[4])**2)))
        return self.variable_value[0]

class suvat_model(suvat_input):
    def __init__(self, horizontal_velocity, vertical_velocity, horizontalDisplacement, peakVerticalDisplacement, time_passed, journeyType, option_choice):
        self.horizontal_velocity = horizontal_velocity
        self.vertical_velocity = vertical_velocity
        self.horizontalDisplacement = horizontalDisplacement
        self.peakVerticalDisplacement = peakVerticalDisplacement
        self.time_passed = time_passed
        self.journeyType = journeyType
        self.option_choice = option_choice
        # All attributes are the variables taken from the previously launched projectile
    
    def one(self): # Depending on the user's input methods will use different equations and values, based on if the user want to use the vertical or horizontal journey
        if self.journeyType == "Horizontal": 
            finalVelocity = round(float(self.horizontal_velocity) + (float(ACCELERATION_MULTIPLIER) * float(self.time_passed)))
            return finalVelocity
        elif self.journeyType == "Vertical":
            finalVelocity = round(float(self.vertical_velocity) + (float(ACCELERATION_MULTIPLIER) * float(self.time_passed)))
            return finalVelocity

    def two(self):
        if self.journeyType == "Horizontal":
            self.horizontalDisplacement = (float(self.horizontal_velocity) * float(self.time_passed)) + (0.5 * float(ACCELERATION_MULTIPLIER) * (float(self.time_passed)**2))
            return self.horizontalDisplacement
        elif self.journeyType == "Vertical":
            self.peakVerticalDisplacement = (float(self.vertical_velocity) * (float(self.time_passed) * 0.5)) + (0.5 * float(ACCELERATION_MULTIPLIER) * ((float(self.time_passed) * 0.5)**2))
            return self.peakVerticalDisplacement
        
    def three(self):
        if self.journeyType == "Horizontal":
            finalVelocity = math.sqrt((float(self.horizontal_velocity[1])**2) + (2 * float(ACCELERATION_MULTIPLIER) * float(self.horizontalDisplacement)))
            return finalVelocity
        elif self.journeyType == "Vertical":
            finalVelocity = math.sqrt((float(self.vertical_velocity[1])**2) + (2 * float(ACCELERATION_MULTIPLIER) * float(self.peakVerticalDisplacement)))
            return finalVelocity