#import required libraries
import pygame, math

#initialise pygame
pygame.init()
pygame.display.set_caption("Battleships")
window = pygame.display.set_mode((1000,1000))
clock = pygame.time.Clock()
fps = 60
dt = 0

def checkDuplicate(data):
    for item1 in data:
        found = False
        for item2 in data:
            if item1 == item2 and not found:
                found = True
            elif item1 == item2 and found:
                return True
    return False

class ship:
    def __init__(self, length, startPos, colour):
        self.length = length
        self.dimensions = 50
        self.selected = False
        self.position = False
        self.surface = pygame.Rect(startPos[0], startPos[1], self.dimensions, self.dimensions*length)
        self.startPos = startPos
        self.colour = colour
        self.shipPlaced = False
        self.updatePoints()

    def updatePoints(self):
        self.points = []
        for x in range(self.length):
            if self.surface.height > self.surface.width:
                #orientated vertically
                self.points.append((self.surface.x, self.surface.y+(x*self.dimensions)))
            else:
                #orientated horizontally
                self.points.append((self.surface.x+(x*self.dimensions), self.surface.y))
            
    def update(self, mousePos, prevMousePos, click):
        self.shipPlacement(mousePos, prevMousePos, click)

        #draw rectangle to screen
        pygame.draw.rect(window, self.colour, self.surface)

    def shipPlacement(self, mousePos, prevMousePos, click):
        global shipSelected
        if click and self.surface.collidepoint(mousePos[0], mousePos[1]) and shipSelected == False:
            #start moving if rectangle clicked
            self.selected = True
            shipSelected = True

            if self.shipPlaced:
                #if ship has already been placed, change cell values back to none 
                board.changeCellContents(self.points, None)

        if click and self.selected:
            #move by change in mouse movement
            self.surface.x += mousePos[0] - prevMousePos[0]
            self.surface.y += mousePos[1] - prevMousePos[1]
            self.updatePoints()
            coords = [board.closestCell(point) for point in self.points]
            board.changeBoardColour((255,255,255))
            board.changeCellColour((0,255,0), coords)

        elif click == False and self.selected:
            #stop moving once mouse click released
            self.selected = False
            shipSelected = False
            coords = [board.closestCell(point) for point in self.points]
            
            #check for duplicates or if cells already contain ships (invalid positions)
            if checkDuplicate(coords) or board.cellsContain(coords):
                #there is a duplicate, reset position
                self.surface.topleft = self.startPos
            else:
                #place ship
                self.points = []
                for coord in coords:
                    self.points.append(coord)

                self.shipPlaced = True
                self.surface.topleft = (coords[0][0]*self.dimensions, coords[0][1]*self.dimensions)
                board.changeCellContents(coords, self)
            board.changeBoardColour((255,255,255))

    def checkRotate(self, mousePos):
        #if currently selected, rotate
        if self.selected:
            #swap width and height
            width = self.surface.width
            self.surface.width = self.surface.height
            self.surface.height = width
            #set centre of rectangle to mouse position
            self.surface.center = mousePos
            self.updatePoints()

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
        
        return closeCellPos
    
    def changeCellColour(self, colour, points):
        for coord in points:
            self.board[coord[1]][coord[0]].colour = colour

    def changeBoardColour(self, colour):
        for y in range(10):
            for x in range(10):
                self.board[y][x].colour = colour

    def cellsContain(self, coords):
        for coord in coords:
            if self.board[coord[1]][coord[0]].value != None:
                return True
        return False
    
    def changeCellContents(self, coords, newVal):
        for coord in coords:
            self.board[coord[1]][coord[0]].value = newVal

                
    def update(self):
        #draw cells to screen
        for row in self.board:
            for obj in row:
                obj.update()

class cell:
    def __init__(self, x, y):
        self.surface = pygame.Rect(x*50, y*50, 50, 50)
        self.colour = (255,255,255)
        self.value = None

    def update(self):
        #draw cell to screen
        pygame.draw.rect(window, self.colour, self.surface)

    def findDistance(self, coord):
        #calclate distance between coordinate and center of cell using pythagoras
        self.distance = math.sqrt((coord[0]-self.surface.x)**2 + (coord[1]-self.surface.y)**2)


#create object for testing       
ships = [ship(4, (50,50), (255,0,0)), ship(3, (100,100), (0,0,255))]
board = gameBoard()

shipSelected = False

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
                for obj in ships:
                    obj.checkRotate(mousePos)

    #get the mouse details 
    mousePos = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()[0]

    #draw objects to the screen
    window.fill((0,0,0))
    board.update()

    for obj in ships:
        obj.update(mousePos, prevMousePos, click)

    prevMousePos = mousePos

    #update window and get time difference between frames
    pygame.display.update()
    dt = clock.tick(fps) / 1000

pygame.quit()