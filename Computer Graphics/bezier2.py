import pygame
from pygame.locals import *

gray = (100,100,100)
lightgray = (200,200,200)
red = (255,0,0)
blue = (0,0,255)

p = [] #empty points array
#gets 4 control points from user input
def get_points():
    #loops through 4 times to get 4 control points
    for i in range(4):
        while True:
            #user input
            p_input = input("Enter X,Y Coordinates for p" + str(i) + ":")
            #splits the string into x and y coordinates
            p_components = p_input.split(',')
            #checks to see if user hasnt entered two coordinates
            if len(p_components) != 2:
                print("Missing coordinate please try again.")
                p_input = input("Enter X,Y Coordinates for p" + str(i) + ":")
                p_components = p_input.split(',')
            #checks to see if the values can not be converted into floats
            try:
                x = float(p_components[0])
                y = float(p_components[1])
            except ValueError:
                print("Invalid coordinates", p_components, "please try again.")
            #appends the x and y coordinates as a 2 dimensional array
            else:
                p.append([float(p_components[0]), float(p_components[1])])
                break
#gets parameter 't' interval from user input
def get_interval():
    while True: 
        try:
            i = int(input("Please enter an interval for the parameter t:"))
        except ValueError:
            print("Invalid interval, please try again")
        else:
            i = abs(i)
            break
    return i
#calculates required coordinates for plotting bezier curve.
def bezier():
    result = [] #empty result array, which will store values x and y values from the bezier curve equation
    get_points() #gets the 4 control points
    i = get_interval() #gets the parameter 't' interval 
    for x in range(i+1): #i+1 so that it includes the last value
        t = x/i #x/i due to python not being able to have a step value of a float, so this is a work around
        x=(p[0][0]*(1-t)**3+p[1][0]*3*t*(1-t)**2+p[2][0]*3*t**2*(1-t)+p[3][0]*t**3) #calculates x coordinate
        y=(p[0][1]*(1-t)**3+p[1][1]*3*t*(1-t)**2+p[2][1]*3*t**2*(1-t)+p[3][1]*t**3) #calculates y coordinate
        result.append((int(x), int(y))) #appends coordinates to result array.
    return result

def main():
    pygame.init()

    points = bezier()
    screen = pygame.display.set_mode((1024, 768))
    clock = pygame.time.Clock()

    done = False
    while not done:
        for event in pygame.event.get():
            # Close the window by pressing the x button.
            if event.type == pygame.QUIT:
                done = True

        #draws the control points
        for i in p:
            pygame.draw.circle(screen, blue, (int(i[0]), int(i[1])), 4)
        #draws the lines between control points
        pygame.draw.lines(screen, lightgray, False, p)
        #draws the bezier curve
        pygame.draw.lines(screen, pygame.Color("red"), False, points, 2)
        pygame.display.flip()
        clock.tick(100)


if __name__ == "__main__":
    main()