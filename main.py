from game import Game
import pygame
import pygame_gui
import sys

SCREEN_SIZE = (640, 360)
BG_COLOR = pygame.Color('#ffffff')

pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
ui_manager = pygame_gui.UIManager(SCREEN_SIZE)

pygame.display.set_caption('Pokemon Card Game')
background = pygame.Surface(SCREEN_SIZE)
background.fill(BG_COLOR)

clock = pygame.time.Clock()
running = True
game = Game()

hello_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 275), (200, 50)), text='Hello World', manager=ui_manager)

def text_input():
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

while running:
    time_delta = clock.tick(60)/1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

            pygame.quit()
            sys.exit()
        
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == hello_button:
                print('Hello World')

        ui_manager.process_events(event)

    ui_manager.update(time_delta)

    screen.blit(background, (0, 0))
    ui_manager.draw_ui(screen)

    pygame.display.update()