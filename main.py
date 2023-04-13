import random
import sys
import pygame
from pygame.locals import *

# global variables
FPS = 30
ScreenWidth = 600
ScreenHeight = 600
score = 0 
Screen = pygame.display.set_mode((ScreenWidth,ScreenHeight))
GroundY = ScreenHeight * 0.8
Game_Images = {}
Game_Sounds = {}
Pipe = 'gallery/images/pipe.png'
# Ground = '/gallery/images/ground.png'
Background = 'gallery/images/background.png'
player = 'gallery/images/bird.png'

# start game screen 
def welcomeScreen():
    blue = (0, 0, 128)
    playerx = int((ScreenWidth - Game_Images['player'].get_height())/2)
    playery = int((ScreenHeight - Game_Images['player'].get_height())/2)
    messagex = int((ScreenWidth - Game_Images['message'].get_width())/2)
    messagey = int(ScreenHeight*0.3)
    basex = 0
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                return mainGame()
            else:
                Screen.blit(Game_Images['background'],(0, 0))
                Screen.blit(Game_Images['player'],( playerx,playery))
                Screen.blit(Game_Images['message'],( messagex,messagey ))
                Screen.blit(Game_Images['base'],( basex,GroundY ))
                font = pygame.font.Font('freesansbold.ttf', 32)
                text = font.render('Press space to start', True, blue, None)
                textRect = text.get_rect()
                textRect.center = (ScreenWidth // 2, ScreenHeight * 0.6 )
                Screen.blit(text, textRect)
                pygame.display.update()
                FPSClock.tick(FPS)
def mainGame():
    global score
    playerx = ScreenWidth // 9
    playery = ScreenHeight  // 3
    basex = 0
    newPipe1 = getPipe()
    newPipe2 = getPipe()
    
    upperpipe = [
        {'x': ScreenWidth+200, 'y':newPipe1[0]['y']},
        {'x': ScreenWidth + 200 + (ScreenWidth//2), 'y': newPipe2[0]['y']}
    ]
    lowerpipe = [
        {'x': ScreenWidth+200, 'y':newPipe1[1]['y']},
        {'x': ScreenWidth + 200 + (ScreenWidth//2), 'y': newPipe2[1]['y']}
    ]
    pipeVelX = -6
    playerVely = 5
    playerMaxVel = 10
    playerMinVel = -9
    playerAccY = 2
    playerflapVel = -12
    playerflapped = False
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and event.key == K_SPACE:
                if playery > 0:
                    playerVely = playerflapVel
                    playerflapped = True
                    Game_Sounds['wing'].play()
        crashtest = iscollide(playerx,playery,upperpipe,lowerpipe)
        if crashtest:
            return extraScreen()
        

        # score 
        playermid = playerx + Game_Images['player'].get_width()
        for pipe in upperpipe:
            pipemid = pipe['x'] + Game_Images['pipe'][0].get_width()
            if pipemid <= playermid < pipemid + 6:
                score += 1
                Game_Sounds['point'].play()
        if playerVely < playerMaxVel and not playerflapped:
            playerVely += playerAccY
        if playerflapped:
            playerflapped = False
        playerh = Game_Images['player'].get_height()
        playery = playery + min(playerVely, GroundY - playery - playerh)

        # moves pipe left 
        for upper,lower in zip(upperpipe,lowerpipe):
            upper['x'] += pipeVelX
            lower['x'] += pipeVelX
        if 0 < upperpipe[0]['x'] < 6:
            newpipe = getPipe()
            upperpipe.append(newpipe[0])
            lowerpipe.append(newpipe[1])
        if upperpipe[0]['x'] < -Game_Images['pipe'][0].get_width():
            upperpipe.pop(0)
            lowerpipe.pop(0)
        Screen.blit(Game_Images['background'],(0, 0))
        Screen.blit(Game_Images['player'],( playerx,playery))
        for upper,lower in zip(upperpipe,lowerpipe):
            Screen.blit(Game_Images['pipe'][1],(lower['x'],lower['y']))
            Screen.blit(Game_Images['pipe'][0],(upper['x'],upper['y']))
        Screen.blit(Game_Images['base'],( basex,GroundY ))
        Digits = [int(x) for x in list(str(score))]
        width = 0
        for digit in Digits:
            width += Game_Images['numbers'][digit].get_width()
        xoffset = (ScreenWidth - Game_Images['numbers'][digit].get_width())//2
        for digit in Digits:
            Screen.blit(Game_Images['numbers'][digit],(xoffset,ScreenHeight*0.82))
            xoffset += Game_Images['numbers'][digit].get_width()
        pygame.display.update()
        FPSClock.tick(FPS)
        
# creating pipes
def getPipe():
    pipeHeight = Game_Images['pipe'][0].get_height()
    offset = ScreenHeight * 0.25
    pipe1y = ScreenHeight * random.uniform(0.3,0.6)
    pipe2y = pipe1y - (Game_Images['pipe'][0].get_height() + offset)
    pipe = [
        {'x': ScreenWidth+10,'y':pipe2y},
        {'x': ScreenWidth+10, 'y':pipe1y}
    ]
    return pipe
    
def iscollide(px, py , Up, Lp):

    if py == GroundY - Game_Images['player'].get_height() or py < 0:
        Game_Sounds['hit'].play()
        Screen.blit(Game_Images['dead'],(px,py))
        pygame.display.update()
        FPSClock.tick(FPS) 
        return True

    for pipe in Up:
        pipeheight = Game_Images['pipe'][0].get_height()
        if (py <= pipeheight + pipe['y']) and pipe['x'] <= px + Game_Images['player'].get_width() <= pipe['x'] + Game_Images['pipe'][0].get_width():
            Game_Sounds['die'].play()
            Screen.blit(Game_Images['dead'],(px,py))
            pygame.display.update()
            FPSClock.tick(FPS)           
            return True
    for pipe in Lp:
        pipeheight = Game_Images['pipe'][0].get_height()
        if (py + Game_Images['player'].get_height() -5 > pipe['y']) and pipe['x'] <= px + Game_Images['player'].get_width() <= pipe['x'] + Game_Images['pipe'][0].get_width():
            Game_Sounds['die'].play()
            Screen.blit(Game_Images['dead'],(px,py))
            pygame.display.update()
            FPSClock.tick(FPS)           
            return True
    return False
def GameOver():
    blue = (0, 0, 128)
    basex = 0
    playerx = (ScreenWidth - Game_Images['player'].get_width())//2
    playery = ScreenHeight * 0.25
    global score
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and event.key == K_SPACE:
                return welcomeScreen()
            else:
                Screen.blit(Game_Images['background'],(0,0))
                Screen.blit(Game_Images['base'],(basex,GroundY))
                Screen.blit(Game_Images['dead'],(playerx,playery))
                font = pygame.font.Font('freesansbold.ttf', 36)
                text = font.render('Your Score', True, blue, None)
                textRect = text.get_rect()
                textRect.center = (ScreenWidth // 2, ScreenHeight * 0.6 )
                Screen.blit(text, textRect)
                Digits = [int(x) for x in list(str(score))]
                width = 0
                for digit in Digits:
                    width += Game_Images['numbers'][digit].get_width()
                xoffset = (ScreenWidth - Game_Images['numbers'][digit].get_width())//2
                for digit in Digits:
                    Screen.blit(Game_Images['numbers'][digit],(xoffset,ScreenHeight*0.4))
                    xoffset += Game_Images['numbers'][digit].get_width()
                pygame.display.update()
                FPSClock.tick(FPS)
                score = 0
def extraScreen():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and event.key == K_SPACE:
                return GameOver()
            else:
                Screen.blit(Game_Images['background'],(0,0))
                pygame.display.update()
                FPSClock.tick(FPS)


if __name__ == "__main__":
    pygame.init() #initialize pygame modules
    FPSClock = pygame.time.Clock()
    pygame.display.set_caption("Flappy Bird")
    Game_Images['player'] = pygame.image.load(player).convert_alpha()
    Game_Images['dead'] =pygame.image.load('gallery/images/deadBird.png').convert_alpha()
    Game_Images['game'] =pygame.image.load('gallery/images/game.png').convert_alpha()
    
    Game_Images['numbers'] = (
        pygame.image.load('gallery/images/zero.png').convert_alpha(),
        pygame.image.load('gallery/images/one.png').convert_alpha(),
        pygame.image.load('gallery/images/two.png').convert_alpha(),
        pygame.image.load('gallery/images/three.png').convert_alpha(),
        pygame.image.load('gallery/images/four.png').convert_alpha(),
        pygame.image.load('gallery/images/five.png').convert_alpha(),
        pygame.image.load('gallery/images/six.png').convert_alpha(),
        pygame.image.load('gallery/images/seven.png').convert_alpha(),
        pygame.image.load('gallery/images/eight.png').convert_alpha(),
        pygame.image.load('gallery/images/nine.png').convert_alpha()
    )
    Game_Images['background'] = pygame.image.load(Background).convert()
    Game_Images['message'] = pygame.image.load('gallery/images/message.png').convert_alpha()
    Game_Images['base'] = pygame.image.load('gallery/images/base.png').convert_alpha()
    Game_Images['pipe'] = (
        pygame.transform.rotate(pygame.image.load(Pipe), 180).convert_alpha(),
        pygame.image.load(Pipe).convert_alpha()
    )
    Game_Sounds['die'] = pygame.mixer.Sound('gallery/sounds/die.wav')
    Game_Sounds['hit'] = pygame.mixer.Sound('gallery/sounds/hit.wav')
    Game_Sounds['point'] = pygame.mixer.Sound('gallery/sounds/point.wav')
    Game_Sounds['swoosh'] = pygame.mixer.Sound('gallery/sounds/swoosh.wav')
    Game_Sounds['wing'] = pygame.mixer.Sound('gallery/sounds/wing.wav')

    # GAME LOOP
    
    welcomeScreen()