#import required libraries
import pygame, math

#initialise pygame
pygame.init()
pygame.display.set_caption("Battleships")
window = pygame.display.set_mode((1000,1000))
clock = pygame.time.Clock()
fps = 60
dt = 0

class ship:
    def __init__(self, length):
        self.length = length
        self.dimensions = 50
        self.placed = True
        self.surface = pygame.Rect(0, 0, self.dimensions, self.dimensions*length)

        if self.length % 2 == 0:
            self.maxLim = maxLim = int(50*(self.length//2))+50
            self.minLim = -int(50*(self.length//2))+50
        else:
            self.maxLim = int(50*(self.length//2))+50
            self.minLim = -int(50*(self.length//2))
    
    def update(self, mousePos, prevMousePos, click):
        self.shipPlacement(mousePos, prevMousePos, click)

        #draw rectangle to screen
        pygame.draw.rect(window, (255,0,0), self.surface)

    def shipPlacement(self, mousePos, prevMousePos, click):
        if click and self.surface.collidepoint(mousePos[0], mousePos[1]):
            #start moving if rectangle clicked
            self.placed = False

        if click and self.placed == False:
            #move by change in mouse movement
            self.surface.x += mousePos[0] - prevMousePos[0]
            self.surface.y += mousePos[1] - prevMousePos[1]
        elif click == False and self.placed == False:
            #stop moving once mouse click released
            self.placed = True
            if self.surface.height > self.surface.width:
                #the ship is orientated vertically 
                print(f"X boundary{self.surface.left, self.surface.right}")
                print(f"Y boundary{self.surface.top, self.surface.bottom}")
                if self.length % 2 == 0:
                    #ship length is even
                    coords = [board.closestCell((self.surface.center[0], self.surface.center[1]-(self.dimensions/2)+y)) for y in range(self.minLim, self.maxLim, self.dimensions)]
                else:
                    #ship length is uneven
                    coords = [board.closestCell((self.surface.center[0], self.surface.center[1]+y)) for y in range(self.minLim, self.maxLim, self.dimensions)]
            else:
                #the ship is orientated horizontally 
                if self.length % 2 == 0:
                    #ship length is even
                    coords = [board.closestCell((self.surface.center[0]-(self.dimensions/2)+x, self.surface.center[1])) for x in range(self.minLim, self.maxLim, self.dimensions)]
                else:
                    #ship length is uneven
                    coords = [board.closestCell((self.surface.center[0]+x, self.surface.center[1])) for x in range(self.minLim, self.maxLim, self.dimensions)]
            print(f"Closest cell coordinates: {coords}")


    def rotate(self, mousePos):
        #if currently selected, rotate
        if self.placed == False:
            #swap width and height
            width = self.surface.width
            self.surface.width = self.surface.height
            self.surface.height = width
            #set centre of rectangle to mouse position
            self.surface.center = mousePos

class gameBoard():
    def __init__(self):
        self.board = [[cell(x,y) for x in range(10)] for y in range(10)]

    def closestCell(self, coord):
        #find the closest cell to a coordinate
        closeCellPos = (0,0)
        for y in range(10):
            for x in range(10):
                self.board[y][x].findDistance(coord)
                if self.board[y][x].distance < self.board[closeCellPos[1]][closeCellPos[0]].distance:
                    closeCellPos = (x, y)

        return self.board[closeCellPos[1]][closeCellPos[0]].surface.center
                
    def update(self):
        #draw cells to screen
        for row in self.board:
            for obj in row:
                obj.update()

class cell:
    def __init__(self, x, y):
        self.surface = pygame.Rect(x*50, y*50, 50, 50)
        self.colour = (255,255,255)

    def update(self):
        #draw cell to screen
        pygame.draw.rect(window, self.colour, self.surface, width=1)

    def findDistance(self, coord):
        #calclate distance between coordinate and center of cell using pythagoras
        self.distance = math.sqrt((coord[0]-self.surface.centerx)**2 + (coord[1]-self.surface.centery)**2)
s
#create object for testing       
s = ship(4)
board = gameBoard()

prevMousePos = (0,0)

#game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            #close the game
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                #when r is pressed, rotate the ship
                s.rotate(mousePos)

    #get the mouse details 
    mousePos = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()[0]

    #draw objects to the screen
    window.fill((0,0,0))
    board.update()
    s.update(mousePos, prevMousePos, click)

    prevMousePos = mousePos

    #update window and get time difference between frames
    pygame.display.update()
    dt = clock.tick(fps) / 1000

pygame.quit()