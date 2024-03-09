import sys
import pygame as pg
from Constants import *
from projectileClass import Projectile
from displayMethodsClass import displayMethods
from suvatClass import suvat_model
from suvatClass import suvat_input

pg.font.init()
pg.init()
clock = pg.time.Clock()

text_font = pg.font.SysFont("Arial", 15)
input_rect = pg.Rect(1175, 20, 140, 32) # Text box used for the user to input their suvat values
value_rect = pg.Rect(1175, 80, 140, 32)

window = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT)) #Creates the window for the user to see
pg.display.set_caption("Project: Projectiles in Motion") #Titles the window
window.fill(BLACK) #Makes the background BLACK

def main():
    projectile_pos = INITIAL_PROJECTILE_POSITION
    ball = Projectile(window, projectile_pos, 0, 0, 0)
    ballDisplay = displayMethods(window, projectile_pos, 0, 0, 0)

    equations_shown = False
    velocityVectorsDisplayed = False
    forceTriangleDisplayed = False
    option_choice = 0 # Indicates which suvat equation they can to use 
    variable_type = ("None") # Indicates if the user wants to use the model variables or input their own
    suvat_variable = [] # s = displacement   u = initial velocity  v = final velocity a = acceleration t = time
    variable_value = [] # value of the SUVAT variables
    user_entry = ("") # Stores the SUVAT variable the user will use
    user_entry1 = ("") # Stores the value of the actual Variable Value
    box_active = False # Used to show if the text box has been clicked
    box_colour = GREY  # Used to change the colour of the text box to show the user if it's active or not
    box_active1 = False
    box_colour1 = GREY
    allVariableValuesFilled = False
    journeyType = ("None")

    horizontalDisplacement = 0
    peakVerticalDisplacement = 0
    ReboundX = 0
    ball_rebounded = False
    peakHeightFound = False
    displaceOfY = 0

    projectile_path_list = [] # List of the positions of the projectile
    mouse_pos = None
    shoot = False
    mouse_pos = pg.mouse.get_pos()

    def exit():
        pg.display.quit()
        pg.quit()
        sys.exit()  

    while True:
        window.fill(BLACK)
        text_surface = text_font.render(user_entry, True, (GREEN))
        text_surface1 = text_font.render(user_entry1, True, (GREEN))
        if equations_shown == False:
            ballDisplay.display_options(text_font, BLUE, 220, 20, equations_shown, variable_type, text_surface, text_surface1, box_colour, box_colour1, velocityVectorsDisplayed, forceTriangleDisplayed)
        else:
            ballDisplay.display_options(text_font, BLUE, 20, 20, equations_shown, variable_type, text_surface, text_surface1, box_colour, box_colour1, velocityVectorsDisplayed, forceTriangleDisplayed)

        if shoot: # Calculates the change in the X and Y coordinates when the ball is shot
            time_passed = (pg.time.get_ticks() - start_time) / 1000 * TIME_MULTIPLIER
            if projectile_pos[1] <= INITIAL_PROJECTILE_POSITION[1]:
                x, y = start_projectile_pos
                
                if ball_rebounded == False:
                    change_y = round(vertical_velocity * time_passed - 0.5 * GRAVITY * pow(time_passed, 2))
                    change_x = round(horizontal_velocity * time_passed) # change_x is only updated this way when there is no collision with the wall
                
                if projectile_pos[0] >= 1280 or projectile_pos[0] <= 0: # ball_rebounded turns true if the projectile hits the walls
                    ball_rebounded = True
                
                if ball_rebounded == True:
                    change_y = round(vertical_velocity * time_passed - 0.5 * GRAVITY * pow(time_passed, 2))
                    ReboundX = change_x # Once there is a collision, the ReboundX takes the change in x-axis as it hits the barrier
                    ReboundX = ReboundX * 0.989 # The ReboundX is decremented to simulate the lose of energy as the ball hits the barrier
                    change_x = ReboundX
                
                
                projectile_pos = (x + change_x, y - change_y) #Projectiles position is updated based on the position it was first launched (point where mouse button up occurs)

                projectile_path_list.append(projectile_pos)
                if projectile_pos[1] > 705 and projectile_pos[1] < 720 :
                    ball_rebounded = False
                    ReboundX = 0 
                
                if peakHeightFound == False and change_y < displaceOfY:
                    peakVerticalDisplacement = change_y
                    peakHeightFound = True
                displaceOfY = change_y

                if velocityVectorsDisplayed == True:
                    ballDisplay.display_velocity_vector(projectile_pos, horizontal_velocity, vertical_velocity, peakHeightFound, ball_rebounded, time_passed)
                
                #print("Change in Y: ", change_y)
                #print("Change in X: ", change_x)

            else: # When the ball lands, shoot is reset, the projectile is set to ground level and the horizontal displacement is stored, and the peakHeightFound is reset
                shoot = False
                projectile_pos = (projectile_pos[0], INITIAL_PROJECTILE_POSITION[1])
                horizontalDisplacement = change_x
                peakHeightFound = False
                
        for event in pg.event.get(): # event loop to track the events that happen in pygame
            if event.type == pg.QUIT:
                exit()
            elif event.type == pg.KEYDOWN: 
                if event.key == pg.K_r: # Resets the position of the Projectile
                    shoot = False
                    projectile_pos = INITIAL_PROJECTILE_POSITION
    
                if event.key == pg.K_h: # Stops the Projectile Simulation for the user to be able to Enter Data or use the data of the projectile just shot in SUVAT equations
                    equations_shown = True
                elif event.key == pg.K_j: # Activates the display of velocity vectors
                    velocityVectorsDisplayed = True
                elif event.key == pg.K_n: # Activates the display of the force triangle
                    forceTriangleDisplayed = True
                elif event.key == pg.K_y: # Lets the user go back to the projectile simulation
                    equations_shown = False
                elif event.key == pg.K_b: # Deactivates the display of velocity vectors
                    velocityVectorsDisplayed = False
                elif event.key == pg.K_m: # Deactivates the display of the force triangle
                    forceTriangleDisplayed = False
                elif event.key == pg.K_o and variable_type == "None": # Lets the user choose what type of values are going to be used in the SUVAT equations
                    variable_type = ("Input")
                elif event.key == pg.K_p and variable_type == "None":
                    variable_type = ("Model")
                elif event.key == pg.K_l: # Lets the user be able to change their choice
                    variable_type = ("None")
                elif event.key == pg.K_c:
                    option_choice = 0
                elif event.key == pg.K_f and variable_type == "Model": # User is able to choose whether the vertical or horizontal journey is worked out
                    journeyType = "Vertical"
                elif event.key == pg.K_g and variable_type == "Model":
                    journeyType = "Horizontal"
                elif equations_shown == True and option_choice == 0: # User chooses which SUVAT equation is used
                    if event.key == pg.K_1:
                        option_choice = 1
                    elif event.key == pg.K_2:
                        option_choice = 2
                    elif event.key == pg.K_3:
                        option_choice = 3
                    elif event.key == pg.K_4:
                        option_choice = 4
                    elif event.key == pg.K_5:
                        option_choice = 5
                elif event.key == pg.K_q and variable_type == "Input": # Clears the data that was previously entered
                    suvat_variable = []
                    variable_value = []
                elif event.key == pg.K_RETURN: # The user enters their values of the SUVAT variables.
                    if box_active == True:
                        suvat_variable.append(user_entry)
                        user_entry = ("")
                        box_active = False
                        box_colour = GREY
                    elif box_active1 == True:
                        variable_value.append(user_entry1)
                        user_entry1 = ("")
                        box_active1 = False
                        box_colour1 = GREY
                        if len(variable_value) == 5: # Checks if all the SUVAT variables and values have been entered.
                            inputAnswer = suvat_input(option_choice, suvat_variable, variable_value)
                            allVariableValuesFilled = True
                elif box_active == True:
                    if event.key == pg.K_BACKSPACE: # deletes previously entered unicode
                        user_entry = user_entry[:-1]
                    else:
                        user_entry += event.unicode # add the typed unicode to the variable user entry
                elif box_active1 == True:
                    if event.key == pg.K_BACKSPACE:
                        user_entry1 = user_entry1[:-1]
                    else:
                        user_entry1 += event.unicode

            elif event.type == pg.MOUSEMOTION:
                mouse_pos = event.pos # Gets position of the mouse
            elif event.type == pg.MOUSEBUTTONDOWN:
                start_count_time = pg.time.get_ticks()
                if input_rect.collidepoint(event.pos): # Used to ensure the user is only able to type in the text box if it's clicked on
                    box_active = True
                    box_colour = AQUA_BLUE
                else:
                    box_active = False
                    box_colour = GREY
                if value_rect.collidepoint(event.pos): # Used to ensure the user is only able to type in the text box if it's clicked on
                    box_active1 = True
                    box_colour1 = AQUA_BLUE
                else:
                    box_active1 = False
                    box_colour1 = GREY
            elif event.type == pg.MOUSEBUTTONUP and equations_shown == False: 
                end_time = (pg.time.get_ticks() - start_count_time) / 1000 # Find the time of how long the user held their mouse button down
                start_time, horizontal_velocity, vertical_velocity = ball.shoot(end_time, mouse_pos) # works out the values for the projectile to be launched
                start_time, horizontal_velocity, vertical_velocity = ballDisplay.shoot(end_time, mouse_pos) # These values worked out are for the display only
                start_projectile_pos = projectile_pos 
                projectile_path_list = []
                shoot = True
        
        ball.update_projectile_pos(projectile_pos)
        ballDisplay.update_projectile_pos(projectile_pos)
        if equations_shown == False: # draws the balls path if the user hasn't chosen to use the suvat equations
            if mouse_pos is not None:
                ballDisplay.draw_line(mouse_pos, ball, horizontalDisplacement, peakVerticalDisplacement, forceTriangleDisplayed)
            ballDisplay.draw_projectile_path(projectile_path_list)

        if equations_shown == True and option_choice == 0:
            ballDisplay.display_suvat_equations(20, 60, option_choice)

        elif option_choice != 0 and equations_shown == True:
            ballDisplay.display_suvat_equations(20, 60, option_choice)
        
        if option_choice != 0 and variable_type == "Input" and equations_shown == True:
            ballDisplay.displayInputValue(variable_value)
            ballDisplay.displayRestart()
            if allVariableValuesFilled == True:
                inputAnswer.displayWorkedSuvat()
        
        if variable_type == "Model" and equations_shown == True:
            ballDisplay.requestJourneyType(journeyType)

        if allVariableValuesFilled == True:
            if option_choice == 1:
                inputAnswer.one()
            elif option_choice == 2:
                inputAnswer.two()
            elif option_choice == 3:
                inputAnswer.three()
            elif option_choice == 4:
                inputAnswer.four()
            elif option_choice == 5:
                inputAnswer.five()

        if journeyType != "None" and equations_shown == True and option_choice != 0 and variable_type == "Model":
            modelValues = suvat_model(horizontal_velocity, vertical_velocity, horizontalDisplacement, peakVerticalDisplacement, time_passed, journeyType, option_choice)
            if option_choice == 1:
                modelAnswer = modelValues.one()
            elif option_choice == 2:
                modelAnswer = modelValues.two()
            elif option_choice == 3:
                modelAnswer = modelValues.three()
            modelValues.displayWorkedSuvatModelled(modelAnswer)
            

        pg.display.flip()
        clock.tick(REFRESH_RATE)

pg.init()
main()