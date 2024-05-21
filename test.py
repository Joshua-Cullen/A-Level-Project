import pygame, math

pygame.init()
window = pygame.display.set_mode((800,800))
clock = pygame.time.Clock()
fps = 60
dt = 0
running = True
arial = pygame.font.SysFont("arial", 50)

def switchPlayer(currentPlayer):
    #switches between the players in the list
    if players[currentPlayer] == players[0]:
        currentPlayer = 1
    else:
        currentPlayer = 0
    return currentPlayer

def checkDuplicate(data):
    for item1 in data:
        found = False
        for item2 in data:
            if item1 == item2 and not found:
                found = True
            elif item1 == item2 and found:
                return True
    return False

def displayText(font, text, pos, colour):
    text = font.render(text, True, colour)
    window.blit(text, pos)


def shipPlacement(player):
    global shipSelected
    player.board.changeBoardColour((255,255,255))
    for index in range(len(player.ships)):
        shipSelected = player.ships[index].checkSelected(shipSelected)

        if player.ships[index].selected and click:
            #if the ship is currently being hovered over and clicked
            if player.ships[index].placed:
                #if the ship has already been placed, then change cell values back to None
                player.board.changeCellContents(player.ships[index].points, None)
                player.ships[index].placed = False

            #ship is currently selected and being moved
            player.ships[index].surface.x += mousePos[0] - prevMousePos[0]
            player.ships[index].surface.y += mousePos[1] - prevMousePos[1]
            player.ships[index].updatePoints()
            coords = [player.board.closestCell(point) for point in player.ships[index].points]

            if checkDuplicate(coords) or player.board.cellsContain(coords):
                #position invalid
                player.board.changeCellColour((255,0,0), coords)
            else:
                #position valid
                player.board.changeCellColour((0,255,0), coords)

        elif player.ships[index].selected and click == False:
            #ship was being moved but has now been released - needs to be placed
            coords = [player.board.closestCell(point) for point in player.ships[index].points]

            #check for duplicates or if cells already contain another ship
            if checkDuplicate(coords) or player.board.cellsContain(coords):
                #there is a duplicate, reset position
                player.ships[index].resetPos()
            
            else:
                #place ship (self.points now is used to store the cell coordinates)
                player.ships[index].points = []
                player.ships[index].origPoints = []
                for coord in coords:
                    player.ships[index].points.append(coord)
                    player.ships[index].origPoints.append(coord)

                #place ship in new position 
                player.ships[index].surface.topleft = (coords[0][0]*player.ships[index].dimensions, coords[0][1]*player.ships[index].dimensions)
                player.board.changeCellContents(coords, player.ships[index].id)

                #change boolean values
                player.ships[index].placed = True
                player.ships[index].selected = False
            shipSelected = None

    #draw the ships and board to the screen
    player.board.update()
    for ship in player.ships:
        ship.update()

    if readyButton.update():
        #if the button is clicked
        for ship in player.ships:
            if ship.placed == False:
                return player, False
        return player, True
    return player, False
    #if the button has been pressed and all ships have been placed, then return player, True
    #else return player, False 

#How to split takeGo function so works with computer class as well
#select cell - should be different for the computer and the player
#decide whether cell is hit or miss / display graphics / pause after hit - happens no matter computer/player

def takeGo(player, enemy):
    global paused, timeElapsed, msg
    finished = False

    if paused == False:
        player.board.changeBoardColour((255,255,255))
        #find the cell the user is currently hovering over
        cell = player.board.selectedCell(mousePos)

        if cell != None:
            #the mouse is hovering over a cell
            player.board.changeCellColour("darkgray", [cell])

            if click:
                #when a cell is clicked
                if player.board.board[cell[1]][cell[0]].hit == False:
                    #the position has not already been selected

                    #find the relevant ship and remove the point from the ship 
                    for ship in enemy.ships:
                        result = ship.checkHit(cell)
                        if result == "hit":
                            msg = "Hit"
                            player.board.board[cell[1]][cell[0]].value = "hit"
                            break
                        elif result == "sunk":
                            player.board.changeCellContents(ship.origPoints, "sunk")
                            enemy.ships.remove(ship)
                            msg = "Sunk"
                            break
                    
                    if result == None:
                        #the selected cell has missed all enemy ships 
                        msg = "Miss"
                        player.board.board[cell[1]][cell[0]].value = "miss"

                    paused = True

                else:
                    #already selected  
                    pass

                player.board.board[cell[1]][cell[0]].hit = True

    else:
        #create a pause of 2 seconds 
        timeElapsed += dt
        displayText(arial, msg, (550,0), (255,255,255)) 
        if timeElapsed > 2:
            paused = False 
            timeElapsed = 0 
            finished = True

    player.board.showHits()

    return player, enemy, finished, len(enemy.ships) == 0 and not(paused)

class computer:
    def __init__(self, id):
        self.id = id

    def placeShips(self):
        pass

class easy(computer):
    def chooseSpot(self):
        pass

class medium(computer):
    def chooseSpot(self):
        pass

class hard(computer):
    def chooseSpot(self):
        pass

class ship:
    def __init__(self, id, length, startPos, colour):
        self.id = id
        self.length = length
        self.startPos = startPos
        self.colour = colour 
        self.dimensions = 50
        self.surface = pygame.Rect(startPos[0], startPos[1], self.dimensions, self.dimensions*length)
        self.selected = False
        self.placed = False
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

    def checkSelected(self, shipSelected):
        if self.surface.collidepoint(mousePos[0], mousePos[1]) and click:
            if shipSelected == None:
                shipSelected = self.id
            
            self.selected = shipSelected == self.id
        return shipSelected
    
    def checkHit(self, coord):
        if coord in self.points:
            #if the ship has been hit, remove the point from points
            self.points.remove(coord)

            if len(self.points) == 0:
                #if all the ship's points have been hit, it has been sunk
                return "sunk"
            return "hit"
        
        #return none if the coord did not hit this specific ship 
        return None
    
    def resetPos(self):
        if self.surface.width > self.surface.height:
            self.rotate()
        self.surface.topleft = self.startPos
        
    def rotate(self):
        #swap width and height
        width = self.surface.width
        self.surface.width = self.surface.height
        self.surface.height = width
        #set centre of rectangle to mouse position
        self.surface.center = mousePos
        self.updatePoints()

    def update(self):
        #draw rectangle to screen
        pygame.draw.rect(window, self.colour, self.surface)

        
class gameBoard():
    def __init__(self):
        self.board = [[cell(x,y) for x in range(10)] for y in range(10)]
        self.surface = pygame.Rect(0,0,500,500)

    def closestCell(self, coord):
        #find the closest cell to a coordinate
        closeCellPos = (0,0)
        for y in range(10):
            for x in range(10):
                self.board[y][x].findDistance(coord)
                if self.board[y][x].distance < self.board[closeCellPos[1]][closeCellPos[0]].distance:
                    closeCellPos = (x, y)
        
        return closeCellPos
    
    def showHits(self):
        for row in self.board:
            for cell in row:
                if cell.value == "hit":
                    colour = (0,255,0)
                elif cell.value == "miss":
                    colour = (255,0,0)
                elif cell.value == "sunk":
                    colour = (255,255,0)
                else:
                    colour = cell.colour
                    
                pygame.draw.rect(window, colour, cell.surface)
    
    def selectedCell(self, coord):
        for y in range(10):
            for x in range(10):
                if self.board[y][x].surface.collidepoint(coord):
                    return (x,y)
        return None
    
    def changeCellColour(self, colour, points):
        #change particular cell colours 
        for coord in points:
            self.board[coord[1]][coord[0]].colour = colour

    def changeBoardColour(self, colour):
        #reset the entire board colour 
        for y in range(10):
            for x in range(10):
                self.board[y][x].colour = colour

    def cellsContain(self, coords):
        #check if cells contain a value other than None
        for coord in coords:
            if self.board[coord[1]][coord[0]].value != None:
                return True
        return False
    
    def changeCellContents(self, coords, newVal):
        #update the contents of certain cells to newVal
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
        self.hit = False

    def update(self):
        #draw cell to screen
        pygame.draw.rect(window, self.colour, self.surface)

    def findDistance(self, coord):
        #calclate distance between coordinate and center of cell using pythagoras
        self.distance = math.sqrt((coord[0]-self.surface.x)**2 + (coord[1]-self.surface.y)**2)

class player:
    def __init__(self, id):
        self.ships = [ship("1", 4, (525,25), "darkgray"), ship("2", 3, (600, 25), "darkgray")]
        self.board = gameBoard()

        self.placingShips = True
        self.takingGo = False

        self.id = id 

    def update(self, enemy):
        if self.placingShips:
            self, finished = shipPlacement(self)

            self.placingShips = not(finished)
            self.takingGo = finished
        
        elif self.takingGo:
            self, enemy, finished, won = takeGo(self, enemy)
            if won:
                return enemy, "won"

        else:
            finished = False

        displayText(arial, self.id, (550,75), (255,255,255))

        return enemy, finished
    
class button:
    def __init__(self, x, y, width, height):
        self.surface = pygame.Rect(x, y, width, height)
    
    def update(self):
        #draws the buttton to the screen 
        pygame.draw.rect(window, (255,255,255), self.surface)

        if self.surface.collidepoint(mousePos) and click and prevClick == False:
            #if the button is pressed 
            return True
        else:
            return False

players = [player("Player 1"), player("Player 2")]
currentPlayer = 0
shipSelected = None

readyButton = button(550,300, 100, 50)

paused = False
timeElapsed = 0

game = True
winScreen = False

prevClick = False
prevMousePos = (0,0)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                if players[currentPlayer].placingShips:
                    for obj in players[currentPlayer].ships:
                        if obj.selected:
                            obj.rotate() 

    window.fill((0,0,0))

    mousePos = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()[0]

    if game:
        players[switchPlayer(currentPlayer)], finished = players[currentPlayer].update(players[switchPlayer(currentPlayer)])
        if finished == True:
            currentPlayer = switchPlayer(currentPlayer)
        elif finished == "won":
            winScreen = True
            game = False

    elif winScreen:
        displayText(arial, f'{players[currentPlayer].id} has won', (0,0), (255,255,255))
    
    prevClick = click
    prevMousePos = mousePos
    pygame.display.update()
    dt = clock.tick(fps) / 1000