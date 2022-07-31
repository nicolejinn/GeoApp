#-----------------------------------------------------------------------------
# Name:        GeoApp
# Purpose:     This project is a tool to assist the users that accepts input of
#              parameters of different two dimensional geometric shapes in Mathematics
#              and display and visualize these geometric shapes on the screen. The
#              program would be able to calculate the area and the perimeter of the
#              shape. The user can also customize the display and choose if they
#              want the shape to be generated on a coordinate system.
#
# Author:      Nicole J
# Created:     18-Mar-2021
# Updated:     2-Apr-2021
#-----------------------------------------------------------------------------

# microbit code:
# https://python.microbit.org/v/2
    

import pygame as pg
import math
from decimal import Decimal
from Microbit import *


class RegShape:
    """
    A class used to represent a regular shape 
    
    """
    def __init__(self):
        '''
        This function initializes the regular shape's number of sides, its side length, its start point and its scale

        Parameters
        ----------
        None

        Returns
        -------
        None
        '''
        self.numOfSide = None 
        self.side = None # side length 
        self.startPos = (250, 275)
        self.scale = 1
        
    def draw(self, surfaceIn):
        '''
        This function draws the regular shape onto the screen

        Parameters
        ----------
        surfaceIn: Surface
            the surface/screen where the regular shape is displaying to

        Returns
        -------
        None
        '''
        if self.numOfSide != None and self.side != None:
            prevPos = self.startPos
            angle = math.pi*2/self.numOfSide
            for i in range(self.numOfSide):
                nxtPos = (prevPos[0] + self.side*10*math.sin(angle*i)/self.scale, prevPos[1] + self.side*10*math.cos(angle*i)/self.scale)
                pg.draw.line(surfaceIn, (0, 0, 0), prevPos, nxtPos, 2)
                prevPos = nxtPos
            
    def getPerimeter(self):
        '''
        This function calculates the perimeter of the regular shape

        Parameters
        ----------
        None

        Returns
        -------
        roundedPer: float
            the perimeter of the regular shape that is rounded to second decimal place
        '''
        if self.numOfSide != None and self.side != None:
            roundedPer = round((self.numOfSide * self.side), 2)
            return roundedPer
    
    def getArea(self):
        '''
        This function calculates the area of the regular shape

        Parameters
        ----------
        None

        Returns
        -------
        roundedArea: float
            the area of the regular shape that is rounded to second decimal place
        '''
        if self.numOfSide != None and self.side != None:
            angle = math.pi*2/self.numOfSide
            roundedArea = round((((self.side)**2)*self.numOfSide)/(4*math.tan(angle/2)), 2)
            return roundedArea
       
        
class IrregShape:
    """
    A class used to represent an irregular / customized shape
    
    """
    def __init__(self):
        '''
        This function initializes the irregular / customized shape's number of sides, its side length input, its angle input,
        its start point, its points positions and its scale. It also initializes the state of drawing (start drawing / start
        inputting / finish drawing).

        Parameters
        ----------
        None

        Returns
        -------
        None
        '''
        self.numOfSide = None
        self.side = None
        self.angle = None
        
        self.startIrregInput = False # start inputting
        self.finishDrawing = False # finish drawing
        
        self.sideChanged = False # detect if a new side is inputted
        self.angleChanged = False # detect if a new angle is inputted
        self.localSideChanged = False # store the sideChanged value locally
        self.localAngleChanged = False # store the angleChanged value locally
        
        self.oldShape = False # if this object is previously stored in the data
        
        self.startPos = [250, 275]
        self.points = [self.startPos]
        self.scale = 1
                
    def draw(self, surfaceIn, scale):
        '''
        This function draws the irregular / customized shapes onto the screen

        Parameters
        ----------
        surfaceIn: Surface
            the surface/screen where the regular shape is displaying to
        scale: float
            the new scale of the shape (zoomed in or zoomed out)

        Returns
        -------
        None
        '''
        if self.startIrregInput and not self.oldShape: # if the shape is new and start inputting
            if self.scale != scale: # if the shape needs to be rescaled
                # temporary points, used for recalculating the coordinate of next point when new scale is inputted
                temPoints = [self.startPos]
                for i in range(1, len(self.points)-1):
                    temPoints.append([(self.points[i][0]-self.startPos[0])/scale*self.scale+self.startPos[0], (self.points[i][1] - self.startPos[1])/scale*self.scale+self.startPos[1]])
                    # calculate the shortened distance between certain point / vertex to the starting point to rescale the shape
                    self.points[i] = temPoints[i] # replace original points with newly calculated rescaled points
                self.scale = scale
            if len(self.points) == 1 and self.sideChanged: # first point only requires side length input
                nxtPos = [self.points[-1][0] + self.side*10/self.scale, self.points[-1][1]]
                self.points.append(nxtPos)
            elif 1 < len(self.points) < self.numOfSide and self.changedIn(): # rest of the points require both side length and angle input
                # reset the local values to false
                self.localSideChanged = False
                self.localAngleChanged = False
                # calculate next point
                nxtPos = [self.points[-1][0] + self.side*10*math.cos(math.radians(360-self.angle))/self.scale, self.points[-1][1] + self.side*10*math.sin(math.radians(360-self.angle))/self.scale]
                self.points.append(nxtPos)
            elif len(self.points) == self.numOfSide: # automatically connect the last point and starting point as the last side drawn
                nxtPos = self.startPos
                self.points.append(nxtPos)
                self.finishDrawing = True
            for i in range(len(self.points)-1): # draw lines from the points list onto the screen
                pg.draw.line(surfaceIn, (0, 0, 0), self.points[i], self.points[i+1], 2)
            # reset sideChanged and angleChanged after the boolean is stored into local variables
            self.sideChanged = False
            self.angleChanged = False
        elif self.oldShape: # if the shape is previously stored
            if self.scale != scale: # enable zoomed in and out feature
                for i in range(1, len(self.points)-1):
                    self.points[i] = [(self.points[i][0]-self.startPos[0])/scale*self.scale+self.startPos[0], (self.points[i][1] - self.startPos[1])/scale*self.scale+self.startPos[1]]
                self.scale = scale
            for i in range(len(self.points)-1): # draw lines from the points list onto the screen
                pg.draw.line(surfaceIn, (0, 0, 0), self.points[i], self.points[i+1], 2)
            
    def changedIn(self):
        '''
        This function stores the booleans of whether the side and angle changed locally

        Parameters
        ----------
        None

        Returns
        -------
        bothChanged: Boolean
            whether both side length and angle are inputted by the user
        '''
        if self.sideChanged:
            self.localSideChanged = True
        if self.angleChanged:
            self.localAngleChanged = True
        bothChanged = self.localSideChanged and self.localAngleChanged
        return bothChanged
     
    def getPerimeter(self):
        '''
        This function calculates the perimeter of the drawn shape

        Parameters
        ----------
        None

        Returns
        -------
        roundedPer: float
            the perimeter of the drawn shape that is rounded to second decimal place
        '''
        perimeter = 0
        for i in range(len(self.points)-1):
            # calculate the distance between two adjacent vertexes / points
            perimeter += (((self.points[i+1][0]/10-self.points[i][0]/10)*self.scale)**2 + ((self.points[i+1][1]/10 - self.points[i][1]/10)*self.scale)**2)**0.5
        roundedPer = round(perimeter, 2)
        return roundedPer
    
    def getArea(self):
        '''
        This function calculates the area of the drawn shape

        Parameters
        ----------
        None

        Returns
        -------
        roundedArea: float
            the area of the drawn shape that is rounded to second decimal place
        '''
        # shoelace theorem (only works if inputs are in a clockwise direction!)
        # more information and specific formula on: https://artofproblemsolving.com/wiki/index.php/Shoelace_Theorem
        sum1 = 0
        sum2 = 0
        for i in range(len(self.points)-1):
            sum1 += self.points[i][0]*self.points[i+1][1]/100*(self.scale**2)
            sum2 += self.points[i][1]*self.points[i+1][0]/100*(self.scale**2)
        area = abs(sum1 - sum2)/2
        roundedArea = round(area, 2)
        return roundedArea


class HandDraw:
    """
    A class used to represent hand drawing shapes (with mouse or microbit)
    
    """
    def __init__(self):
        '''
        This function initializes the mouse position, microbit position and its initial speed,
        the temporary surface to display to, and the detection of whether the drawing is started for the hand drawing option

        Parameters
        ----------
        None

        Returns
        -------
        None
        '''
        self.mousePrevPos = None # default mouse position to None
        
        self.microPrevPos = (250, 275) # default microbit position to origin (on the customized coordinate plane)
        self.speed = [0, 0] # default speed to 0 for both x and y componenets
        
        self.drawing = False
        
        # create a temporary surface to display the drawing to first, for later blitting the surface onto the main screen
        self.temSurface = pg.Surface((700, 550))
        self.temSurface.fill((255, 255, 255))
    
    def move(self, xIn, yIn):
        '''
        This function receives the new velocity of the drawinf line
        and passes the velocity to get the new end point position of the line

        Parameters
        ----------
        xIn: float
            the x component of the velocity of the microbit
        yIn: float
            the y component of the velocity of the microbit

        Returns
        -------
        newPos: tuple
            a tuple of new coordinate that the microbit moves to
        '''
        newPos = (self.microPrevPos[0] + xIn, self.microPrevPos[1] + yIn)
        return newPos
        
    def accelerate(self, xIn, yIn):
        '''
        This function detects the movement of the microbit and passes the acceleration to get the
        new velocity for the new drawing speed of the line

        Parameters
        ----------
        xIn: float
            the x component of the acceleration of the microbit
        yIn: float
            the y component of the acceleration of the microbit

        Returns
        -------
        None
        '''
        self.speed[0] += xIn
        self.speed[1] += yIn
        
    def update(self):
        '''
        This function updates the position of the end point of the line on screen by checking
        the microbit's acceleration and updating the line's drawing speed and the its position

        Parameters
        ----------
        None

        Returns
        -------
        newPos: tuple
            a tuple of new coordinate that the microbit moves to
        '''
        newPos = self.move(self.speed[0], self.speed[1])
        return newPos
    
    def microDraw(self, xIn, yIn):
        '''
        This function draws the line traced by microbit

        Parameters
        ----------
        xIn: float
            the x component of the acceleration of the microbit (tilting from left to right)
        yIn:float
            the y component of the acceleration of the microbit (from forwards to backwards)

        Returns
        -------
        None
        '''
        if self.drawing: # when the microbit is connected
            # reduce the sensitivity of the velocity of the drawing line to the tilting of the microbit
            self.accelerate(-int(xIn)/1200,0) 
            self.accelerate(0,-int(yIn)/1200)
            # get new position of the microbit
            newPos = self.update()
            # draw line to the temporary surface
            pg.draw.line(self.temSurface, (0, 0, 0), self.microPrevPos, newPos, 2)
            self.microPrevPos = newPos
            
    def moDraw(self):
        '''
        This function draws the line traced by the mouse

        Parameters
        ----------
        None

        Returns
        -------
        None
        '''
        if self.drawing: # if the mouse button is pressed
            pos = pg.mouse.get_pos() # get mouse position
            if self.mousePrevPos != None:
                # draw line based on old and new mouse position to the temporary surface
                pg.draw.line(self.temSurface, (0, 0, 0), self.mousePrevPos, pos, 2)
            self.mousePrevPos = pos
            
    def display(self, surfaceIn):
        '''
        This function displays the temporary surface onto the main screen

        Parameters
        ----------
        surfaceIn: Surface
            the surface/screen where the regular shape is displaying to

        Returns
        -------
        None
        '''
        surfaceIn.blit(self.temSurface, (0, 0))
            
    def lineCut(self):
        '''
        This function cuts the line when the mouse button is released and
        reset the speed when the microbit drawing is restarted

        Parameters
        ----------
        None

        Returns
        -------
        None
        '''
        self.mousePrevPos = None
        self.microPrevPos = (250, 275)
        self.speed = [0, 0]
        
    def reset(self):
        '''
        This function resets the temporary surface and clears the past drawing

        Parameters
        ----------
        None

        Returns
        -------
        None
        '''
        self.temSurface.fill((255, 255, 255))
        self.lineCut()
    
    
class CoordinatePlane:
    """
    A class used to represent the coordinate plane
    
    """
    def __init__(self, SMALLFONTIn):
        '''
        This function initializes the origin of the coordinate plane,
        the font to display the numbers on the axes, the axes and its scale

        Parameters
        ----------
        SMALLFONTIn: Object
            the small font that the numbers on the axes display in

        Returns
        -------
        None
        '''
        self.origin = (250, 275)
        # the line of axes from its start point to its end point
        self.yAxis = (250, 550), (250, 0)
        self.xAxis = (0, 275), (700, 275)
        
        self.FONT = SMALLFONTIn
        
        self.scale = 1
        
    def draw(self, surfaceIn):
        '''
        This function draws the coordinate plane onto a
        temporary surface in a customized scale and then display the surface to the main screen

        Parameters
        ----------
        surfaceIn: Surface
            the small font that the numbers on the axes display in

        Returns
        -------
        None
        '''
        # create temporary surface and set it to transparent
        temSurface = pg.Surface((700, 550))
        temSurface.set_colorkey((0, 0, 0))
        # set the min and max of the zoom in and out feature
        if self.scale < 2**-3:
            self.scale = 2**-3
        elif self.scale > 2**9:
            self.scale = 2**9
        # display numbers labeled on the x-axis
        for i in range(700):
            # if scale is large enough, the number displayed are integers
            if self.scale > 2:
                if i % 100 == 0: # fixed distance between two numbers, prevent the gap to become too wide
                    txt = str(int((i//10-25)*self.scale))
                    temSurface.blit(self.FONT.render(txt, True, (100, 100, 100)), (i, 280))
                    pg.draw.line(temSurface, (200, 200, 200), (i, 0), (i, 550))
            else: # if scale is smaller, the number displayed are floats
                if i%(50*self.scale) == 0:
                    if self.scale == 2 or self.scale == 1:
                        txt = str(int((i//10-25)*self.scale))
                    else:
                        txt = str(round((i//10-25)*self.scale, 2))
                    temSurface.blit(self.FONT.render(txt, True, (100, 100, 100)), (i, 280))
                    pg.draw.line(temSurface, (200, 200, 200), (i, 0), (i, 550))
        # display numbers labeled on the y-axis
        for i in range(550):
            # if scale is large enough, the number displayed are integers. Prevent overlapping numbers from both axes at the origin.
            if self.scale > 2 and (i < 270 or i > 280):
                if i % 100 == 0: # fixed distance between two numbers, prevent the gap to become too wide
                    txt = str(int((28 - i//10)*self.scale))
                    temSurface.blit(self.FONT.render(txt, True, (100, 100, 100)), (255, i))
                    pg.draw.line(temSurface, (200, 200, 200), (0, i), (700, i))
            else: # if scale is smaller, the number displayed are floats. Prevent overlapping numbers.
                if i%(50*self.scale) == 0 and (i < 270 or i > 280):
                    if self.scale == 2 or self.scale ==1:
                        txt = str(int((28 - i//10)*self.scale))
                    else:
                        txt = str(round((28 - i//10)*self.scale, 2))
                    temSurface.blit(self.FONT.render(txt, True, (100, 100, 100)), (255, i))
                    pg.draw.line(temSurface, (200, 200, 200), (0, i), (700, i))
        # draw axes
        pg.draw.line(temSurface, (100, 100, 100), (250, 550), (250, 0))
        pg.draw.line(temSurface, (100, 100, 100), (0, 275), (700, 275))
        surfaceIn.blit(temSurface, (0, 0)) # blit the temporary surface onto the main screen
    
    
class Button:
    """
    A class used to represent a button
    
    """
    def __init__(self, rectIn, text, FONT):
        '''
        This function initializes the size, the position, the text and ths font it uses on a button

        Parameters
        ----------
        rectIn: tuple
            the size and position of the button
        text: String
            the text on the button to show the functionality of the button
        FONT: Object
            the font that the text on the button is displayed in

        Returns
        -------
        None
        '''
        self.rect = rectIn
        
        self.txt = text
        self.txtSurf = FONT.render(text, True, (255, 255, 255))
        
        self.color = (116, 116, 117)
        
        self.buttonActive = False # detect if the button is pressed
        
    def draw(self, surfaceIn):
        '''
        This function draws the button onto the screen

        Parameters
        ----------
        surfaceIn: Surface
            the small font that the numbers on the axes display in

        Returns
        -------
        None
        '''
        if self.buttonActive: # if button is pressed, change the button to a darker color
            self.color = (75, 75, 75)
        elif not self.buttonActive:
            self.color = (116, 116, 117)
        pg.draw.rect(surfaceIn, self.color, self.rect, border_radius = 15) # draw the button onto the screen
        
        # set the position of the text in regards to the position of the button and display it on screen
        txtRect = self.txtSurf.get_rect(center=((2*self.rect[0]+self.rect[2])/2 , (2*self.rect[1]+self.rect[3])/2))
        surfaceIn.blit(self.txtSurf, txtRect)
        
    def mouseCollide(self):
        '''
        This function detects if the mouse is on the button

        Parameters
        ----------
        None

        Returns
        -------
        Boolean
            whether the mouse is on the button
        '''
        mousePos = pg.mouse.get_pos()
        if (mousePos[0] > self.rect[0] and mousePos[0] < self.rect[0] + self.rect[2] and mousePos[1] > self.rect[1] and mousePos[1] < self.rect[1] + self.rect[3]): 
            # this function is only called when mouse is pressed, so when mouse is on the button, also set buttonActive to True
            self.buttonActive = True
            return True
        else:
            self.buttonActive = False
            return False 
        
    
class UserInput:
    """
    A class used to represent a user input box
    
    """
    def __init__(self, rectIn, FONT, titleIn):
        '''
        This function initializes the position, the font, and the title of user input box

        Parameters
        ----------
        rectIn: tuple
            the size and the position of the user input box
        FONT: Object
            the font that the title is displayed in
        titleIn: String
            the title of the input box, to show the functionality of the input box

        Returns
        -------
        None
        '''
        self.color = (200, 200, 200) # inactive color, active color: (0, 0, 0)
        
        self.rect = pg.Rect(rectIn) # store the input as a rectangle
        
        self.title = titleIn
        self.titleSurf = FONT.render(titleIn, True, (100, 100, 100))
        
        # set the default text inside the input box
        self.txt = ""
        self.txtSurf = FONT.render(self.txt, True, self.color)
        
        self.active = False # if the input box is being inputted
        
    def mouseCollide(self):
        '''
        This function detects if the mouse is on the input box

        Parameters
        ----------
        None

        Returns
        -------
        Boolean
            if the mouse is on the input box
        '''   
        mousePos = pg.mouse.get_pos()
        if (self.rect.x <= mousePos[0] <= (self.rect.x + self.rect.w)) and (self.rect.y <= mousePos[1] <= (self.rect.y + self.rect.h)):
            self.active = not self.active # the function is only called after the mouse is pressed
            return True
        else:
            self.active = False
            return False
        
    def update(self):
        '''
        This function updates the input box if the text input is too long

        Parameters
        ----------
        None

        Returns
        -------
        None
        '''
        width = max(50, self.txtSurf.get_width()+10) 
        self.rect.w = width
        
    def draw(self, surfaceIn):
        '''
        This function draws the input box and display the texts and titles onto the screen

        Parameters
        ----------
        surfaceIn: Surface
            the small font that the numbers on the axes display in

        Returns
        -------
        None
        '''
        # display the text input
        surfaceIn.blit(self.txtSurf, (self.rect.x + 5, self.rect.y + 5))
        # display the title of the input box
        titleRect = self.titleSurf.get_rect(topright=((self.rect.x-5),(self.rect.y+5)))
        surfaceIn.blit(self.titleSurf, titleRect)
        # draw input box
        pg.draw.rect(surfaceIn, self.color, self.rect, 2)
        
        
class DisplayMsg:
    """
    A class used to represent a customized text that displays in the program to show the output of calculation or illegal input 
    
    """
    def __init__(self, textIn, FONTIn):
        '''
        This function initializes the text that needs to be displayed onto the screen temporarily

        Parameters
        ----------
        textIn: String
            the text that needs to be displayed on screen
        FONTIn: Object
            the font that the text is displayed in

        Returns
        -------
        None
        '''
        self.txt = textIn
        self.FONT = FONTIn
        
        self.color = (100, 100, 100) # the color of the font
        
        self.frameCount = 0 # set the timer using the number of frames counted
        
        self.change = False # if the text is changed
        self.updateColor = False # if the color needs to be reset (a boolean to control a run-once loop)
    
    def txtChange(self):
        '''
        This function detects if the text that needs to be displayed has changed

        Parameters
        ----------
        None

        Returns
        -------
        None
        '''
        self.change = True
        self.updateColor = True
        
    def update(self):
        '''
        This function updates the display of the text to achieve the fading effect

        Parameters
        ----------
        None

        Returns
        -------
        None
        '''
        if self.change:
            if self.updateColor: # reset the color when the text is first changed
                self.color = (100, 100, 100)
                self.updateColor = False
            self.frameCount += 1 # increase the frame count
            if (self.frameCount % 3 == 0) and self.color != (255, 255, 255):
                self.color = (self.color[0]+1, self.color[1]+1, self.color[2]+1) # fading effect of the text
    
    def draw(self, surfaceIn, screenSize):
        '''
        This function displays the text onto the screen

        Parameters
        ----------
        surfaceIn: Surface
            the small font that the numbers on the axes display in
        screenSize: tuple
            the size of the screen

        Returns
        -------
        None
        '''
        txtSurf = self.FONT.render(self.txt, True, self.color)
        txtRect = txtSurf.get_rect(center = (screenSize[0]/2, screenSize[1]-20))
        surfaceIn.blit(txtSurf, txtRect)
        
        
class Text:
    """
    A class used to represent a text that shows in the program
    
    """
    def __init__(self, textIn, centerRectIn, FONTIn):
        '''
        This function initializes the text that needs to be displayed onto the screen

        Parameters
        ----------
        textIn: String
            the text that needs to be displayed on screen
        centerRectIn: tuple
            the coordinate of the center of the text-rectangle
        FONTIn: Object
            the font that the text is displayed in

        Returns
        -------
        None
        '''
        self.text = textIn
        self.textSurf = FONTIn.render(self.text, True, (0, 0, 0))
        self.rect = self.textSurf.get_rect()
        self.rect.center = centerRectIn
        
    def draw(self, surfaceIn):
        '''
        This function displays the text onto the screen

        Parameters
        ----------
        surfaceIn: Surface
            the small font that the numbers on the axes display in

        Returns
        -------
        None
        '''
        surfaceIn.blit(self.textSurf, self.rect)
        
    
class Program:
    """
    A class used to represent the program
    
    """
    def __init__(self):
        '''
        This function initializes the program

        Parameters
        ----------
        None

        Returns
        -------
        None
        '''
        # set up the main screen
        self.screenSize = (700, 550)
        self.screen = pg.display.set_mode(self.screenSize)
        
        # set up and load all of the fonts
        self.HUGEFONT = pg.font.SysFont('arial', 35, True) # set huge size font
        self.BIGFONT = pg.font.SysFont('arial', 16, True) # set big size font
        self.SMALLFONT = pg.font.SysFont('arial', 11) # set smaller size font
        # fonts for testing and debugging
        # self.HUGEFONT = pg.font.Font(None, 50) # set huge size font
        # self.BIGFONT = pg.font.Font(None, 25) # set big size font
        # self.SMALLFONT = pg.font.Font(None, 18) # set smaller size font
        
        # create a regular shape object list
        self.regShape = []
        self.regShape.append(RegShape())
        
        # create a irregular shape object list
        self.irregShape = []
        self.irregShape.append(IrregShape())
        
        # create coordinate plane and default it to not showing
        self.coordPlane = CoordinatePlane(self.SMALLFONT)
        self.showCoord = False
        
        # create display message
        self.displayMsg = DisplayMsg("", self.BIGFONT)
        
        # create the mouse drawing object
        self.mouseDraw = HandDraw()
        self.shouldMouseDraw = False
        self.mouseMove = False
        
        # create microbit drawing object and microbit
        self.microbitDraw = HandDraw()
        self.mb = Microbit()
        
        # detect if the clear button is not pressed
        self.shouldDraw = True
        
        # create a user input box list
        self.userInGroup = []
        # number of sides in regular shapes
        self.userInGroup.append(UserInput((625, 10, 40, 25), self.BIGFONT, "Number of sides: "))
        # side length in regular shapes
        self.userInGroup.append(UserInput((625, 50, 40, 25), self.BIGFONT, "Side length: "))
        # number of sides in irregular shapes
        self.userInGroup.append(UserInput((625, 10, 40, 25), self.BIGFONT, "Number of sides: "))
        # side length in irregular shapes
        self.userInGroup.append(UserInput((625, 10, 40, 25), self.BIGFONT, "Side length: "))
        # angle in irregular shapes
        self.userInGroup.append(UserInput((625, 50, 40, 25), self.BIGFONT, "Angle: "))
        
        # create a button list
        self.buttonGroup = []
        # clear button
        self.buttonGroup.append(Button((615, 500, 75, 40), "CLEAR", self.BIGFONT)) 
        # show area button
        self.buttonGroup.append(Button((540, 90, 150, 40), "calculate area", self.BIGFONT))
        # show perimeter button
        self.buttonGroup.append(Button((515, 140, 175, 40), "calculate perimeter", self.BIGFONT))
        # switch coordinate plane on button
        self.buttonGroup.append(Button((505, 450, 185, 40), "show coordinate plane", self.BIGFONT))
        # switch coordinate plane off button
        self.buttonGroup.append(Button((505, 450, 185, 40), "hide coordinate plane", self.BIGFONT))
        # draw regular shape button
        self.buttonGroup.append(Button((505, 10, 185, 40), "draw regular shapes", self.BIGFONT))
        # draw irregular shape button
        self.buttonGroup.append(Button((485, 60, 205, 40), "draw customized shapes", self.BIGFONT))
        # back to main screen button
        self.buttonGroup.append(Button((615, 400, 75, 40), "BACK", self.BIGFONT))
        # coordinate zoom in button
        self.buttonGroup.append(Button((10, 10, 30, 30), "+", self.BIGFONT))
        # coordinate zoom out button
        self.buttonGroup.append(Button((50, 10, 30, 30), "-", self.BIGFONT))
        # start drawing button
        self.buttonGroup.append(Button((275, 275, 150, 40), "START DRAWING", self.BIGFONT))
        # tutorial button
        self.buttonGroup.append(Button((300, 350, 100, 40), "TUTORIAL", self.BIGFONT))
        # go back to start screen button
        self.buttonGroup.append(Button((615, 500, 75, 40), "BACK", self.BIGFONT))
        # draw by mouse button
        self.buttonGroup.append(Button((540, 110, 150, 40), "draw with mouse", self.BIGFONT))
        # draw by microbit button
        self.buttonGroup.append(Button((520, 160, 170, 40), "draw with microbit", self.BIGFONT))
        # back to start screen
        self.buttonGroup.append(Button((10, 500, 75, 40), "BACK", self.BIGFONT))
        
        # create a display text list
        self.txtGroup = []
        # welcome text
        self.txtGroup.append(Text("GEOMETRY DISPLAYER", (350, 150), self.HUGEFONT))
        # tutorial text 1
        self.txtGroup.append(Text("This is a tool to help you display geometric shape!", (350, 25), self.BIGFONT))
        # tutorial text 2
        self.txtGroup.append(Text("You can choose to draw regular shapes,", (175, 75), self.BIGFONT))
        # tutorial text 3
        self.txtGroup.append(Text("customized/irregular shapes or even", (165, 100), self.BIGFONT))
        # tutorial text 3
        self.txtGroup.append(Text("draw by mouse or microbits!", (130, 125), self.BIGFONT))
        # tutorial text 4
        self.txtGroup.append(Text("The area and perimeter of the", (570, 175), self.BIGFONT))
        # tutorial text 5
        self.txtGroup.append(Text("shape can be calculated by the program", (525, 200), self.BIGFONT))
        # tutorial text 6
        self.txtGroup.append(Text("You can also turn on a Cartesian coordinate plane", (210, 250), self.BIGFONT))
        # tutorial text 7
        self.txtGroup.append(Text("You will be able to zoom in and out with these buttons", (225, 275), self.BIGFONT))
        # tutorial text 8
        self.txtGroup.append(Text("And if you mess up the drawing, just click the clear button", (450, 325), self.BIGFONT))
        # tutorial text 9
        self.txtGroup.append(Text("Notes while drawing:", (100, 375), self.BIGFONT))
        # tutorial text 10
        self.txtGroup.append(Text("When inputting the angle parameter for the customized drawing,", (275, 400), self.BIGFONT))
        # tutorial text 11
        self.txtGroup.append(Text("please input the angle in degree relative to the x-axis", (230, 425), self.BIGFONT))
        # tutorial text 12
        self.txtGroup.append(Text("in the counterclockwise direction", (145, 450), self.BIGFONT))
        # tutorial text 13
        self.txtGroup.append(Text("And if you want to get a precise value for a customized drawing,", (275, 475), self.BIGFONT))
        # tutorial text 14
        self.txtGroup.append(Text("remember to input the points in a clockwise direction!", (230, 500), self.BIGFONT))
        
        # create an image list
        self.imgGroup = []
        # load images for displaying in the tutorial
        self.imgGroup.append(pg.image.load("calculateButtonImg.png").convert_alpha())
        self.imgGroup.append(pg.image.load("clearButtonImg.png").convert_alpha())
        self.imgGroup.append(pg.image.load("CoordButtonImg.png").convert_alpha())
        self.imgGroup.append(pg.image.load("shapes.png").convert_alpha())
        
        self.end = False  # if the program ends
        self.clock = pg.time.Clock()
        self.gameState = -0.5
        '''
        -0.5 = start screen run once
        0 = start screen
        0.5 = tutorial screen run once
        1 = tutorial screen
        2 = main screen
        3 = regular shape
        4 = customized/irregular shape
        5 = mouse draw
        6 = microbit draw
        '''
        
    def runOnce(self):
        '''
        This function consists of all commands that only need to run once

        Parameters
        ----------
        None

        Returns
        -------
        None
        '''
        if self.gameState == -0.5:
            self.screen.fill((255, 255, 255))
            self.txtGroup[0].draw(self.screen)
            # set up the background and display the text on the start screen
            self.gameState = 0
        elif self.gameState == 0.5:
            # set up the background for the tutorial screen
            self.screen.fill((255, 255, 255))
            # display all of the texts
            for i in range(1, 16):
                self.txtGroup[i].draw(self.screen)
            # display all of the images
            self.screen.blit(pg.transform.scale(self.imgGroup[0], (1000, 550)), (100, 150))            
            self.screen.blit(pg.transform.scale(self.imgGroup[1], (1200, 600)), (75, 310))       
            self.screen.blit(pg.transform.scale(self.imgGroup[2], (800, 400)), (500, 225))
            self.screen.blit(pg.transform.scale(self.imgGroup[3], (1000, 400)), (475, 50))
            self.gameState = 1
        
    def run(self):
        '''
        This function lets the program run

        Parameters
        ----------
        None

        Returns
        -------
        None
        '''
        # when the program first opened, get the store data
        self.readData()
        while not self.end: # while the program is not ended
            self.runOnce()
            self.event()
            self.update()
            self.draw()
            pg.display.flip() # display
            self.clock.tick(100) # force frame rate to be lower
        # if there is a microbit, close connection
        if self.mb.microbit != None:
            self.mb.closeConnection()
        # store the data when the program is closed
        self.storeData()
        
    def storeData(self):
        '''
        This function stores the data of regular shapes and irregular shapes
        that were not cleared before the program ends

        Parameters
        ----------
        None

        Returns
        -------
        None
        '''
        with open('storeData.txt', 'w') as file:
            storeRegStr = []
            if len(self.regShape) >= 2:
                # store the number of sides and side length of regular shapes
                for i in self.regShape:
                    storeRegStr += (i.numOfSide, i.side)
            file.write(f'{storeRegStr}\n')
            if len(self.irregShape) >= 2:
                # store the coordinates of points / vertexes of irregular shapes on separate lines
                for i in self.irregShape:
                    file.write(f'{i.points}\n')
            file.write('\n') # create new line
            
    def readData(self):
        '''
        This function reads the stored data of regular shapes and irregular shapes
        when the program is first opened

        Parameters
        ----------
        None

        Returns
        -------
        None
        '''
        with open('storeData.txt', 'r') as file:
            # get the regular shape data without unnecessary characters
            regLst = file.readline().translate(str.maketrans('', '', '[]\n')).split(', ')
            irregLst = []
            # get the irregular shape data as separate lists without unnecessary characters, each list represents one shape
            line = file.readline()
            while line != '\n':
                irregLst.append(line.translate(str.maketrans('', '', '\n[]')).split(', '))
                line = file.readline()
            # create objects to assign the stored data to
            for i in range(int(len(regLst)/2-1)):
                self.regShape.append(RegShape())
            for i in range(int(len(irregLst))):
                self.irregShape.append(IrregShape())
            # assigning data to newly created objects
            for i in range(len(regLst)-2):
                if i % 2 == 0: # assigning number of sides data
                    self.regShape[int(i/2)].numOfSide = int(regLst[i])
                elif i % 2 == 1: # assigning side length data
                    self.regShape[math.floor(i/2)].side = float(regLst[i])
            for i in range(len(irregLst)-1):
                for j in range(len(irregLst[i])):
                    if j % 2 == 0:
                        # assining list of points to the newly created irregular shape object
                        self.irregShape[i].points.append([float(irregLst[i][j]), float(irregLst[i][j+1])])
                # set the number of sides
                self.irregShape[i].numOfSide = int(len(irregLst[i])/2-1)
                self.irregShape[i].oldShape = True
        
    def numOfSideInput(self, ev, i):
        '''
        This function gets the number of side input

        Parameters
        ----------
        ev: EventType instance
            get a single event from the queue
        i: integer
            the index of certain elements in the userInGroup list

        Returns
        -------
        None
        '''
        if self.userInGroup[i].active:
            if ev.key == pg.K_RETURN:
                try:
                    # make sure the input is an integer
                    numOfSide = int(self.userInGroup[i].txt)
                    # make sure the input is bigger or equal to three
                    if numOfSide < 3:
                        self.displayMsg.txt = "The input number of length should be at least 3."
                        self.displayMsg.txtChange()
                    else:
                        if i == 0: # if input number of sides for regular shapes
                            self.regShape[-1].numOfSide = numOfSide
                        elif i == 2: # if input number of sides for irregular
                            self.irregShape[-1].numOfSide = numOfSide
                            self.irregShape[-1].startIrregInput = True
                except:
                    self.displayMsg.txt = "The input has to be an integer."
                    self.displayMsg.txtChange()
                self.userInGroup[i].txt = "" # reset the text inside the input box
            elif ev.key == pg.K_BACKSPACE:
                self.userInGroup[i].txt = self.userInGroup[i].txt[:-1] # delete character
            else:
                self.userInGroup[i].txt += ev.unicode # add the user input text
            self.userInGroup[i].txtSurf = self.BIGFONT.render(self.userInGroup[i].txt, True, self.userInGroup[i].color)
            
    def sideLengthInput(self, ev, i):
        '''
        This function gets side length input

        Parameters
        ----------
        ev: EventType instance
            get a single event from the queue
        i: integer
            the index of certain elements in the userInGroup list

        Returns
        -------
        None
        '''
        if self.userInGroup[i].active:
            if ev.key == pg.K_RETURN:
                try: # make sure the input is a number
                    sideLen = float(self.userInGroup[i].txt)
                    if sideLen <= 0: # make sure the input is bigger than 0
                        self.displayMsg.txt = "The input number of side length needs to be positive."
                        self.displayMsg.txtChange()
                    else:
                        if i == 1: # if input side length for regular shapes
                            self.regShape[-1].side = sideLen
                        elif i == 3: # if input side length for irregular shapes
                            self.irregShape[-1].side = sideLen
                            self.irregShape[-1].sideChanged = True
                        self.shouldDraw = True
                except:
                    self.displayMsg.txt = "The input has to be a number."
                    self.displayMsg.txtChange()
                self.userInGroup[i].txt = ""
            elif ev.key == pg.K_BACKSPACE: # delete character
                self.userInGroup[i].txt = self.userInGroup[i].txt[:-1]
            else:
                self.userInGroup[i].txt += ev.unicode
            self.userInGroup[i].txtSurf = self.BIGFONT.render(self.userInGroup[i].txt, True, self.userInGroup[i].color)
            
    def angleInput(self, ev):
        '''
        This function gets angle input

        Parameters
        ----------
        ev: EventType instance

        Returns
        -------
        None
        '''
        if self.userInGroup[4].active:
            if ev.key == pg.K_RETURN:
                try: # make sure the input is a number
                    angle = float(self.userInGroup[4].txt)
                    self.irregShape[-1].angle = angle
                    self.irregShape[-1].angleChanged = True
                    self.shouldDraw = True
                except:
                    self.displayMsg.txt = "The input has to be a number."
                    self.displayMsg.txtChange()
                self.userInGroup[4].txt = ""
            elif ev.key == pg.K_BACKSPACE:
                self.userInGroup[4].txt = self.userInGroup[4].txt[:-1]
            else:
                self.userInGroup[4].txt += ev.unicode
            self.userInGroup[4].txtSurf = self.BIGFONT.render(self.userInGroup[4].txt, True, self.userInGroup[4].color)
            
    def areaPeriButtonPressed(self, func):
        '''
        This function changes the displayed text after the calculate area or perimeter button is pressed

        Parameters
        ----------
        func: a function that returns a number
            get the area or perimeter calculated function

        Returns
        -------
        None
        '''
        if self.shouldDraw:
            self.displayMsg.txt = str(func)
        else:
            self.displayMsg.txt = "No shape is displayed"
        self.displayMsg.txtChange()
        
    def checkAreaPeriButton(self, objLst):
        '''
        This function detects if the claculate area or perimeter button is pressed

        Parameters
        ----------
        objLst: list
            a list of objects of either regular shapes or irregular shapes

        Returns
        -------
        None
        '''
        if self.buttonGroup[1].mouseCollide(): # if calculate area is pressed
            try: 
                self.areaPeriButtonPressed(objLst[-2].getArea())
            except:
                self.displayMsg.txt = "No shape is displayed"
                self.displayMsg.txtChange()
        elif self.buttonGroup[2].mouseCollide(): # if calculate perimeter is pressed
            try:
                self.areaPeriButtonPressed(objLst[-2].getPerimeter())
            except:
                self.displayMsg.txt = "No shape is displayed"
                self.displayMsg.txtChange()
    
    def backButtonPressed(self):
        '''
        This function detects if the back button is pressed

        Parameters
        ----------
        None

        Returns
        -------
        None
        '''
        if self.buttonGroup[7].mouseCollide():
            self.gameState = 2
            
    def clrCoordButtonPressed(self):
        '''
        This function detects if the clear or show / hide coordinate plane button is pressed

        Parameters
        ----------
        None

        Returns
        -------
        None
        '''
        if self.buttonGroup[0].mouseCollide(): # if clear button is pressed
            if self.gameState == 2 or self.gameState == 3 or self.gameState == 4:
                self.shouldDraw = False
                self.regShape = [RegShape()]
                self.irregShape = [IrregShape()]
            if self.gameState == 5:
                self.mouseDraw.reset()
            elif self.gameState == 6:
                self.microbitDraw.reset()
        elif not self.showCoord and self.buttonGroup[3].mouseCollide(): # if show coordinate plane button is pressed
            self.showCoord = True
        elif self.showCoord and self.buttonGroup[4].mouseCollide(): # if hide coordinate plane button is pressed
            self.showCoord = False
            
    def zoomButtonPressed(self):
        '''
        This function detects if the coom in / out button is pressed

        Parameters
        ----------
        None

        Returns
        -------
        None
        '''
        if self.showCoord: # if the coordinate plane is showing
            if self.buttonGroup[8].mouseCollide(): # zoom in
                self.coordPlane.scale /= 2 # rescale
                for i in self.regShape: # rescale for regular shapes
                    i.scale = self.coordPlane.scale
            elif self.buttonGroup[9].mouseCollide(): # zoom out
                self.coordPlane.scale *= 2
                for i in self.regShape: # rescale for regular shapes
                    i.scale = self.coordPlane.scale
           
    def event(self):
        '''
        This function detects any user event

        Parameters
        ----------
        None

        Returns
        -------
        None
        '''
        ev = pg.event.poll() # Look for any event
        if ev.type == pg.QUIT:  
            self.end = True
        if self.gameState == 0: # start screen
            if ev.type == pg.MOUSEBUTTONDOWN:
                if self.buttonGroup[10].mouseCollide(): # start button pressed
                    self.gameState = 2
                elif self.buttonGroup[11].mouseCollide(): # tutorial button pressed
                    self.gameState = 0.5
        elif self.gameState == 1: # tutorial screen
            if ev.type == pg.MOUSEBUTTONDOWN:
                if self.buttonGroup[12].mouseCollide(): # back button pressed
                    self.gameState = -0.5
        elif self.gameState == 2: # main screen
            if ev.type == pg.MOUSEBUTTONDOWN:
                # detects any button pressed
                self.clrCoordButtonPressed()
                self.zoomButtonPressed()
                if self.buttonGroup[5].mouseCollide(): # draw regular shapes
                    self.gameState = 3
                elif self.buttonGroup[6].mouseCollide(): # draw irregular shapes
                    self.gameState = 4
                elif self.buttonGroup[13].mouseCollide(): # draw with mouse
                    self.gameState = 5
                elif self.buttonGroup[14].mouseCollide(): # draw with microbit
                    self.gameState = 6
                elif self.buttonGroup[15].mouseCollide(): # back button
                    self.gameState = -0.5
        elif self.gameState == 3: # regular shapes
            if ev.type == pg.MOUSEBUTTONDOWN:
                # detects any button pressed
                self.clrCoordButtonPressed()
                self.zoomButtonPressed()
                self.backButtonPressed()
                self.checkAreaPeriButton(self.regShape)
                for i in range(2): # if user input boxes are pressed
                    self.userInGroup[i].mouseCollide()
                    self.userInGroup[i].color = (0, 0, 0) if self.userInGroup[i].active else (200, 200, 200)
            elif ev.type == pg.KEYDOWN:
                self.numOfSideInput(ev, 0)
                self.sideLengthInput(ev, 1)
        elif self.gameState == 4: # irregular shapes
            if ev.type == pg.MOUSEBUTTONDOWN:
                # detect if any button pressed
                self.clrCoordButtonPressed()
                self.zoomButtonPressed()
                self.backButtonPressed()
                self.checkAreaPeriButton(self.irregShape)
                # detect if any user input boxes are pressed
                for i in range(2, 5):
                    if (i == 2 and self.irregShape[-1].startIrregInput == False) or (i != 2 and self.irregShape[-1].startIrregInput == True):
                        if self.userInGroup[i].mouseCollide():
                            if i == 2:
                                self.irregShape[-1].startIrregInput = False
                        self.userInGroup[i].color = (0, 0, 0) if self.userInGroup[i].active else (200, 200, 200)
            elif ev.type == pg.KEYDOWN:
                # number of sides input are separate from other two inputs
                if self.irregShape[-1].startIrregInput == False:
                    self.numOfSideInput(ev, 2)
                elif self.irregShape[-1].startIrregInput == True:
                    self.sideLengthInput(ev, 3)
                    self.angleInput(ev)
        elif self.gameState == 5: # draw with mouse
            if ev.type == pg.MOUSEBUTTONDOWN:
                # detect if any button is pressed
                self.clrCoordButtonPressed()
                self.backButtonPressed()
                self.mouseDraw.drawing = True # start tracing
            elif ev.type == pg.MOUSEMOTION:
                self.mouseDraw.moDraw() # tracing
            elif ev.type == pg.MOUSEBUTTONUP:
                self.mouseDraw.drawing = False # stop tracing and cuts the line
                self.mouseDraw.lineCut()
        elif self.gameState == 6: # draw with microbit
            if ev.type == pg.MOUSEBUTTONDOWN:
                # detect if any button is pressed
                self.clrCoordButtonPressed()
                self.backButtonPressed()
            if not self.mb.isReady(): # if microbit is not connected
                self.displayMsg.txt = "No microbit detected."
                self.displayMsg.txtChange()
            elif self.mb.isReady(): # if microbit is connected
                self.microbitDraw.drawing = True
                line = self.mb.nonBlockingReadRecentLine()
                if line != None:
                    x, y = line.split() # get the x and y componenets of acceleration
                    self.microbitDraw.microDraw(x, y)
                    
    def update(self):
        '''
        This function updates texts and lists

        Parameters
        ----------
        None

        Returns
        -------
        None
        '''
        self.displayMsg.update() # update the display message
        if self.gameState == 3:
            for i in range(2):
                self.userInGroup[i].update() # update the user input box if the input is too long
            if self.regShape[-1].numOfSide != None and self.regShape[-1].side != None:
                    self.regShape.append(RegShape()) # if the last regular shape is finished inputting, add a new shape to the list
        elif self.gameState == 4:
            for i in range(2, 5):
                self.userInGroup[i].update() # update the user input box if the input is too long
            if self.irregShape[-1].finishDrawing:
                self.irregShape.append(IrregShape()) # if the last irregular shape is finished inputting, add a new shape to the list
        
    def drawMostUsedButtons(self):
        '''
        This function draws some of the most used buttons

        Parameters
        ----------
        None

        Returns
        -------
        None
        '''
        # draw show / hide coordinate plane
        if self.showCoord:
            self.coordPlane.draw(self.screen)
            self.buttonGroup[4].draw(self.screen)
        elif not self.showCoord:
            self.buttonGroup[3].draw(self.screen)
        self.buttonGroup[0].draw(self.screen)
        # draw zoom in/out button
        if self.gameState != 5 and self.gameState != 6:
            for i in range(8, 10):
                self.buttonGroup[i].draw(self.screen)
        # draw back button
        if self.gameState == 3 or self.gameState == 4 or self.gameState == 5 or self.gameState == 6:
            self.buttonGroup[7].draw(self.screen)
        # draw calcualte area / perimeter buttons
        if self.gameState == 3 or self.gameState == 4:
            for i in range(1, 3):
                self.buttonGroup[i].draw(self.screen)
        
    def draw(self):
        '''
        This function draws shapes, buttons, user input boxes, and display texts and messages

        Parameters
        ----------
        None

        Returns
        -------
        None
        '''
        if self.gameState == 0: # start screen
            for i in range(10, 12): # draw buttons
                self.buttonGroup[i].draw(self.screen)
        elif self.gameState == 1: # tutorial screen
            # draw back button
            self.buttonGroup[12].draw(self.screen)
        elif self.gameState == 2: # main screen
            # set background
            self.screen.fill((255, 255, 255))
            # draw display message
            self.displayMsg.draw(self.screen, self.screenSize)
            # draw buttons
            self.drawMostUsedButtons()
            for i in range(5, 7):
                self.buttonGroup[i].draw(self.screen)
            for i in range(13, 16):
                self.buttonGroup[i].draw(self.screen)
            # draw regular and irregular shapes
            if self.shouldDraw:
                for i in self.regShape:
                    i.draw(self.screen)
                for i in self.irregShape:
                    i.draw(self.screen, self.coordPlane.scale)
        elif self.gameState == 3: # regular shape
            # set up background
            self.screen.fill((255, 255, 255))
            #display message
            self.displayMsg.draw(self.screen, self.screenSize)
            # draw buttons
            self.drawMostUsedButtons()
            # draw regular shapes
            if self.shouldDraw:
                for i in self.regShape:
                    i.draw(self.screen)
            # draw user input boxes
            for i in range(2):
                self.userInGroup[i].draw(self.screen)
        elif self.gameState == 4: # irregular shape
            self.screen.fill((255, 255, 255))
            self.displayMsg.draw(self.screen, self.screenSize)
            self.drawMostUsedButtons()
            # draw irregular shapes
            if self.shouldDraw:
                for i in self.irregShape:
                    i.draw(self.screen, self.coordPlane.scale)
            # draw user input boxes
            if not self.irregShape[-1].startIrregInput:
                self.userInGroup[2].draw(self.screen)
            elif self.irregShape[-1].startIrregInput:
                for i in range(3,5):
                    self.userInGroup[i].draw(self.screen)
        elif self.gameState == 5: # draw with mouse
            self.screen.fill((255, 255, 255))
            self.mouseDraw.display(self.screen)
            self.drawMostUsedButtons()
        elif self.gameState == 6: # draw with microbit
            self.screen.fill((255, 255, 255))
            self.microbitDraw.display(self.screen)
            self.drawMostUsedButtons()
            self.displayMsg.draw(self.screen, self.screenSize)
                

pg.init() # initialize the program
program = Program() # create program object
program.run() # run program
pg.quit() # quit program
