import pygame as pg
import math
from Constants import *
from projectileClass import Projectile
pg.font.init()
pg.init()

text_font = pg.font.SysFont("Arial", 15)
suvat_font = pg.font.SysFont("Arial", 20)
input_rect = pg.Rect(1175, 20, 140, 32) # Text box used for the user to input their suvat values
value_rect = pg.Rect(1175, 60, 140, 32)

window = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT)) #Creates the window for the user to see

class displayMethods(Projectile):
    def __init__(self, window, projectile_pos, horizontal_velocity, vertical_velocity, angle):
        super().__init__(window, projectile_pos, horizontal_velocity, vertical_velocity, angle)

    def draw_projectile(self): # Draw the Projectile on screen
        pg.draw.circle(self.window, WHITE, self.projectile_pos, PROJECTILE_RADIUS)

    def update_projectile_pos(self, projectile_pos, draw_projectile=True): # Updates the position of the projectile
        self.projectile_pos = projectile_pos
        if draw_projectile: # Constantly draw the projectile in it's new position 
            self.draw_projectile()

    def draw_line(self,current_mouse_pos, ball, horizontalDisplacement, peakVerticalDisplacement, forceTriangleDisplayed):
        x1, y1, x2, y2 = [*self.projectile_pos, *current_mouse_pos]
        pg.draw.circle(self.window, RED, current_mouse_pos, radius=2)#(Surface, colour, centre, radius)
        pg.draw.line(self.window, GREEN, self.projectile_pos, current_mouse_pos)#(Surface, colour, start position, end position)
        if forceTriangleDisplayed == True:
            pg.draw.line(self.window, GREEN,(x1, y1), (x2,y1)) # Displays the Horizontal Component
            pg.draw.line(self.window, GREEN,(x2, y1), (x2,y2)) # Displays the Vertical Component
        self.display_magnitudes(text_font, RED, 20, 20, current_mouse_pos, ball, horizontalDisplacement, peakVerticalDisplacement) # Displays the horizontal, vertical and resultant values and angle
    
    def display_magnitudes(self, font, colour, x, y, current_mouse_pos, ball, horizontalDisplacement, peakVerticalDisplacement): # Blits the text onto the screen
        f = open("Main Run/Variables.txt", "r")
        contents = f.readlines()
        displayVerticalVelocity = self.getVerticalVelocity()
        displayHorizontalVelocity = self.getHorizontalVelocity()
        angle = round(self.getAngle())
        if angle > 90:
            angle = 180 - angle
        resultant_velocity = int(round(math.sqrt(abs(displayVerticalVelocity) ** 2 + abs(displayHorizontalVelocity) ** 2)))
        text1 = text_font.render(contents[0] + str(displayHorizontalVelocity) + contents[6], True, RED)
        text2 = text_font.render(contents[1] + str(displayVerticalVelocity) + contents[6], True, RED)
        text3 = text_font.render(contents[2] + str(resultant_velocity) + contents[6], True, RED)
        text4 = text_font.render(contents[3] + str(angle) + "°", True, RED)
        text5 = text_font.render(contents[4] + str(round(horizontalDisplacement/10)) + contents[7], True, RED)
        text6 = text_font.render(contents[5] + str(round(peakVerticalDisplacement/10)) + contents[7], True, RED)
        window.blit(text1,(x,y))
        window.blit(text2,(x, y + 20))
        window.blit(text3,(x, y + 40))
        window.blit(text4,(x, y + 60))
        window.blit(text5,(x, y + 80))
        window.blit(text6,(x, y + 100))
        
    def display_velocity_vector(self, projectile_pos, horizontalVector, verticalVector, peakHeightFound, ballrebounded, time_passed):
        x = projectile_pos[0]
        y = projectile_pos[1]
        verticalVector = verticalVector * 0.5
        displacementOfY = round(verticalVector * time_passed + 0.5 * -GRAVITY * pow(time_passed, 2)) 
        if displacementOfY < -175:
            displacementOfY = -175 # The vertical vector shouldn't go infinitely downwards or it will look unrealistic for the user.
        if ballrebounded == True: # The Horizontal vector should point in the opposite direction after hitting a barrier, as well as decreasing it's length to display the loss of energy
            horizontalVector *= -0.85 
        pg.draw.line(self.window, GREEN,  (x, y), (x, y - displacementOfY), width = 3)
        pg.draw.line(self.window, GREEN,  (x, y), (x + horizontalVector, y), width = 3)
        # Displays the arrow on the end of the Vector and changes it's direction based on if the peak height was reached and if there was a collision
        if peakHeightFound == False:
            pg.draw.polygon(self.window, GREEN, [(x, y - displacementOfY - 5), (x - 5, y - displacementOfY), (x + 5, y - displacementOfY)])
        else:
            pg.draw.polygon(self.window, GREEN, [(x, y - displacementOfY + 5), (x - 5, y - displacementOfY), (x + 5, y - displacementOfY)])
        if horizontalVector < 0:
            pg.draw.polygon(self.window, GREEN, [(x + horizontalVector - 5, y), (x + horizontalVector, y - 5), (x + horizontalVector, y + 5)])
        else:
            pg.draw.polygon(self.window, GREEN, [(x + horizontalVector + 5, y), (x + horizontalVector, y - 5), (x + horizontalVector, y + 5)])
            
    def display_options(self, font, colour, x, y, equations_shown, variable_type, text_surface, text_surface1, box_colour, box_colour1, velocityVectorsDisplayed, forceTriangleDisplayed):# Shows options the user can press depending on what has already happened
        if equations_shown == False: # Equations shown is true if the suvat equations are shown or if "u" is pressed
            text1 = text_font.render("Press H: Display Equation Options", True, BLUE)
            if velocityVectorsDisplayed == False:
                text4 = text_font.render("Press J: Display Velocity Vectors", True, BLUE)
                window.blit(text4,(x + 250,y))
            else:
                text4 = text_font.render("Press B: Remove Velocity Vectors", True, BLUE)
                window.blit(text4,(x + 250,y)) 
            if forceTriangleDisplayed == False:
                text5 = text_font.render("Press N: Display Force Triangle", True, BLUE)
                window.blit(text5,(x + 500,y))
            else:
                text5 = text_font.render("Press M: Remove Force Triangle", True, BLUE)
                window.blit(text5,(x + 500,y))
        else:
            text1 = text_font.render("Press Y: To Go Back", True, BLUE) 
            if variable_type == "None":
                text2 = text_font.render("Press O: To input values   Press P: To use model values, NOTE: 4 and 5 can't be used with model values", True, BLUE)# The user is able to choose which values they would like to use when working with the suvat equations
                window.blit(text2,(x + 160, y))
            elif variable_type == "Input":
                text2 = text_font.render("Input Values Used", True, BLUE)
                text3 = text_font.render("Press L: To change variable type", True, BLUE)
                window.blit(text2,(x + 160, y))
                window.blit(text3,(x + 300, y))
                text6 = text_font.render("Type the letter of the SUVAT variable in the order s-u-v-a-t:  ", True, BLUE)
                text7 = text_font.render("Type the value of the SUVAT variable or to skip type 0: ", True, BLUE)
                pg.draw.rect(window, box_colour, input_rect, 2)
                pg.draw.rect(window, box_colour1, value_rect, 2)
                window.blit(text_surface,(input_rect.x + 5, input_rect.y + 5))
                window.blit(text_surface1,(value_rect.x + 5, value_rect.y + 5))
                input_rect.w = max(100,text_surface.get_width() + 10)
                value_rect.w = max(100,text_surface1.get_width() + 10)
                window.blit(text6,(input_rect.x - 385, input_rect.y + 5))
                window.blit(text7,(value_rect.x - 360, value_rect.y + 5))
            elif variable_type == "Model":
                text2 = text_font.render("Model Values Used", True, BLUE)
                text3 = text_font.render("Press L: To change variable type", True, BLUE)
                window.blit(text2,(x + 160, y))
                window.blit(text3,(x + 300, y))
        window.blit(text1,(x,y))
    
    def display_suvat_equations(self, x, y, option_choice):
        if option_choice == 0:
            text1 = pg.image.load(r"Main Run/Display images/suvats.jpg") # loads an image onto the screen to show the user the options of suvat equations
            window.blit(text1, (x,y))
        else:
            text1 = text_font.render("Press C: To change SUVAT equation used", True, BLUE) # Allows the user to change the equation
            text2 = text_font.render("SUVAT Equation: ", True, BLUE)
            if option_choice != 0:
                text3 = pg.image.load(r"Main run/Display images/Suvat "+ str(option_choice) +".png") # Displays the equation that they chose
            window.blit(text1, (x,y)) 
            window.blit(text2, (x,y+20))
            if option_choice != 0:
                window.blit(text3, (x,y+50))

    def draw_projectile_path(self, projectile_positions): # Draws the path of the Projectile
        if projectile_positions:
            for pos in projectile_positions:
                pg.draw.circle(self.window, BLUE, pos, radius=2)



    def displayInputValue(self, variable_value): # Displays the current SUVAT values that the user has entered
        x = 1175
        y = 75
        if len(variable_value) >= 1:    
            text1 = text_font.render(f"s = {variable_value[0]}m", True, BLUE)
            window.blit(text1,(x,y+20))
        if len(variable_value) >= 2:
            text2 = text_font.render(f"u = {variable_value[1]}m/s", True, BLUE)
            window.blit(text2,(x,y+40))
        if len(variable_value) >= 3:   
            text3 = text_font.render(f"v = {variable_value[2]}m/s", True, BLUE)
            window.blit(text3,(x,y+60))
        if len(variable_value) >= 4:
            text4 = text_font.render(f"a = {variable_value[3]}m/s²", True, BLUE)
            window.blit(text4,(x,y+80))
        if len(variable_value) >= 5:
            text5 = text_font.render(f"t = {variable_value[4]}s", True, BLUE)
            window.blit(text5,(x,y+100))

    def displayWorkedSuvat(self): # Displays the SUVAT equation in the form of the option they chose and the values they entered
        if self.option_choice == 1:
            text1 = suvat_font.render(f"{self.variable_value[2]}m/s = {self.variable_value[1]}m/s + {self.variable_value[3]}m/s²  x  {self.variable_value[4]}s", True, BLUE)
            window.blit(text1,(640, 360))
        elif self.option_choice == 2:
            text1 = suvat_font.render(f"{self.variable_value[0]}m = ({self.variable_value[1]}m/s x {self.variable_value[4]}s) + (0.5 x {self.variable_value[3]}m/s² x {self.variable_value[4]}s²)", True, BLUE)
            window.blit(text1,(640, 360))
        elif self.option_choice == 3:
            text1 = suvat_font.render(f"{self.variable_value[2]}m/s = √(({self.variable_value[1]}²m/s) + (2 x {self.variable_value[3]}m/s² x {self.variable_value[0]}m))", True, BLUE)
            window.blit(text1,(640, 360))
        elif self.option_choice == 4:
            text1 = suvat_font.render(f"{self.variable_value[0]}m = ((0.5 * ({self.variable_value[2]}m/s + {self.variable_value[1]}m/s)) x {self.variable_value[4]})", True, BLUE)
            window.blit(text1,(640, 360))
        elif self.option_choice == 5:
            text1 = suvat_font.render(f"{self.variable_value[0]}m = (({self.variable_value[2]}m/s x {self.variable_value[4]}s) - (0.5 x {self.variable_value[3]}m/s² x ({self.variable_value[4]}s²)))", True, BLUE)
            window.blit(text1,(640, 360))

    def displayWorkedSuvatModelled(self, modelAnswer): # Displays the worked SUVAT equation of the previously launched projectile
        if self.option_choice == 1 and self.journeyType == "Horizontal":
            text1 = suvat_font.render(f"{modelAnswer}m/s = {self.horizontal_velocity}m/s + {ACCELERATION_MULTIPLIER}m/s²  x  {self.time_passed}s", True, BLUE)
            window.blit(text1,(640, 360))
        elif self.option_choice == 2 and self.journeyType == "Horizontal":
            text1 = suvat_font.render(f"{self.horizontalDisplacement}m = ({self.horizontal_velocity}m/s x {self.time_passed}s) + (0.5 x {ACCELERATION_MULTIPLIER}m/s² x {self.time_passed}s²)", True, BLUE)
            window.blit(text1,(640, 360))
        elif self.option_choice == 3 and self.journeyType == "Horizontal":
            text1 = suvat_font.render(f"{modelAnswer}m/s = √(({self.horizontal_velocity}²m/s) + (2 x {ACCELERATION_MULTIPLIER}m/s² x {self.horizontalDisplacement}m))", True, BLUE)
            window.blit(text1,(640, 360))
        elif self.option_choice == 1 and self.journeyType == "Vertical":
            text1 = suvat_font.render(f"{modelAnswer}m/s = {self.vertical_velocity}m/s + {ACCELERATION_MULTIPLIER}m/s²  x  {self.time_passed}s", True, BLUE)
            window.blit(text1,(640, 360))
        elif self.option_choice == 2 and self.journeyType == "Vertical":
            text1 = suvat_font.render(f"{self.peakVerticalDisplacement}m = ({self.vertical_velocity}m/s x {self.time_passed}s) + (0.5 x {ACCELERATION_MULTIPLIER}m/s² x {self.time_passed}s²)", True, BLUE)
            window.blit(text1,(640, 360))
        elif self.option_choice == 3 and self.journeyType == "Vertical":
            text1 = suvat_font.render(f"{modelAnswer}m/s = √(({self.vertical_velocity}²m/s) + (2 x {ACCELERATION_MULTIPLIER}m/s² x {self.peakVerticalDisplacement}m))", True, BLUE)
            window.blit(text1,(640, 360))
      
    def displayRestart(self): # Displays an option to cleasr the data that the user has just entered
        text = text_font.render("Press Q: To clear data entered", True, BLUE)
        window.blit(text, (550, 20))

    def requestJourneyType(self, journeyType): # Displays the option to choose between the 2 different types of journey the projectile takes
        if journeyType == "None":
            text1 = text_font.render("Press F: For the Vertical Journey", True, BLUE)
            text2 = text_font.render("Press G: For the Horizontal Journey", True, BLUE)
            window.blit(text1, (545, 20))
            window.blit(text2, (780, 20))
        else:
            text1 = text_font.render(f"{journeyType} Journey Chosen", True, BLUE)
            window.blit(text1, (545, 20))