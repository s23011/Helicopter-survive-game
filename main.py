#標準モジュール
import time
import sys
#インストールのモジュール
import pygame
from pygame.locals import *
#自分のモジュール
import helicopter_game as game
from helicopter_game import State as GameState

surface = game.window.surface
clock = pygame.time.Clock()

while True:
    events = game.update_events()
    
    #   Title
    if GameState.current == GameState.TITLE:
        if game.is_click():
            game.reset()
            game.State.current = GameState.PLAYING
        else:
            game.stage.update()
            game.stage.draw(surface)
            game.chara.draw(surface)

            game.show_title()

    #   Playing
    elif GameState.current == GameState.PLAYING:
        game.stage.update()
        game.stage.draw(surface)
        game.chara.update()
        game.chara.draw(surface)

        game.update_timer()

        game.check_crash()

        if game.State.time_pass > 30:
           game.stage.set_level(game.Stage.HARD) 
        elif game.State.time_pass > 15:
           game.stage.set_level(game.Stage.NORMAL) 

    #   Ranking
    elif GameState.current == GameState.RANKING:
        if game.is_click():
            game.reset()
        else:
            game.show_ranking()

    pygame.display.update()
    clock.tick(game.FPS)
    
    for event in events:
        if event.type == QUIT:
            pygame.quit
            sys.exit()

