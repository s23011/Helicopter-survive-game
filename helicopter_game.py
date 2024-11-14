#標準モジュール
import random
import time
#インストールのモジュール
import pygame
from pygame.locals import *
from pygame import surface
#自分のモジュール
from character import Character2D
from common import (load_image,read_json,write_json
                    ,Vecter2
                    ,Window,Panel,Label)

#Constant Value
PX = 4
FPS = 60

COL_BLACK = (0,0,0)
COL_WHITE = (255,255,255)
COL_RED = (255,0,0)
COL_GRAY = (100,100,100)
BACKGROUND_COLOR = COL_WHITE
WALL_COLOR = (0,255,0)

#Class
class State:
    #Constant Value
    TITLE,PLAYING,RANKING = 0,1,2
    END = 99

    #Default Value
    events = None
    current = 0
    time_start = 0
    time_pass = 0
        
class Helicopter(Character2D):
    MAX_SPEED = 10
    SPEED = 1
    GY = 0.5

    def __init__(self):
        super().__init__()

        self.vecter = Vecter2(0,0)

    def update(self):
        if State.current == State.PLAYING:
            mouse_pressed = pygame.mouse.get_pressed()

            if mouse_pressed[0] == 1 and self.vecter.y > -Helicopter.MAX_SPEED:
                self.vecter.y -= Helicopter.SPEED

            if self.vecter.y < Helicopter.MAX_SPEED:
                self.vecter.y += Helicopter.GY

            self.set_pos_delta(self.vecter.x,self.vecter.y)

    def draw(self,surface:surface):
        surface.blit(chara.image,(chara.center.x,chara.center.y))



class Stage:
    EASY,NORMAL,HARD = 0,1,2

    def __init__(self,window_size:Vecter2):
        #Defalut Value
        self.generate_time_counting = 0            
        self.passway_delta = random.randrange(1,10)
        self.passway_points_y =[]
        self.generate_step = 5   #lower value => higher speed

        self.window_size = window_size
        self.passway_h = self.window_size.y / 2 * 0.5
        self.passway_points_y.append(self.window_size.y/2)

        self.set_level(Stage.EASY)

        for n in range(0,self.window_size.x,PX):
            self.generate_waiting_wall()  

    def set_level(self,level):
        if level == Stage.EASY:
            self.generate_step = 5
            #self.passway_h = self.window_size.y / 2 * 0.5
            self.passway_delta = random.randrange(1,10)
        elif level == Stage.NORMAL:
            self.generate_step = 3
            #self.passway_h = self.window_size.y / 2 * 0.4
            self.passway_delta = random.randrange(1,12)
        elif level == Stage.HARD:
            self.generate_step = 1
            #self.passway_h = self.window_size.y / 2 * 0.3
            self.passway_delta = random.randrange(1,15)

    def reset(self):
        self.set_level(Stage.EASY)

        update_winow_x_px = (int)(self.window_size.x / PX)
        if State.current == State.TITLE:
            update_winow_x_px = int(update_winow_x_px*0.75)
        
            for n in range(0,update_winow_x_px):
                self.roll_next()
        else:
            for n in range(0,update_winow_x_px):
                self.roll_waiting()

    def generate_waiting_wall(self):
        delta = random.randrange(-self.passway_delta,self.passway_delta + 1) * PX
        new_point_y = (self.window_size.y/2) + delta
        self.passway_points_y.append(new_point_y)

    def generate_wall(self):
        delta = random.randrange(-self.passway_delta,self.passway_delta + 1) * PX
        new_point_y = self.passway_points_y[-1] + delta
        
        if (new_point_y - self.passway_h) < PX or (new_point_y + self.passway_h) > (self.window_size.y - PX):
            new_point_y = self.passway_points_y[-1]

        self.passway_points_y.append(new_point_y)
        
    def destroy_wall(self):
        self.passway_points_y.pop(0)

    def roll_next(self):
        self.destroy_wall()
        self.generate_wall()

    def roll_waiting(self):
        self.destroy_wall()
        self.generate_waiting_wall()

    def update(self):
        if self.generate_time_counting >= self.generate_step:
            stage.generate_time_counting = 0

            if State.current == State.PLAYING:
                self.roll_next()
            else:
                self.roll_waiting()
        else:
            self.generate_time_counting += 1 

    def draw(self,surface:surface):
        surface.fill(BACKGROUND_COLOR)   

        winow_x_px = (int)(self.window_size.x / PX) + 1
        for n in range(0,winow_x_px):
            #Rect(pos_x,pos_y,w,h)
            pygame.draw.rect(surface,WALL_COLOR,
                             Rect(n * PX,0,
                                  PX,self.passway_points_y[n] - self.passway_h))
            pygame.draw.rect(surface,WALL_COLOR,
                             Rect(n * PX,self.passway_points_y[n] + self.passway_h,
                                  PX,self.window_size.y - self.passway_points_y[n]))

#Default Value
window_caption = 'Helicopter Game'
window_size = Vecter2(1024,640)
ranking_list = []

#Inital Value
window = Window(window_caption,window_size)
stage = Stage(window.size)
#   UI
pos_center = Vecter2(window_size.x / 2,window_size.y / 2)
panel_title_size = Vecter2(pos_center.x,80)
panel_title = Panel(panel_title_size.tuple(),pos_center.tuple(),
                    background_col=COL_GRAY)
label_title = Label(40,COL_WHITE,pos_center.tuple())
label_title.text = 'Click to Start !'

label_time = Label(40,COL_BLACK,(pos_center.x,20))

panel_ranking = Panel((window_size.x / 2,200),pos_center.tuple(),
                      background_col=COL_GRAY)
label_gameover_size = 80
label_gameover_pos = Vecter2(pos_center.x , pos_center.y - panel_ranking.rect.height/2 - label_gameover_size/2)
label_gameover = Label(label_gameover_size,COL_RED,label_gameover_pos.tuple())
label_gameover.text = 'Game Over !'

label_ranking_size = 40
label_ranking_pos = Vecter2(pos_center.x ,  pos_center.y - panel_ranking.rect.height/2 + label_ranking_size/2)
label_ranking = Label(label_ranking_size,COL_BLACK,label_ranking_pos.tuple())
label_ranking.text = 'Ranking'

label_option_delta = label_ranking_size + 10
label_rankings_pos = [Vecter2(label_ranking_pos.x,label_ranking_pos.y + label_option_delta),
                      Vecter2(label_ranking_pos.x,label_ranking_pos.y + label_option_delta*2),
                      Vecter2(label_ranking_pos.x,label_ranking_pos.y + label_option_delta*3)]
label_rankings = [Label(label_ranking_size,COL_BLACK,label_rankings_pos[0].tuple()),
                  Label(label_ranking_size,COL_BLACK,label_rankings_pos[1].tuple()),
                  Label(label_ranking_size,COL_BLACK,label_rankings_pos[2].tuple())]

#   Character
chara = Helicopter()
chara.image = load_image('helicopter_1.png',-1)
chara.center.x = PX * 10
chara.center.y = window.size.y / 2


#Game Methods
def show_title():
    panel_title.draw(window.surface)
    label_title.draw(window.surface)

def show_ranking():    

    panel_ranking.draw(window.surface)
    label_gameover.draw(window.surface)
    label_ranking.draw(window.surface)

    for n in range(0,len(label_rankings)):
        label = label_rankings[n]
        
        time = 0
        if n < len(ranking_list):
            time = ranking_list[n]

        label.text = '{0}.   {1:>10.2f} sec'.format(n+1,time)
        label.draw(window.surface)

def check_crash():
    if is_crash():
        read_ranking_list()
        new_rank(State.time_pass)

        State.current = State.RANKING

def is_click():
    for event in State.events:
        if event.type == MOUSEBUTTONDOWN:
            return True
    return False

def update_events():
    State.events = pygame.event.get()
    return State.events

def update_timer():
    State.time_pass = time.perf_counter() - State.time_start
    label_time.text = '{:.2f} s'.format(State.time_pass)
    label_time.draw(window.surface)

def is_crash():
    crashed = 0
    
    image_rect=chara.image.get_rect()
    img_h = image_rect.height
    img_w_px = int(image_rect.width / PX)
    img_x_px = int(chara.center.x / PX)

    tolerace = img_h / 4

    for n in range(img_x_px + img_w_px - 2, img_x_px,-1):
        
        if crashed == 0:
            top = stage.passway_points_y[n] - stage.passway_h
            bottom = stage.passway_points_y[n] + stage.passway_h

            if chara.center.y + tolerace < top:
                crashed = 1
            elif chara.center.y + img_h - tolerace > bottom:
                crashed = 2

        if crashed == 1:
            pygame.draw.rect(window.surface,COL_RED,
                    Rect(n * PX,0,
                        PX,stage.passway_points_y[n] - stage.passway_h))
        elif crashed == 2:
            pygame.draw.rect(window.surface,COL_RED,
                Rect(n * PX,stage.passway_points_y[n] + stage.passway_h,
                    PX,stage.window_size.y - stage.passway_points_y[n]))

    return crashed > 0


def reset():
    stage.reset()

    chara.center.x = PX * 10
    chara.center.y = window.size.y / 2
    chara.vecter.y = 0

    State.time_start = time.perf_counter()
    State.time_pass = 0
    State.current = State.TITLE

def read_ranking_list():
    if len(ranking_list) == 0:
        scores = read_json('helicopter game ranking')
        ranking_list.extend(scores)

def write_ranking_list():
    write_json('helicopter game ranking',ranking_list)

def new_rank(new_score):

    ranking_list.sort(reverse=True)
    
    if len(ranking_list) <  len(label_rankings):
        ranking_list.append(new_score)
        ranking_list.sort(reverse=True)
        write_ranking_list()
    else:
        for score in ranking_list:
            if new_score >= score:
                ranking_list.append(new_score)
                ranking_list.sort(reverse=True)

                if len(ranking_list) > len(label_rankings):
                    ranking_list.pop(-1)

                write_ranking_list()
                break

    