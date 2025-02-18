from card import Card
from player import Player
from move import Move
from state import State
from game import Game
import pygame
import sys

screen = pygame.display.set_mode((300, 300))

bg_color = (255, 255, 255)

pygame.display.set_caption('Pokemon Card Game')

screen.fill(bg_color)

pygame.display.flip()

running = True
game = Game()
zap = Move("Zap", 50, 1)
pikachu = Card("Pikachu", "Lightning", 100, "basic")
raichu = Card("Raichu", "Lightning", 150, "stage 1")

game.state.playerA.active_card = pikachu
game.state.playerB.active_card = raichu

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

            pygame.quit()
            sys.exit()

    valid_actions = ["attack", "retreat"]
    action = input("Enter Action>>>")

    if action == "attack":
        if game.state.current_player == game.state.playerA:
            game.state.playerA.active_card.attack(game.state.playerB.active_card, zap)
            game.state.change_player()
        elif game.state.current_player == game.state.playerB:
            game.state.playerB.active_card.attack(game.state.playerA.active_card, zap)
            game.state.change_player()
    
    if game.state.playerA.active_card.hp <= 0:
        game.state.playerB.increase_points()
        print("Player B Points:", game.state.playerB.points)
    
    elif game.state.playerB.active_card.hp <= 0:
        game.state.playerA.increase_points()
        print("Player A Points:", game.state.playerA.points)

    if game.state.playerA.points >= 3 or game.state.playerB.points >= 3:
        running = False

