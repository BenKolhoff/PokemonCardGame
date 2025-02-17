from card import Card
from player import Player
from move import Move
from state import State
import pygame
import sys

screen = pygame.display.set_mode((300, 300))

bg_color = (255, 255, 255)

pygame.display.set_caption('Pokemon Card Game')

screen.fill(bg_color)

pygame.display.flip()

running = True
state = State()
zap = Move("Zap", 50, 1)
pikachu = Card("Pikachu", "Lightning", 100, "basic")
raichu = Card("Raichu", "Lightning", 150, "stage 1")

state.playerA.active_card = pikachu
state.playerB.active_card = raichu

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

            pygame.quit()
            sys.exit()

    valid_actions = ["attack", "retreat"]
    action = input("Enter Action>>>")

    if action == "attack":
        if state.current_player == state.playerA:
            state.playerA.active_card.attack(state.playerB.active_card, zap)
            state.change_player()
        elif state.current_player == state.playerB:
            state.playerB.active_card.attack(state.playerA.active_card, zap)
            state.change_player()
    
    if state.playerA.active_card.hp <= 0:
        state.playerB.increase_points()
        print("Player B Points:", state.playerB.points)
    
    elif state.playerB.active_card.hp <= 0:
        state.playerA.increase_points()
        print("Player A Points:", state.playerA.points)

    if state.playerA.points >= 3 or state.playerB.points >= 3:
        running = False

