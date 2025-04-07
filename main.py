from card import Card
from move import Move
from game import Game
import pygame
import sys


class PokemonCardGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((700, 600))
        self.bg_color = (255, 255, 255)
        pygame.display.set_caption('Pokemon Card Game')
        self.screen.fill(self.bg_color)
        pygame.display.flip()

        self.running = True
        self.game = Game()

        # Create a button rectangle for "Attack" and initialize a font for its text.
        self.attack_button_rect = pygame.Rect(300, 550, 100, 40)
        self.font = pygame.font.SysFont(None, 24)

        # New UI element for setting an active card.
        self.active_button_rect = pygame.Rect(50, 550, 100, 40)
        self.input_active = False
        self.active_input_text = ""
        self.input_box_rect = pygame.Rect(50, 500, 100, 30)

        # Message log to display multiple messages.
        self.message_log = []

    def set_message(self, message):
        # Append the new message to the log.
        self.message_log.append(message)

    def draw_message(self):
        # Display only the most recent message at the bottom middle of the screen.
        if self.message_log:
            msg = self.message_log[-1]
            text_surface = self.font.render(msg, True, (255, 0, 0))
            text_rect = text_surface.get_rect()
            screen_width = self.screen.get_width()
            screen_height = self.screen.get_height()
            text_rect.midbottom = (screen_width // 2, screen_height - 60)
            self.screen.blit(text_surface, text_rect)

    def draw_attack_button(self):
        # Draw a green button with white "Attack" text.
        pygame.draw.rect(self.screen, (0, 200, 0), self.attack_button_rect)
        text_surface = self.font.render("Attack", True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.attack_button_rect.center)
        self.screen.blit(text_surface, text_rect)
        pygame.display.update(self.attack_button_rect)

    def draw_active_button(self):
        # Draw a blue button with white "Set Active" text.
        pygame.draw.rect(self.screen, (0, 0, 200), self.active_button_rect)
        text_surface = self.font.render("Set Active", True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.active_button_rect.center)
        self.screen.blit(text_surface, text_rect)
        pygame.display.update(self.active_button_rect)

    def draw_input_box(self):
        # Draw the input rectangle and the current text.
        pygame.draw.rect(self.screen, (200, 200, 200), self.input_box_rect)
        pygame.draw.rect(self.screen, (0, 0, 0), self.input_box_rect, 2)
        text_surface = self.font.render(self.active_input_text, True, (0, 0, 0))
        self.screen.blit(text_surface, (self.input_box_rect.x + 5, self.input_box_rect.y + 5))
        pygame.display.update(self.input_box_rect)

    def draw_turn_info(self):
        turn_text = f"Turn: Player {self.game.state.current_player.name}"
        text_surface = self.font.render(turn_text, True, (0, 0, 0))
        # Adjust the position as needed
        self.screen.blit(text_surface, (300, 20))

    def draw_points(self):
        player_a = self.game.state.playerA
        player_b = self.game.state.playerB
        a_text = f"Player A Points: {player_a.points}"
        b_text = f"Player B Points: {player_b.points}"
        a_surface = self.font.render(a_text, True, (0, 0, 0))
        b_surface = self.font.render(b_text, True, (0, 0, 0))
        # Adjust the positions as needed.
        self.screen.blit(a_surface, (20, 80))
        self.screen.blit(b_surface, (500, 80))

    def draw_active_cards(self):
        player_a = self.game.state.playerA
        player_b = self.game.state.playerB
        active_a = player_a.active_card.name if player_a.active_card else "None"
        active_b = player_b.active_card.name if player_b.active_card else "None"
        a_text = f"Player A Active: {active_a}"
        b_text = f"Player B Active: {active_b}"
        a_surface = self.font.render(a_text, True, (0, 0, 0))
        b_surface = self.font.render(b_text, True, (0, 0, 0))
        # Adjust the positions as needed.
        self.screen.blit(a_surface, (20, 110))
        self.screen.blit(b_surface, (500, 110))

    def draw_hand_options(self):
        """Display the current player's hand as selectable options."""
        hand = self.game.state.current_player.hand
        # Start drawing from a Y position; adjust as needed.
        start_y = 150
        for index, card in enumerate(hand):
            card_text = f"{index}: {card.name}"
            text_surface = self.font.render(card_text, True, (0, 0, 0))
            self.screen.blit(text_surface, (20, start_y + index * 20))

    def attack_action(self):
        current_card = self.game.state.current_player.active_card
        if current_card is not None:
            try:
                if 0 <= 0 < len(current_card.moves):
                    move = current_card.moves[0]
                    players = self.game.state.get_player_list()
                    other_player = players[0] if self.game.state.current_player != players[0] else players[1]
                    attack_message = current_card.attack(other_player.active_card, move)
                    self.game.state.change_player()
                    self.set_message(attack_message)
                else:
                    self.set_message("Error: The specified move is not valid for the active card")
            except Exception as ex:
                self.set_message("Attack error: " + str(ex))
        else:
            self.set_message("Error: You cannot attack without an active card")

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.attack_button_rect.collidepoint(event.pos):
                    self.attack_action()
                elif self.active_button_rect.collidepoint(event.pos):
                    # Activate text input for setting an active card.
                    self.input_active = True
                    self.active_input_text = ""
            elif event.type == pygame.KEYDOWN and self.input_active:
                if event.key == pygame.K_RETURN:
                    # Finalize input and attempt to set the active card.
                    try:
                        index = int(self.active_input_text)
                        self.game.state.current_player.set_active_card(index)
                    except ValueError:
                        self.set_message("Error: Please enter a valid integer for the card index")
                    self.input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    self.active_input_text = self.active_input_text[:-1]
                else:
                    self.active_input_text += event.unicode

    def inputs(self):
        # Retained console input if needed for other actions.
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
                        self.set_message("Error: The specified move is not valid for the active card")
                except ValueError:
                    self.set_message("Error: Please enter a valid integer for the move index")
            else:
                self.set_message("Error: You cannot attack without an active card")
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
                self.set_message("Error: Please enter a valid integer for the card index")
            # Check if both players have an active card.
            if self.game.state.activate_card_phase:
                self.game.state.change_player()
                both_active = (self.game.state.get_player_list()[0].active_card is not None and
                               self.game.state.get_player_list()[1].active_card is not None)
                self.game.state.activate_card_phase = not both_active
        elif action[0] == "pass":
            self.game.state.change_player()
        else:
            self.set_message("Error: That is not a valid action")

    def run(self):
        """Main game loop."""
        while self.running:
            self.events()
            # Redraw background and buttons every loop iteration.
            self.screen.fill(self.bg_color)
            self.draw_turn_info()  # Draw the current player's turn
            self.draw_points()     # Display players' points
            self.draw_active_cards()  # Display both players' active cards
            self.draw_hand_options()    # Display current player's hand options
            self.draw_attack_button()
            self.draw_active_button()
            if self.input_active:
                self.draw_input_box()
            # Draw the message log on screen.
            self.draw_message()
            # Check for a winning condition.
            if self.game.state.playerA.points >= 3 or self.game.state.playerB.points >= 3:
                winner = "Player A" if self.game.state.playerA.points >= 3 else "Player B"
                self.set_message(f"{winner} won!")
                # self.running = False  <-- Comment out or remove this line to keep the game running

            # Update the display (flip the buffer).
            pygame.display.flip()
            pygame.time.delay(100)


if __name__ == '__main__':
    game_app = PokemonCardGame()
    game_app.run()