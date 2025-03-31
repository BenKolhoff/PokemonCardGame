from game import Game
from menu_manager import MenuManager
import pygame
import pygame_gui
import sys

class PokemonCardGame:
    def __init__(self):
        self.SCREEN_SIZE = (640, 360)
        self.BG_COLOR = pygame.Color('#ffffff')

        pygame.init()
        self.screen = pygame.display.set_mode(self.SCREEN_SIZE)
        self.ui_manager = pygame_gui.UIManager(self.SCREEN_SIZE)

        pygame.display.set_caption('Pokemon Card Game')
        self.background = pygame.Surface(self.SCREEN_SIZE)
        self.background.fill(self.BG_COLOR)

        self.clock = pygame.time.Clock()
        self.running = True
        self.game = Game()

        self.menu_manager = MenuManager(self.game, self.SCREEN_SIZE, self.ui_manager)
        self.current_menu = self.menu_manager.create_start_menu()

    def start_game(self):
        self.current_menu = self.menu_manager.create_game_menu()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

                pygame.quit()
                sys.exit()
            
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element.text == "Start":
                    self.start_game()
            
            self.ui_manager.process_events(event)

    def text_input(self):
        valid_actions = ["attack", "retreat", "state", "hand", "draw"]
        action = input("Enter Action>>>")
        action = action.split(' ')

        if action[0] == "attack" and len(action) > 1:
            if self.game.state.current_player.active_card != None: # Check if current player has an active card
                if 0 <= int(action[1]) < len(self.game.state.current_player.active_card.moves):
                    move = self.game.state.current_player.active_card.moves[int(action[1])]
                    other_player = self.game.state.get_player_list()[0] if self.game.state.current_player != self.game.state.get_player_list()[0] else self.game.state.get_player_list()[1]
                    
                    self.game.state.current_player.active_card.attack(other_player.active_card, move)
                    self.game.state.change_player()
                else: print("Error: The specified move is not valid for the active card")
            else: print("Error: You cannot attack without an active card")
        elif action[0] == "state":
            self.game.state.print_state()
        elif action[0] == "hand":
            self.game.state.current_player.print_hand()
        elif action[0] == "draw":
            self.game.state.current_player.draw_card()
        elif action[0] == "active" and len(action) > 1:
            self.game.state.current_player.set_active_card(int(action[1]))

            if self.game.state.activate_card_phase == True:
                self.game.state.change_player()
                self.game.state.activate_card_phase = not (self.game.state.get_player_list()[0].active_card != None and self.game.state.get_player_list()[1].active_card != None)
        elif action[0] == "pass":
            self.game.state.change_player()
        else:
            print("Error: That is not a valid action")

        if self.game.state.playerA.points >= 3 or self.game.state.playerB.points >= 3:
            print(f"{"Player A" if self.game.state.playerA.points >= 3 else "Player B"} won!")
            self.running = False

    def run(self): 
        while self.running:
            time_delta = self.clock.tick(60)/1000.0

            self.events()
            self.ui_manager.update(time_delta)

            self.screen.blit(self.background, (0, 0))
            self.ui_manager.draw_ui(self.screen)

            pygame.display.update()

if __name__ == '__main__':
     game_app = PokemonCardGame()
     game_app.run()