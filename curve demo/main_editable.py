import pygame
import gc
#import time
import math
#import dis
#from line_profiler import LineProfiler
##import numpy
import cProfile

#pygame initialization
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
clock = pygame.time.Clock()
fps = str(int(clock.get_fps()))





#screen title
pygame.display.set_caption('BREAKNEK')

# Util Class 
# Globvar Class
class Globvar():
    
    #global constants and variables
    PI = 3.14
    lead_x = display_width/2
    lead_y = display_height/2
#    segments = []
    Color = {'Light' : {'road': (136, 136, 136), 'grass':(66,147,82), 'rumble':(184,49,46)},
             'Dark'  : {'road': (102, 102, 102), 'grass':(57,125,70), 'rumble':(221,221,221), 'lane':(255,255,255)}
                 }
    ROAD = {
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
##    segments = [x for x in range(no_segments)]
    road_width = 1000
    seg_length = 100
    camera_depth = 0.84
    rumble_length = 3
    gameDisplay = pygame.display.set_mode((display_width, display_height), pygame.FULLSCREEN)
##    gameDisplay.fill(blue)
    image = pygame.image.load('images\\CAR1.png').convert_alpha()
    image = pygame.transform.scale(image, (round(display_width*0.366),round(display_width*0.366)))
    background = pygame.image.load('images\\green bkg2.png').convert_alpha()
    background = pygame.transform.scale(background, (display_width, round(display_height/2 )))
    gameDisplay.blit(background, (0, 0))
    distToPlane = None
    player_x = 0
    player_z = 0.0
    sprites = []
    cos_beta = math.cos(math.radians(0))
    x = 0
    z = 0
    speed = 0
    
    player_flag_z = None
    player_flag_x = None
    road_length = None
    
# Circuit Class
class Circuit(Globvar):
    
    def __init__(self):
        self.total_segments = None
##        self.road_length = None
        self.visible_segments = 200
        self.rumble_segments = 5
        self.road_lanes = 3
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
    def create(self,curve):
        Globvar.segments = []
##        global segments
        self.createRoad(curve)

        # colorize first last segment
##        for n in range(1):
##            Globvar.segments[n]['color']['road'] = (255,255,255)
##            Globvar.segments[len(Globvar.segments)-1-n]['color']['road'] = (34,34,34)
##        if Globvar.segments[0]['index']== 0 :
##            Globvar.segments[0]['color']['road'] = (255,255,255)

##        if Globvar.segments[1]['index']== 1 :
##            Globvar.segments[1]['color']['road'] = (255,255,255)
##
##        if Globvar.segments[2]['index']== 2 :
##            Globvar.segments[2]['color']['road'] = (255,255,255)
##
##        if Globvar.segments[3]['index']== 3 :
##            Globvar.segments[3]['color']['road'] = (255,255,255)
##
##        if Globvar.segments[4]['index']== 4 :
##            Globvar.segments[4]['color']['road'] = (255,255,255)

##        print(Globvar.segments)

        self.total_segments = len(Globvar.segments)
        Globvar.road_length = self.total_segments * Globvar.seg_length
##        print(self.road_length)
    

    def createRoad(self,curve):
        self.createSection(500, curve)

    def createSection(self, no_segments, curve):
        for i in range(no_segments):
            self.createSegment(curve)

##    def createSection(self):
####        Globvar.segments = [x for x in range(no_segments)]
####        print(Globvar.segments)
##        Globvar.segments = [{'index': x,
##             'point': { 'world': {'x': 0, 'y': 0, 'z': x* Globvar.seg_length},
##                        'scale': -1,
##                        'screen': {'x': 0, 'y': 0, 'w': 0}
##                        },
##             'color': Globvar.Color['Dark'] if math.floor(x/self.rumble_segments)%2 else Globvar.Color['Light']
##             } for x in range(len(Globvar.segments)) ]
        



    def createSegment(self, curve):
##        Color = {'Light' : {'road': (136, 136, 136), 'grass':(66,147,82)},
##             'Dark'  : {'road': (102, 102, 102), 'grass':(57,125,70)}
##                 }
        n = len(Globvar.segments)
##        print(n)
        self.segments.append(
            {'index': n,
             'point': { 'world': {'x': 0, 'y': 0, 'z': n* Globvar.seg_length },
                        'scale': -1,
                        'screen': {'x': 0, 'y': 0, 'w': 0}
                        },
             'curve':curve,   
             'color': Globvar.Color['Dark'] if math.floor(n/self.rumble_segments)%2 else Globvar.Color['Light']
             }
            )
        
    def addRoad(self,enter, hold, leave, curve):
        for n in range(int(enter)):
            self.create(self.easeIn(0, curve, n/enter))
        for n in range(int(hold)):
            self.create(curve)
        for n in range(int(leave)):
            self.create(self.easeInOut(curve, 0, n/leave))

    def addStraight(self,num):
        num = num or Globvar.ROAD['LENGTH']['MEDIUM']
        self.addRoad(num, num, num, 0)

    def addCurve(self,num, curve):
        num    = num or Globvar.ROAD['LENGTH']['MEDIUM']
        curve  = curve or Globvar.ROAD['CURVE']['MEDIUM']
        self.addRoad(num, num, num, curve)
    

    def addSCurves(self):
        self.addRoad(Globvar.ROAD['LENGTH']['MEDIUM'], Globvar.ROAD['LENGTH']['MEDIUM'], Globvar.ROAD['LENGTH']['MEDIUM'],  -Globvar.ROAD['CURVE']['MEDIUM'])
##        self.addRoad(Globvar.ROAD['LENGTH']['MEDIUM'], Globvar.ROAD['LENGTH']['MEDIUM'], Globvar.ROAD['LENGTH']['MEDIUM'],   Globvar.ROAD['CURVE']['MEDIUM'])
##        self.addRoad(Globvar.ROAD['LENGTH']['MEDIUM'], Globvar.ROAD['LENGTH']['MEDIUM'], Globvar.ROAD['LENGTH']['MEDIUM'],   Globvar.ROAD['CURVE']['EASY'])
##        self.addRoad(Globvar.ROAD['LENGTH']['MEDIUM'], Globvar.ROAD['LENGTH']['MEDIUM'], Globvar.ROAD['LENGTH']['MEDIUM'],  -Globvar.ROAD['CURVE']['EASY'])
##        self.addRoad(Globvar.ROAD['LENGTH']['MEDIUM'], Globvar.ROAD['LENGTH']['MEDIUM'], Globvar.ROAD['LENGTH']['MEDIUM'],  -Globvar.ROAD['CURVE']['MEDIUM'])

    def resetRoad(self):
        Globvar.segments = []
        self.addStraight(Globvar.ROAD['LENGTH']['SHORT']/4)
        self.addSCurves()
##        self.addStraight(Globvar.ROAD['LENGTH']['LONG'])
##        self.addCurve(Globvar.ROAD['LENGTH']['MEDIUM'], Globvar.ROAD['CURVE']['MEDIUM'])
##        self.addCurve(Globvar.ROAD['LENGTH']['LONG'], Globvar.ROAD['CURVE']['MEDIUM'])
##        
##        self.addSCurves()
##        self.addCurve(Globvar.ROAD['LENGTH']['LONG'], -Globvar.ROAD['CURVE']['MEDIUM'])
##        self.addCurve(Globvar.ROAD['LENGTH']['LONG'], Globvar.ROAD['CURVE']['MEDIUM'])
##        
##        self.addSCurves()
##        self.addCurve(Globvar.ROAD['LENGTH']['LONG'], -Globvar.ROAD['CURVE']['EASY'])


        
    

    
    
    def getSegment(self, positionZ):
##        print(positionZ)
        if (positionZ<0):
            positionZ += Globvar.road_length
##        print(Globvar.segments)    
##        if (self.total_segments <= 0):
##            self.total_segments = 1
##        print(self.total_segments)
        index = math.floor(positionZ / Globvar.seg_length)% self.total_segments
#        print('getsegment',Globvar.segments[index])
        return Globvar.segments[index]    
        
    def project3d(self, point, cameraX, cameraY, cameraZ, cameraDepth):
        transX = point['world']['x'] - cameraX
        transY = point['world']['y'] - cameraY
        transZ = point['world']['z'] - cameraZ

##        if transZ == 0 :
##            transZ += 1
##        print(cameraZ)
##        print(transZ)
##        print(point['world']['z'])

        point['scale'] = cameraDepth/transZ

        projectedX = point['scale'] * transX
        projectedY = point['scale'] * transY
        projectedW = point['scale'] * Globvar.road_width
        
        point['screen']['x'] = round((1 + projectedX) * Globvar.lead_x)
        point['screen']['y'] = round((1 - projectedY) * Globvar.lead_y)
        point['screen']['w'] = round(projectedW * Globvar.lead_x)
        
    def render3d(self):
        
        clip_bottom_line = display_height
##        print('r3d',self.getSegment(Globvar.z))
##        print(Globvar.z)
##        if Globvar.z == 19603.0 :
##            Globvar.z = 19597.0
        base_segment = self.getSegment(Globvar.z)
##        print('r3d base_segment',base_segment['index'])

        base_percent = self.percentageRemaining(Globvar.z, Globvar.seg_length)
        dx = - (base_segment['curve'] * base_percent)
        x = 0

        base_index = base_segment['index']
        
        for n in range(self.visible_segments):
            current_index = (base_index + n)% self.total_segments
##            print('r3d current_index',current_index)
            current_segment = Globvar.segments[current_index]
##            print('current_segment',current_segment)
##            print('Globvar.z',Globvar.z)

            offset_z =  Globvar.road_length if current_index < base_index else 0
##            print(Globvar.x)
            self.project3d(current_segment['point'], Globvar.x - x - dx, Camera.y, Globvar.z - offset_z, Globvar.distToPlane)

            x = x + dx
            dx = dx + current_segment['curve']
            curr_bottom_line = current_segment['point']['screen']['y']
##            print('curr_bottom_line ',curr_bottom_line)
            if n>0 and curr_bottom_line < clip_bottom_line:
                previous_index = current_index - 1 if (current_index > 0) else self.total_segments -1
##                print('r3d previous_index',previous_index)
                previous_segment = Globvar.segments[previous_index]
##                print(previous_segment['point'])
##                self.project3d(previous_segment['point'], Camera.x - x , Camera.y, Globvar.z - offset_z, Globvar.distToPlane)
                p1 = previous_segment['point']['screen']
                
                p2 = current_segment['point']['screen']
                

                
##                print('drawseg called')
                self.drawSeg(current_segment['color'],
                      p1['x'],
                      p1['y'],
                      p1['w'],
                      p2['x'],
                      p2['y'],
                      p2['w'])

                clip_bottom_line = curr_bottom_line
            


##                print('current_segment',current_segment)
##                print('previous_segment',previous_segment)

    def drawSeg(self, color, x1, y1, w1, x2, y2, w2):
##        print('x1',x1)
##        print('y1',y1)
##        print('w1',w1)
##        print('x2',x2)
##        print('y2',y2)
##        print('w2',w2)

    ##  a = ((x1-w1, y1), (x2-w2, y2), (x2+w2, y2), (x1+w1, y1))
        #grass
        pygame.draw.rect(Globvar.gameDisplay, color['grass'], (0, y2, display_width, y1-y2) )
        #road
        pygame.draw.polygon(Globvar.gameDisplay, color['road'], ((x1-w1, y1), (x1+w1, y1), (x2+w2, y2), (x2-w2, y2) ))
        #rumble strips
        rumble_width1 = w1/5
        rumble_width2 = w2/5
        pygame.draw.polygon(Globvar.gameDisplay, color['rumble'], ((x1-w1-rumble_width1, y1), (x1-w1, y1), (x2-w2, y2), (x2-w2-rumble_width2, y2)))
        pygame.draw.polygon(Globvar.gameDisplay, color['rumble'], ((x1+w1+rumble_width1, y1), (x1+w1, y1), (x2+w2, y2), (x2+w2+rumble_width2, y2)))
        # lanes
        if color.get('lane') is not None:
            line_w1 = (w1/20)/2
            line_w2 = (w2/20)/2
            lane_w1 = (w1*2)/self.road_lanes
            lane_w2 = (w2*2)/self.road_lanes

            lane_x1 = x1 - w1
            lane_x2 = x2 - w2

            for i in range(1,self.road_lanes):
                lane_x1 += lane_w1
                lane_x2 += lane_w2

                pygame.draw.polygon(Globvar.gameDisplay, color['lane'], ((lane_x1-line_w1, y1), (lane_x1+line_w1, y1), (lane_x2+line_w2, y2), (lane_x2-line_w2, y2)))


# Camera class
class Camera:
    
        
##  update x to get control motion
    Globvar.x=0 
    y = 1000
    

    distToPlayer = 500


    def init(self):
        
##        global distToPlane
##        if (Globvar.distToPlane == None):
        Globvar.distToPlane = 1/(self.y / self.distToPlayer)
            


    def update(self):
        Globvar.x = Globvar.player_x * Globvar.road_width
        
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
##        print(self.max_speed)
        

    def restart(self):
        Globvar.player_x = 0
        self.y = 0
        Globvar.player_z = 0

        Globvar.speed = self.max_speed 
##        Globvar.player_z = Globvar.speed * 0.0016

    def update(self, dt):
        # speed changes according to player inputs
##        Globvar.player_x = Globvar.player_x + 10 if Globvar.player_flag_x == True else 0 
##        print(Globvar.player_x)
        Globvar.speed = self.max_speed if Globvar.player_flag_z == True else 0
##        print(dt)
##        print(Globvar.speed)
##        Globvar.player_z = (Globvar.player_z + Globvar.speed * dt) if Globvar.player_flag == True else  Globvar.speed *dt
        Globvar.player_z += Globvar.speed * dt
##        print('Globvar.player_z',Globvar.player_z)
##        print('Globvar.z',Globvar.z)
        if (Globvar.player_z >= Globvar.road_length):
            print("last_seg")
            Globvar.player_z -= Globvar.road_length
                    
                    
        
        
                    
        
        
        
##        if Globvar.player_z >= Globvar.road_length:
##            Globvar.player_z -= Globvar.road_length


all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)        
        

camera_object = Camera()
player_object = Player()
circuit_object = Circuit()
##camera_object.init()
##circuit_object.create()
####print(len(Globvar.segments))
player_object.restart()
##all_sprites.update()
def gameLoop():
    gameExit = False
    gameOver = False

    while not gameExit:

            
            
                    
                    
##                    Globvar.player_flag = True
##                else:
##                    Globvar.player_flag = False
                    
##                    Globvar.player_z += Globvar.speed * dt
        ####        print(len(Globvar.segments))
##        print(clock_tick/1000)
        camera_object.init()
            
##        print(Globvar.distToPlane)
        circuit_object.addSCurves()
##      print(len(Globvar.segments))
##        player_object.restart()
        clock_tick = clock.tick(60)
        dt = min(1, clock_tick/1000)
##        Globvar.player_z = Globvar.speed * dt
        

        
##        Globvar.dt_for_player = dt

        player_object.update(dt)
##        print(Globvar.z)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    Globvar.player_flag_z = True
##                    Globvar.player_z = Globvar.player_z + Globvar.speed * dt 
                    
                
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    Globvar.player_flag_z = False


            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    Globvar.x += 10

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    Globvar.x = 0

##            elif event.type == pygame.KEYDOWN:
##                if event.key == pygame.K_LEFT:
##                    Globvar.player_flag_x = True
##
##            elif event.type == pygame.KEYUP:
##                if event.key == pygame.K_LEFT:
##                    Globvar.player_flag_x = False
            
##                    Globvar.player_z = Globvar.player_z
                    
            
##        for event in pygame.event.get():
##            if event.type == pygame.KEYDOWN:
##                if event.key == pygame.K_UP:
##        player_object.update(dt)
##            
        camera_object.update()
##        print(Globvar.segments)
        circuit_object.render3d()
        all_sprites.draw(Globvar.gameDisplay)
        
        pygame.draw.rect(Globvar.gameDisplay, Globvar.black, (0, 0, 25, 20) )
        Globvar.gameDisplay.blit(update_fps(), (0,0))
        
        
       
        
        pygame.display.update()
        clock.tick(FPS)
##        print(clock.tick(FPS))
##        print(clock.get_fps())
##        gc.collect()
##        gameExit = True
    pygame.quit()
    quit()


##gameLoop()
##dis.dis(gameLoop)
#lp = LineProfiler()
#lp_wrapper = lp(gameLoop)
#lp.print_stats()
cProfile.run('gameLoop()')


