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
            current_card = self.game.state.current_player.active_card
            if current_card is not None:
                try:
                    move_index = int(action[1])
                    if 0 <= move_index < len(current_card.moves):
                        move = current_card.moves[move_index]
                        players = self.game.state.get_player_list()
                        other_player = players[0] if self.game.state.current_player != players[0] else players[1]
                        current_card.attack(other_player.active_card, move)
                        self.game.state.change_player()
                    else:
                        print("Error: The specified move is not valid for the active card")
                except ValueError:
                    print("Error: Please enter a valid integer for the move index")
            else:
                print("Error: You cannot attack without an active card")
        elif action[0] == "state":
            self.game.state.print_state()
        elif action[0] == "hand":
            self.game.state.current_player.print_hand()
        elif action[0] == "draw":
            self.game.state.current_player.draw_card()
        elif action[0] == "active" and len(action) > 1:
            try:
                index = int(action[1])
                self.game.state.current_player.set_active_card(index)
            except ValueError:
                print("Error: Please enter a valid integer for the card index")
            # Check if both players have an active card to exit activation phase
            if self.game.state.activate_card_phase:
                self.game.state.change_player()
                both_active = (self.game.state.get_player_list()[0].active_card is not None and
                               self.game.state.get_player_list()[1].active_card is not None)
                self.game.state.activate_card_phase = not both_active
        elif action[0] == "pass":
            self.game.state.change_player()
        else:
            print("Error: That is not a valid action")

    def run(self):
        """Main game loop."""
        while self.running:
            self.events()
            self.inputs()
            
            # Check for a winning condition
            if self.game.state.playerA.points >= 3 or self.game.state.playerB.points >= 3:
                winner = "Player A" if self.game.state.playerA.points >= 3 else "Player B"
                print(f"{winner} won!")
                self.running = False

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
if __name__ == '__main__':
    game_app = PokemonCardGame()
    game_app.run()