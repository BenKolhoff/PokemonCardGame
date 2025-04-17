import random
from card import Card
from move import Move
from game import Game
import pygame
import sys


class PokemonCardGame:
    def __init__(self):
        pygame.init()
        icon = pygame.image.load("sprites/tcg.png")
        pygame.display.set_icon(icon)
        self.screen = pygame.display.set_mode((1000, 600))
        self.bg_color = (255, 255, 255)
        pygame.display.set_caption('Pokemon Card Game')
        self.screen.fill(self.bg_color)
        pygame.display.flip()

        self.running = True
        self.game = Game()
        self.font = pygame.font.SysFont(None, 24)

        # UI buttons and input setup...
        self.attack_button_rect = pygame.Rect(300, 550, 100, 40)
        self.draw_button_rect = pygame.Rect(175, 550, 100, 40)
        self.bench_button_rect = pygame.Rect(425, 550, 100, 40)
        self.active_button_rect = pygame.Rect(50, 550, 100, 40)
        self.input_box_rect = pygame.Rect(50, 500, 100, 30)
        self.input_active = False
        self.current_input_src = None
        self.active_input_text = ""
        self.message_log = []
        
        # Begin deck selection before starting game loop.
        self.deck_selection_phase()

    def set_message(self, message):
        self.message_log.append(message)

    def deck_selection_phase(self):
        scroll_offset = 0  # New variable to track vertical scroll offset
        # Let each player choose 10 cards from self.game.pokemon using the UI.
        for player in self.game.state.get_player_list():
            chosen_cards = []  # Will hold the JSON objects for the chosen Pokémon.
            while len(chosen_cards) < 10 and self.running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.MOUSEWHEEL:
                        # Adjust the scroll offset (tweak the multiplier 30 as needed)
                        scroll_offset += event.y * 30
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        # Display the list, with scroll offset.
                        for index, poke in enumerate(self.game.pokemon):
                            y = 50 + index * 30 + scroll_offset
                            rect = pygame.Rect(50, y, 200, 25)
                            if rect.collidepoint(event.pos) and poke not in chosen_cards:
                                chosen_cards.append(poke)
                                self.set_message(f"Player {player.name} selected {poke['Name']} ({len(chosen_cards)}/10)")
                # Redraw the deck selection screen.
                self.screen.fill(self.bg_color)
                prompt = self.font.render(f"Player {player.name}: Select 10 cards.", True, (0, 0, 0))
                self.screen.blit(prompt, (50, 10))
                # Draw available Pokémon using scroll_offset.
                for index, poke in enumerate(self.game.pokemon):
                    y = 50 + index * 30 + scroll_offset
                    poke_text = self.font.render(f"{poke['Number']}: {poke['Name']}", True, (0, 0, 0))
                    self.screen.blit(poke_text, (50, y))
                # Display currently selected numbers.
                sel_text = self.font.render(
                    f"Selected ({len(chosen_cards)}/10): " + ", ".join([str(p["Number"]) for p in chosen_cards]),
                    True, (0, 0, 0))
                self.screen.blit(sel_text, (300, 50))
                pygame.display.flip()
            # Build a deck for the player based on the chosen cards.
            deck = []
            for poke in chosen_cards:
                new_card = Card(
                    poke['Name'],
                    poke['Type'],
                    poke['HP'],
                    poke['Stage'],
                    poke['Weakness'],
                    poke['Retreat'],
                    poke['evolves_from'],
                    None,
                    player
                )
                if 'Moves' in poke:
                    temp_moves = []
                    for move_name in poke['Moves']:
                        for move in self.game.moves:
                            if move['Name'] == move_name:
                                temp_move = Move(move['Name'], move['Damage'], move['Cost'])
                                temp_moves.append(temp_move)
                    new_card.moves = temp_moves
                deck.append(new_card)
            # Override any pre-existing deck and hand
            player.set_deck(deck)
            player.hand = []
            # Randomly draw 5 cards as starting hand.
            if len(player.deck) >= 5:
                starting_hand = random.sample(player.deck, 5)
            else:
                starting_hand = player.deck[:]
            for card in starting_hand:
                player.hand.append(card)
                player.deck.remove(card)
            self.set_message(f"Player {player.name} deck selection complete.")

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

    def draw_draw_button(self):
        # Draw a blue button with white "Draw" text.
        pygame.draw.rect(self.screen, (0, 0, 200), self.draw_button_rect)
        text_surface = self.font.render("Draw", True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.draw_button_rect.center)
        self.screen.blit(text_surface, text_rect)
        pygame.display.update(self.draw_button_rect)

    def draw_bench_button(self):
        # Draw a green button with white "Bench" text.
        pygame.draw.rect(self.screen, (0, 200, 0), self.bench_button_rect)
        text_surface = self.font.render("Bench", True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.bench_button_rect.center)
        self.screen.blit(text_surface, text_rect)
        pygame.display.update(self.bench_button_rect)

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
        self.screen.blit(text_surface, (425, 20))

    def draw_points(self):
        player_a = self.game.state.playerA
        player_b = self.game.state.playerB
        a_text = f"Player A Points: {player_a.points}"
        b_text = f"Player B Points: {player_b.points}"
        a_surface = self.font.render(a_text, True, (0, 0, 0))
        b_surface = self.font.render(b_text, True, (0, 0, 0))
        # Adjust the positions as needed.
        self.screen.blit(a_surface, (20, 80))
        self.screen.blit(b_surface, (650, 80))

    def draw_active_cards(self):
        player_a = self.game.state.playerA
        player_b = self.game.state.playerB
        active_a = player_a.active_card
        active_b = player_b.active_card
        a_text = f"Player A Active: {active_a.name if active_a is not None else 'None'}{f' (HP: {active_a.hp})' if active_a is not None else ''}"
        b_text = f"Player B Active: {active_b.name if active_b is not None else 'None'}{f' (HP: {active_b.hp})' if active_b is not None else ''}"
        
        a_surface = self.font.render(a_text, True, (0, 0, 0))
        b_surface = self.font.render(b_text, True, (0, 0, 0))
        # Adjust the positions as needed.
        self.screen.blit(a_surface, (20, 110))
        self.screen.blit(b_surface, (650, 110))

    def draw_hand_options(self):
        """Display the current player's hand as selectable options."""
        hand = self.game.state.current_player.hand
        start_y = 150
        screen_width = self.screen.get_width()
        for index, card in enumerate(hand):
            card_text = f"{index}: {card.name} ({card.stage}) (HP: {card.hp})"
            text_surface = self.font.render(card_text, True, (0, 0, 0))
            text_rect = text_surface.get_rect()
            text_rect.centerx = screen_width // 2
            text_rect.y = start_y + index * 20
            self.screen.blit(text_surface, text_rect)

    def draw_benched_cards(self):
        # Draw Player A's bench underneath active card (active card drawn at (20, 110))
        bench_text_surface_a = self.font.render("Bench:", True, (0, 0, 0))
        self.screen.blit(bench_text_surface_a, (20, 150))
        player_a_bench = self.game.state.playerA.benched_cards
        for index, card in enumerate(player_a_bench):
            card_text = f"{index}: {card.name} (HP: {card.hp})"
            text_surface = self.font.render(card_text, True, (0, 0, 0))
            self.screen.blit(text_surface, (20, 180 + index * 20))

        # Draw Player B's bench underneath active card (active card drawn at (650, 110))
        bench_text_surface_b = self.font.render("Bench:", True, (0, 0, 0))
        self.screen.blit(bench_text_surface_b, (650, 150))
        player_b_bench = self.game.state.playerB.benched_cards
        for index, card in enumerate(player_b_bench):
            card_text = f"{index}: {card.name} (HP: {card.hp})"
            text_surface = self.font.render(card_text, True, (0, 0, 0))
            self.screen.blit(text_surface, (650, 180 + index * 20))

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
                    self.current_input_src = self.active_button_rect
                    self.active_input_text = ""
                elif self.draw_button_rect.collidepoint(event.pos):
                    self.game.state.current_player.draw_card()
                    self.game.state.change_player()
                elif self.bench_button_rect.collidepoint(event.pos):
                    if len(self.game.state.current_player.benched_cards) < 3:
                        self.input_active = True
                        self.current_input_src = self.bench_button_rect
                        self.active_input_text = ""
            elif event.type == pygame.KEYDOWN and self.input_active:
                if event.key == pygame.K_RETURN:
                    # Finalize input and attempt to set the active card.
                    try:
                        if self.current_input_src is self.active_button_rect:
                            index = int(self.active_input_text)
                            self.game.state.current_player.set_active_from_bench(index)
                        elif self.current_input_src is self.bench_button_rect:
                            index = int(self.active_input_text)
                            self.game.state.current_player.bench_card(index)
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
        while self.running:
            self.events()
            self.screen.fill(self.bg_color)
            self.draw_turn_info()
            self.draw_points()
            self.draw_active_cards()
            self.draw_hand_options()
            self.draw_benched_cards()
            self.draw_attack_button()
            self.draw_active_button()
            self.draw_draw_button()
            self.draw_bench_button()
            if self.input_active:
                self.draw_input_box()
            self.draw_message()
            # Winning condition check...
            if self.game.state.playerA.points >= 3 or self.game.state.playerB.points >= 3:
                winner = "Player A" if self.game.state.playerA.points >= 3 else "Player B"
                self.set_message(f"{winner} won!")
            pygame.display.flip()
            pygame.time.delay(100)


if __name__ == '__main__':
    game_app = PokemonCardGame()
    game_app.run()