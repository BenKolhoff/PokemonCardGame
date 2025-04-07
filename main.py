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
        self.screen = pygame.display.set_mode((300, 300))
        self.bg_color = (255, 255, 255)
        pygame.display.set_caption('Pokemon Card Game')
        self.background = pygame.Surface(self.SCREEN_SIZE)
        self.background.fill(self.BG_COLOR)

        self.clock = pygame.time.Clock()
        self.running = True
        self.game = Game()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

                pygame.quit()
                sys.exit()

    def inputs(self):
        valid_actions = ["attack", "retreat", "state", "hand", "draw"]
        action = input("Enter Action>>>").strip().split(' ')

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
                self.game.state.activate_card_phase = not (self.game.state.get_player_list()[0].active_card != None and self.game.state.get_player_list()[1].active_card != None)
        elif action[0] == "pass":
            self.game.state.change_player()
        else:
            self.set_message("Error: That is not a valid action")

        if self.game.state.playerA.points >= 3 or self.game.state.playerB.points >= 3:
            print(f"{"Player A" if self.game.state.playerA.points >= 3 else "Player B"} won!")
            self.running = False

    def run(self): 
        while self.running:
            time_delta = self.clock.tick(60)/1000.0

            self.events()
            self.inputs()
            
            # Check for a winning condition
            if self.game.state.playerA.points >= 3 or self.game.state.playerB.points >= 3:
                winner = "Player A" if self.game.state.playerA.points >= 3 else "Player B"
                print(f"{winner} won!")
                self.running = False

            # Update the display (flip the buffer).
            pygame.display.flip()

            # Small delay so that the loop doesn't hog the CPU.
            pygame.time.delay(100)


if __name__ == '__main__':
     game_app = PokemonCardGame()
     game_app.run()