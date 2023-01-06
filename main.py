import pygame
import sys
import gc

import math
import json

##pygame initialization
pygame.init()


# display res
display_width = 1366
display_height = 768

##fps meter
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 18)
def update_fps():
    fps = str(int(clock.get_fps()))
    fps_text = font.render(fps, 1, pygame.Color("coral"))
    return fps_text


#frames per second
FPS = 60

#timer
main_clock = pygame.time.Clock()
fps = str(int(clock.get_fps()))





#screen title
pygame.display.set_caption('BREAKNEK')

# Globvar Class
class Globvar():
    
    #global constants and variables
    PI = 3.14
    lead_x = display_width/2
    lead_y = display_height/2
    Color = {'Light' : {'Level_1':{'road': (136, 136, 136), 'grass':(66,147,82), 'rumble':(184,49,46)},
                        'Level_2':{'road': (136, 136, 136), 'grass':(194,178,128), 'rumble':(184,49,46)}},
             'Dark'  : {'Level_1':{'road': (102, 102, 102), 'grass':(57,125,70), 'rumble':(221,221,221), 'lane':(255,255,255)},
                        'Level_2':{'road': (102, 102, 102), 'grass':(168,143,89), 'rumble':(221,221,221), 'lane':(255,255,255)}
            }}
            
    Road = {
          'LENGTH': { 'NONE': 0, 'SHORT':  25, 'MEDIUM':  50, 'LONG':  100 },
          'CURVE':  { 'NONE': 0, 'EASY':    2, 'MEDIUM':   4, 'HARD':    6 }
            }
    red = (255, 0, 0)
    green = (0, 255, 0)
    blue = (135,206,235)
    black = (0, 0, 0)
    white = (255, 255, 255)
    grey = (128,128,128)
    no_segments = 1000
    segments = []
    road_width = 1000
    seg_length = 100
    camera_depth = 0.84
    rumble_length = 3
    font_name = "font\\8-BIT WONDER.TTF"
    display = pygame.Surface((display_width, display_height))
    menuDisplay = pygame.display.set_mode((display_width, display_height),pygame.FULLSCREEN)
    resolution = ((1366,768),(1280,720),(800,600),(640,480))
    gameDisplay = pygame.display.set_mode(resolution[0],pygame.FULLSCREEN)
    image = pygame.image.load('images\\CAR1.png').convert_alpha()
    image = pygame.transform.scale(image, (round(display_width*0.366),round(display_width*0.366)))
    image2 = pygame.image.load('images\\CAR2.png').convert_alpha()
    image2 = pygame.transform.scale(image2, (round(display_width*0.366),round(display_width*0.366)))
    logo = pygame.image.load('images\\LOGO.png').convert_alpha()
    logo = pygame.transform.scale(logo, (511,287))
    background = pygame.image.load('images\\green bkg2.png').convert_alpha()
    background = pygame.transform.scale(background, (display_width, round(display_height/2+10)))
    background2 = pygame.image.load('images\\background.png').convert_alpha()
    background2 = pygame.transform.scale(background2, (display_width, round(display_height/2+10)))
    menu_image = pygame.image.load("images\\istockphoto-1251454383-612x612 (2).jpg")
    menu_image = pygame.transform.scale(menu_image, (display_width, display_height))
    gameDisplay.blit(background, (0, 0))
    road_lanes = 3
    distToPlane = None
    player_x = 0
    player_z = 0.0
    sprites = []
    x = 0
    dx_l = -100
    dx_r = 100
    z = 0
    speed = 0
    player_flag_z = None
    player_flag_x_l= None
    player_flag_x_r= None

    road_length = None
    click = False
    click_1 = False
    click_2 = False
    click_3 = False

def drawText(text, size, color, surface, x, y):
    font = pygame.font.Font(Globvar.font_name,size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.topleft = (x,y)
    surface.blit(text_surface,text_rect)

click = False
def mainMenu():
    while True:

        Globvar.menuDisplay.fill((0,0,0))
        Globvar.menuDisplay.blit(Globvar.menu_image , (0,0))
        Globvar.menuDisplay.blit(Globvar.logo, (363, 40))
        drawText("Main Menu", 30, (255,255,255), Globvar.menuDisplay, 20, 20)
        
        
        mx,my = pygame.mouse.get_pos()
        
        button_1 = pygame.Rect(50,100,200,50)
        button_2 = pygame.Rect(50,200,200,50)
        button_3 = pygame.Rect(50,300,200,50)
        button_4 = pygame.Rect(50,400,200,50)
        if button_1.collidepoint((mx,my)):
            if Globvar.click :
                levelSelector()
        if button_2.collidepoint((mx,my)):
            if Globvar.click :
                options()
        if button_3.collidepoint((mx,my)):
            if Globvar.click :
                log()
        if button_4.collidepoint((mx,my)):
            if Globvar.click:
                pygame.quit()
                sys.exit()
                
                
        pygame.draw.rect(Globvar.menuDisplay,(0, 0, 150), button_1)
        drawText("Play Game", 20, (255,255,255), Globvar.menuDisplay, 62, 113)
        
        pygame.draw.rect(Globvar.menuDisplay,(0, 0, 150), button_2)
        drawText("Options", 20, (255,255,255), Globvar.menuDisplay, 85, 213)

        pygame.draw.rect(Globvar.menuDisplay,(0, 0, 150), button_3)
        drawText("Login", 20, (255,255,255), Globvar.menuDisplay, 105, 313)
        
        pygame.draw.rect(Globvar.menuDisplay,(0, 0, 150), button_4)
        drawText("quit", 20, (255,255,255), Globvar.menuDisplay, 110, 413)
        Globvar.click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    Globvar.click = True
        pygame.display.update()
        main_clock.tick(60)

def options():
    running = True
    while running:
        Globvar.menuDisplay.blit(Globvar.menu_image , (0,0))
        drawText("Options" , 20, (255,255,255), Globvar.menuDisplay, 20, 20)
        mx,my = pygame.mouse.get_pos()
        
        button_1 = pygame.Rect(50,100,200,50)
        button_2 = pygame.Rect(50,200,200,50)
        button_3 = pygame.Rect(50,300,200,50)
        button_4 = pygame.Rect(50,400,200,50)

        
        
        if button_1.collidepoint((mx,my)):
            if Globvar.click_2 :
                Globvar.gameDisplay = pygame.display.set_mode(Globvar.resolution[0],pygame.FULLSCREEN)
                
        if button_2.collidepoint((mx,my)):
            if Globvar.click_2 :
                Globvar.gameDisplay = pygame.display.set_mode(Globvar.resolution[0],pygame.FULLSCREEN)
                Globvar.gameDisplay = pygame.display.set_mode(Globvar.resolution[1],pygame.FULLSCREEN)

        if button_3.collidepoint((mx,my)):
            if Globvar.click_2 :
                Globvar.gameDisplay = pygame.display.set_mode(Globvar.resolution[0],pygame.FULLSCREEN)
                Globvar.gameDisplay = pygame.display.set_mode(Globvar.resolution[2],pygame.FULLSCREEN)
        if button_4.collidepoint((mx,my)):
            if Globvar.click_2:
                Globvar.gameDisplay = pygame.display.set_mode(Globvar.resolution[0],pygame.FULLSCREEN)
                Globvar.gameDisplay = pygame.display.set_mode(Globvar.resolution[3],pygame.FULLSCREEN)
                

        pygame.draw.rect(Globvar.menuDisplay,(0, 0, 150), button_1)
        drawText("1366 x 768", 20, (255,255,255), Globvar.menuDisplay, 65, 113)
        
        pygame.draw.rect(Globvar.menuDisplay,(0, 0, 150), button_2)
        drawText("1280 x 720", 20, (255,255,255), Globvar.menuDisplay, 65, 213)

        pygame.draw.rect(Globvar.menuDisplay,(0, 0, 150), button_3)
        drawText("800 x 600", 20, (255,255,255), Globvar.menuDisplay, 75, 313)
        
        pygame.draw.rect(Globvar.menuDisplay,(0, 0, 150), button_4)
        drawText("640 x 480", 20, (255,255,255), Globvar.menuDisplay, 75, 413)
        Globvar.click_2 = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    Globvar.click_2 = True
        pygame.display.update()
        main_clock.tick(60)
        

    
def save(save):
    with open("data\\Player_Log.txt")as file:
        data = file.read()
    json_load = json.loads(data)
    n = len(json_load)
    search_name = save

    def found():
        for i in range(n):
            if (json_load[i]["Name"] == search_name ):
                return(True)
                
    def not_found():
        data1 = {"Name":search_name, "Score":1000000}
        json_load.append(data1)
        with open("data\\Player_Log.txt","w")as file1:
            file1.write(json.dumps(json_load))
        print("New Username Created")
            
    if found() == True:
        print("Old User")
    else:
        not_found()
    

def log():
    
    running = True
    while running:
        user_text = ''
        base_font = pygame.font.Font(None, 32)
        Globvar.menuDisplay.blit(Globvar.menu_image , (0,0))
        drawText("Put Username" , 30, (255,255,255), Globvar.menuDisplay, 20, 20)
 
        active = False
                
        while True and running:
            mx,my = pygame.mouse.get_pos()

            button_1 = pygame.Rect(300, 300, 140, 32)
            if button_1.collidepoint((mx,my)):
                if Globvar.click_3 :
                    save(user_text)
                    

            pygame.draw.rect(Globvar.menuDisplay,(0, 0, 150), button_1)
            drawText("enter", 20, (255,255,255), Globvar.menuDisplay, 322, 305)
            input_rect = pygame.Rect(200, 200, 140, 32)
  
# color_active stores color(lightskyblue3) which
# gets active when input box is clicked by user
            color_active = pygame.Color('lightskyblue3')
  
# color_passive store color(chartreuse4) which is
# color of input box.
            color_passive = pygame.Color('chartreuse4')
            color = color_passive
            Globvar.click_3 = False

            for event in pygame.event.get():
  
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    if event.key == pygame.K_KP_ENTER:
                        running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        Globvar.click_3 = True
                
                if event.type == pygame.MOUSEBUTTONDOWN:                    
                    if input_rect.collidepoint(event.pos):
                        active = True
                    else:
                        active = False

                    if event.button == 1:
                        Globvar.click_3 = True
  
                if event.type == pygame.KEYDOWN:
  
            # Check for backspace
                    if event.key == pygame.K_BACKSPACE:
  
                # get text input from 0 to -1 i.e. end.
                        user_text = user_text[:-1]
  
            # Unicode standard is used for string
            # formation
                    elif event.unicode.isalpha():
                        
                        
                        user_text += event.unicode
      
    # it will set background color of screen
            
  
            if active:
                color = color_active
            else:
                color = color_passive
          
    # draw rectangle and argument passed which should
    # be on screen
            pygame.draw.rect(Globvar.menuDisplay, color, input_rect)
  
            text_surface = base_font.render(user_text, True, (255, 255, 255))
      
    # render at position stated in arguments
            Globvar.menuDisplay.blit(text_surface, (input_rect.x+5, input_rect.y+5))
      
    # set width of textfield so that text cannot get
    # outside of user's text input
            input_rect.w = max(100, text_surface.get_width()+10)
    # display.flip() will update only a portion of the
    # screen to updated, not full area
            pygame.display.flip()
            clock.tick(60)
##    print(user_text)  
    # clock.tick(60) means that for every second at most 60 frames should be passed.
            

def levelSelector():
    running = True
    while running:
        Globvar.menuDisplay.blit(Globvar.menu_image , (0,0))
        drawText("Level Selector", 20, (255,255,255), Globvar.menuDisplay, 20, 20)
        mx,my = pygame.mouse.get_pos()
        button_3 = pygame.Rect(50,100,200,50)
        button_4 = pygame.Rect(50,200,200,50)
        
        if button_3.collidepoint((mx,my)):
                if Globvar.click_1 :
                    gc.collect()
                    gameLoop_1()
        if button_4.collidepoint((mx,my)):
                if Globvar.click_1 :
                    gc.collect()
                    gameLoop_2()

        pygame.draw.rect(Globvar.menuDisplay,(0, 0, 150), button_3)
        drawText("LEVEL 1", 20, (255,255,255), Globvar.menuDisplay, 85, 113)
        
        pygame.draw.rect(Globvar.menuDisplay,(0, 0, 150), button_4)
        drawText("LEVEL 2", 20, (255,255,255), Globvar.menuDisplay, 85, 213)
        Globvar.click_1 = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    Globvar.click_1 = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            
        pygame.display.update()
        

# Circuit Class
class Circuit(Globvar):
    
    
    def __init__(self):
        self.total_segments = None
        self.visible_segments = 200
        self.rumble_segments = 5
        
    def create(self):
        Globvar.segments = []
        self.createRoad()


        self.total_segments = len(Globvar.segments)
        Globvar.road_length = self.total_segments * Globvar.seg_length
    

    def createRoad(self):
        self.createSection(200)

    def createSection(self, no_segments):
        for i in range(no_segments):
            self.createSegment()




    def createSegment(self):
        n = len(Globvar.segments)
        self.segments.append(
            {'index': n,
             'point': { 'world': {'x': 0, 'y': 0, 'z': n* Globvar.seg_length },
                        'scale': -1,
                        'screen': {'x': 0, 'y': 0, 'w': 0}
                        },
             'color': Globvar.Color['Dark'] if math.floor(n/self.rumble_segments)%2 else Globvar.Color['Light']
             }
            )
        

    
    

    
    
    def getSegment(self, positionZ):
        if (positionZ<0):
            positionZ += Globvar.road_length
        index = math.floor(positionZ / Globvar.seg_length)% self.total_segments
        return Globvar.segments[index]    
        
    def project3d(self, point, cameraX, cameraY, cameraZ, cameraDepth):
        transX = point['world']['x'] - cameraX
        transY = point['world']['y'] - cameraY
        transZ = point['world']['z'] - cameraZ


        point['scale'] = cameraDepth/transZ

        projectedX = point['scale'] * transX
        projectedY = point['scale'] * transY
        projectedW = point['scale'] * Globvar.road_width
        
        point['screen']['x'] = round((1 + projectedX) * Globvar.lead_x)
        point['screen']['y'] = round((1 - projectedY) * Globvar.lead_y)
        point['screen']['w'] = round(projectedW * Globvar.lead_x)
        
    def render3d(self):
        
        clip_bottom_line = display_height
        if Globvar.z == 19603.0 :
            Globvar.z = 19597.0
        base_segment = self.getSegment(Globvar.z)
        base_index = base_segment['index']
        
        for n in range(self.visible_segments):
            current_index = (base_index + n)% self.total_segments
            current_segment = Globvar.segments[current_index]

                
            
            offset_z =  Globvar.road_length if current_index < base_index else 0              
            self.project3d(current_segment['point'], Globvar.x, Camera.y, Globvar.z - offset_z, Globvar.distToPlane)

            curr_bottom_line = current_segment['point']['screen']['y']
            if n>0 and curr_bottom_line < clip_bottom_line:
                previous_index = current_index - 1 if (current_index > 0) else self.total_segments -1
                previous_segment = Globvar.segments[previous_index]
                p1 = previous_segment['point']['screen']
                
                p2 = current_segment['point']['screen']
                self.drawSeg(current_segment['color'],
                      p1['x'],
                      p1['y'],
                      p1['w'],
                      p2['x'],
                      p2['y'],
                      p2['w'])

                clip_bottom_line = curr_bottom_line



    def drawSeg(self, color, x1, y1, w1, x2, y2, w2):
        #grass
        pygame.draw.rect(Globvar.gameDisplay, color['Level_1']['grass'], (0, y2, display_width, y1-y2) )
        #road
        pygame.draw.polygon(Globvar.gameDisplay, color['Level_1']['road'], ((x1-w1, y1), (x1+w1, y1), (x2+w2, y2), (x2-w2, y2) ))
        #rumble strips
        rumble_width1 = w1/5
        rumble_width2 = w2/5
        pygame.draw.polygon(Globvar.gameDisplay, color['Level_1']['rumble'], ((x1-w1-rumble_width1, y1), (x1-w1, y1), (x2-w2, y2), (x2-w2-rumble_width2, y2)))
        pygame.draw.polygon(Globvar.gameDisplay, color['Level_1']['rumble'], ((x1+w1+rumble_width1, y1), (x1+w1, y1), (x2+w2, y2), (x2+w2+rumble_width2, y2)))
        # lanes
        if color['Level_1'].get('lane') is not None:
            line_w1 = (w1/20)/2
            line_w2 = (w2/20)/2
            lane_w1 = (w1*2)/Globvar.road_lanes
            lane_w2 = (w2*2)/Globvar.road_lanes

            lane_x1 = x1 - w1
            lane_x2 = x2 - w2

            for i in range(1,Globvar.road_lanes):
                lane_x1 += lane_w1
                lane_x2 += lane_w2

                pygame.draw.polygon(Globvar.gameDisplay, color['Level_1']['lane'], ((lane_x1-line_w1, y1), (lane_x1+line_w1, y1), (lane_x2+line_w2, y2), (lane_x2-line_w2, y2)))
        
class Circuit_2(Globvar):
    
    
    def __init__(self):
        self.total_segments = None
        self.visible_segments = 200
        self.rumble_segments = 5
        
#util starts

    def accelerate(self,v,accel,dt):
        return v+(accel * dt)

    def easeIn(self,a,b,percent):
        return a+ (b-a)* pow(percent,2)

    def easeOut(self,a,b,percent):
        return a + (b-a)*(1.0-pow(1-percent,2))

    def easeInOut(self,a,b,percent):
        cosV=(percent*Globvar.PI)*(180.0/Globvar.PI)
        v = a + (b-a)*((-math.cos(cosV)/2.0) + 0.5)
        return v

    def percentageRemaining(self,n,total):
        return math.fmod(n,total)/total

# util ends
    def create(self):
        Globvar.segments = []
        self.createRoad()


        self.total_segments = len(Globvar.segments)
        Globvar.road_length = self.total_segments * Globvar.seg_length
    

    def createRoad(self):
        self.createSection(200)

    def createSection(self, no_segments):
        for i in range(no_segments):
            self.createSegment()

        



    def createSegment(self):
        n = len(Globvar.segments)
        self.segments.append(
            {'index': n,
             'point': { 'world': {'x': 0, 'y': 0, 'z': n* Globvar.seg_length },
                        'scale': -1,
                        'screen': {'x': 0, 'y': 0, 'w': 0}
                        },
             'color': Globvar.Color['Dark'] if math.floor(n/self.rumble_segments)%2 else Globvar.Color['Light']
             }
            )
        

    
    

    
    
    def getSegment(self, positionZ):
        if (positionZ<0):
            positionZ += Globvar.road_length
        index = math.floor(positionZ / Globvar.seg_length)% self.total_segments
        return Globvar.segments[index]    
        
    def project3d(self, point, cameraX, cameraY, cameraZ, cameraDepth):
        transX = point['world']['x'] - cameraX
        transY = point['world']['y'] - cameraY
        transZ = point['world']['z'] - cameraZ


        point['scale'] = cameraDepth/transZ

        projectedX = point['scale'] * transX
        projectedY = point['scale'] * transY
        projectedW = point['scale'] * Globvar.road_width
        
        point['screen']['x'] = round((1 + projectedX) * Globvar.lead_x)
        point['screen']['y'] = round((1 - projectedY) * Globvar.lead_y)
        point['screen']['w'] = round(projectedW * Globvar.lead_x)
        
    def render3d(self):
        
        clip_bottom_line = display_height
        if Globvar.z == 19603.0 :
            Globvar.z = 19597.0
        base_segment = self.getSegment(Globvar.z)
        base_index = base_segment['index']
        
        for n in range(self.visible_segments):
            current_index = (base_index + n)% self.total_segments
            current_segment = Globvar.segments[current_index]

                
            
            offset_z =  Globvar.road_length if current_index < base_index else 0              
            self.project3d(current_segment['point'], Globvar.x, Camera.y, Globvar.z - offset_z, Globvar.distToPlane)

            curr_bottom_line = current_segment['point']['screen']['y']
            if n>0 and curr_bottom_line < clip_bottom_line:
                previous_index = current_index - 1 if (current_index > 0) else self.total_segments -1
                previous_segment = Globvar.segments[previous_index]
                p1 = previous_segment['point']['screen']
                
                p2 = current_segment['point']['screen']
                self.drawSeg(current_segment['color'],
                      p1['x'],
                      p1['y'],
                      p1['w'],
                      p2['x'],
                      p2['y'],
                      p2['w'])

                clip_bottom_line = curr_bottom_line



    def drawSeg(self, color, x1, y1, w1, x2, y2, w2):

        #grass
        pygame.draw.rect(Globvar.gameDisplay, color['Level_2']['grass'], (0, y2, display_width, y1-y2) )
        #road
        pygame.draw.polygon(Globvar.gameDisplay, color['Level_2']['road'], ((x1-w1, y1), (x1+w1, y1), (x2+w2, y2), (x2-w2, y2) ))
        #rumble strips
        rumble_width1 = w1/5
        rumble_width2 = w2/5
        pygame.draw.polygon(Globvar.gameDisplay, color['Level_2']['rumble'], ((x1-w1-rumble_width1, y1), (x1-w1, y1), (x2-w2, y2), (x2-w2-rumble_width2, y2)))
        pygame.draw.polygon(Globvar.gameDisplay, color['Level_2']['rumble'], ((x1+w1+rumble_width1, y1), (x1+w1, y1), (x2+w2, y2), (x2+w2+rumble_width2, y2)))
        # lanes
        if color['Level_2'].get('lane') is not None:
            line_w1 = (w1/20)/2
            line_w2 = (w2/20)/2
            lane_w1 = (w1*2)/Globvar.road_lanes
            lane_w2 = (w2*2)/Globvar.road_lanes

            lane_x1 = x1 - w1
            lane_x2 = x2 - w2

            for i in range(1,Globvar.road_lanes):
                lane_x1 += lane_w1
                lane_x2 += lane_w2

                pygame.draw.polygon(Globvar.gameDisplay, color['Level_2']['lane'], ((lane_x1-line_w1, y1), (lane_x1+line_w1, y1), (lane_x2+line_w2, y2), (lane_x2-line_w2, y2)))
        

# Camera class
class Camera:
    
        
        
    
    y = 1000
    

    distToPlayer = 500


    def init(self):
        
        Globvar.distToPlane = 1/(self.y / self.distToPlayer)
            


    def update(self):
        Globvar.x =  Globvar.x + Globvar.dx_l   if Globvar.player_flag_x_l == True and Globvar.x >= -850 else Globvar.x
        
        Globvar.x =  Globvar.x + Globvar.dx_r   if Globvar.player_flag_x_r == True and Globvar.x <= 850 else Globvar.x
        # added + 1 to avoid transZ == 0
        Globvar.z = Globvar.player_z  -self.distToPlayer + 1

        if (Globvar.z < 0 ) :
            Globvar.z += Globvar.road_length
            
            

# Player Class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = Globvar.image

        self.rect = self.image.get_rect()

        self.rect.center = (Globvar.lead_x - 26, ((15/20)*display_height))
        
        self.y = 0
        

        self.max_speed = (Globvar.seg_length)/(1/60)
        

    def restart(self):
        Globvar.player_x = 0
        self.y = 0
        Globvar.player_z = 0

        Globvar.speed = self.max_speed 

    def update(self, dt):
        # speed changes according to player inputs
        Globvar.speed = self.max_speed if Globvar.player_flag_z == True else 0
##        if Globvar.x >= 850:
##            Globvar.speed = 0
##        elif Globvar.x <= -850:
##            Globvar.speed = 0
            
        Globvar.player_z += Globvar.speed * dt
        if (Globvar.player_z >= Globvar.road_length):
            print("last_seg")
            Globvar.player_z -= Globvar.road_length
                    
                    
        
        
        

camera_object = Camera()
player_object = Player()
circuit_object = Circuit()
player_object.restart()

def gameLoop_1():
    running = True
    all_sprites = pygame.sprite.Group()
    player = Player()
    all_sprites.add(player)
    while running:
        
        gameExit = False
        gameOver = False

        while not gameExit:

            
            
                    
                    
            Globvar.gameDisplay.fill((0,0,0))
            Globvar.gameDisplay.blit(Globvar.background, (0, 0))
            camera_object.init()
            circuit_object.create()
            clock_tick = clock.tick(60)
            dt = min(1, clock_tick/1000)
        

        

            player_object.update(dt)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameExit = True
            
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        Globvar.player_flag_z = True
                    
                
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP:
                        Globvar.player_flag_z = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        Globvar.player_flag_x_l = True
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        Globvar.player_flag_x_l = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        Globvar.player_flag_x_r = True

                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_RIGHT:
                        Globvar.player_flag_x_r = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        pygame.quit()
                        quit()
                    
            camera_object.update()
            circuit_object.render3d()
            all_sprites.draw(Globvar.gameDisplay)
        
            pygame.draw.rect(Globvar.gameDisplay, Globvar.black, (0, 0, 25, 20) )
            Globvar.gameDisplay.blit(update_fps(), (0,0))
        
        
       
        
            pygame.display.update()
            clock.tick(FPS)
        pygame.quit()
        quit()

class Player2(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = Globvar.image2

        self.rect = self.image.get_rect()

        self.rect.center = (Globvar.lead_x - 26, ((15/20)*display_height))
        


circuit_object_2 = Circuit_2()
def gameLoop_2():
    gameExit = False
    gameOver = False
    all_sprites = pygame.sprite.Group()
    player = Player2()
    all_sprites.add(player)
    while not gameExit:

        Globvar.gameDisplay.fill((0,0,0))
        Globvar.gameDisplay.blit(Globvar.background2, (0, 0))
        camera_object.init()
        circuit_object_2.create()
        clock_tick = clock.tick(60)
        dt = min(1, clock_tick/1000)
                
        player_object.update(dt)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    Globvar.player_flag_z = True
                    
                
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    Globvar.player_flag_z = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    Globvar.player_flag_x_l = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    Globvar.player_flag_x_l = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    Globvar.player_flag_x_r = True

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    Globvar.player_flag_x_r = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                        pygame.quit()
                        quit()
                    
                    
                    
            
        camera_object.update()
        circuit_object_2.render3d()
        all_sprites.draw(Globvar.gameDisplay)
        
        pygame.draw.rect(Globvar.gameDisplay, Globvar.black, (0, 0, 25, 20) )
        Globvar.gameDisplay.blit(update_fps(), (0,0))
        
        
       
        
        pygame.display.update()
        clock.tick(FPS)
    pygame.quit()
    quit()



mainMenu()

