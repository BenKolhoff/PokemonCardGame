from card import Card
from move import Move
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

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

            pygame.quit()
            sys.exit()

    valid_actions = ["attack", "retreat", "state", "hand", "draw"]
    action = input("Enter Action>>>")
    action = action.split(' ')

    if action[0] == "attack" and len(action) > 1:
        if game.state.current_player.active_card != None: # Check if current player has an active card
            if 0 <= int(action[1]) < len(game.state.current_player.active_card.moves):
                move = game.state.current_player.active_card.moves[int(action[1])]
                other_player = game.state.get_player_list()[0] if game.state.current_player != game.state.get_player_list()[0] else game.state.get_player_list()[1]
                
                game.state.current_player.active_card.attack(other_player.active_card, move)
                game.state.change_player()
            else: print("Error: The specified move is not valid for the active card")
        else: print("Error: You cannot attack without an active card")
    elif action[0] == "state":
        game.state.print_state()
    elif action[0] == "hand":
        game.state.current_player.print_hand()
    elif action[0] == "draw":
        game.state.current_player.draw_card()
    elif action[0] == "active" and len(action) > 1:
        game.state.current_player.set_active_card(int(action[1]))

        if game.state.activate_card_phase == True:
            game.state.change_player()
            game.state.activate_card_phase = not (game.state.get_player_list()[0].active_card != None and game.state.get_player_list()[1].active_card != None)
    elif action[0] == "pass":
        game.state.change_player()
    else:
        print("Error: That is not a valid action")

    if game.state.playerA.points >= 3 or game.state.playerB.points >= 3:
        print(f"{"Player A" if game.state.playerA.points >= 3 else "Player B"} won!")
        running = False
