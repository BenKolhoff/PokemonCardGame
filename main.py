import random
from card import Card
from move import Move
from game import Game
import pygame
import sys

'''
The main class of the game, acts as the entry point and handles display/UI input and communicates with its own Game instance.

Attributes:
screen (Surface) - The main screen surface.
bg_color ((int, int, int)) - The background color (as an int triple).
bg_image (Surface) - The background image.
running (boolean) - Whether or not the game is running.
game (Game) - An instance of Game that handles the actual logic of the game.
font (Font) - The font used by all text.
attack_button_rect (Rect) - The Rect used by the attack button.
draw_button_rect (Rect) - The Rect used by the draw button.
bench_button_rect (Rect) - The Rect used by the bench button.
active_button_rect (Rect) - The Rect used by the active button.
attach_button_rect (Rect) - The Rect used by the attach button.
pass_button_rect (Rect) - The Rect used by the pass button.
input_box_rect (Rect) - The Rect used by the input text field.
input_active (boolean) - Whether or not the input box is taking input/displaying.
current_input_src (Rect) - The rect of the last button clicked that calls for input_active to be true.
active_input_text (str) - The message of the active input text.
message_log (str[]) - A log of all messages the game has output to the user.
should_draw_message (boolean) - Whether or not the last message of message_log should be shown to the user.
should_draw_game_ui (boolean) - Whether or not the game's UI should be drawn.

Methods:
set_message(message: str) -> None - Sets the current message that is displayed above the buttons.
deck_selection_phase -> None - Creates and handles the logic for the deck selection screen.
draw_message -> None - Draws the current message for the user above the buttons.
draw_attack_button -> None - Handles drawing the attack button.
draw_active_button -> None - Handles drawing the active button.
draw_draw_button -> None - Handles drawing the draw button.
draw_bench_button -> None - Handles drawing the bench button.
draw_attach_button -> None - Handles drawing the attach button.
draw_pass_button -> None - Handles drawing the pass button.
draw_input_box -> None - Handles drawing the input box (for entering card indexes).
draw_turn_info -> None - Handles drawing the text that displays whose turn it is.
draw_points -> None - Handles drawing the text that displays how many points each player has.
draw_energy -> None - Handles drawing the text that displays how much energy current player has.
draw_active_card_move -> None - Handles drawing the text that displays the move of the active card.
draw_active_cards -> None - Handles drawing the active card text for each player.
draw_hand_options -> None - Handles drawing the current player's hand.
draw_benched_cards -> None - Handles drawing the bench for each player.
attack_action -> None - Handles the attack action.
events -> None - Handles event logic for UI inputs.
run -> None - The main loop of the game.
'''
class PokemonCardGame:
    def __init__(self):
        pygame.init()
        icon = pygame.image.load("sprites/tcg.png")
        pygame.display.set_icon(icon)
        self.screen = pygame.display.set_mode((1000, 600))
        self.bg_color = (255, 255, 255)

        # Load & scale your background
        self.bg_image = pygame.image.load("sprites/background8.jpg").convert()
        self.bg_image = pygame.transform.scale(self.bg_image, self.screen.get_size())

        pygame.display.set_caption('Pokemon Card Game')
        self.screen.fill(self.bg_color)
        pygame.display.flip()
        self.attack_button_rect = pygame.Rect(300, 550, 100, 40)
        self.draw_button_rect = pygame.Rect(175, 550, 100, 40)
        self.bench_button_rect = pygame.Rect(425, 550, 100, 40)
        self.active_button_rect = pygame.Rect(50, 550, 100, 40)
        self.attach_button_rect = pygame.Rect(550, 550, 100, 40)
        self.pass_button_rect = pygame.Rect(675, 550, 100, 40)
        self.input_box_rect = pygame.Rect(50, 500, 100, 30)
        self.input_box_rect_positions = [(50, 500), (425, 500), (550, 500)]
        self.input_active = False
        self.current_input_src = None
        self.active_input_text = ""
        self.message_log = []
        self.should_draw_message = True

        from game import Game
        self.game = Game()
        self.running = True
        self.font = pygame.font.SysFont(None, 24)
        
        # Begin deck selection before starting game loop.
        self.deck_selection_phase()

    '''
    Sets the current message that is displayed above the buttons.

    return: None
    '''
    def set_message(self, message):
        self.should_draw_message = True
        self.message_log.append(message)

    '''
    Creates and handles the logic for the deck selection screen.

    return: None
    '''
    def deck_selection_phase(self):
        # Start playing opening music on loop
        pygame.mixer.music.load("sounds/opening.mp3")
        pygame.mixer.music.set_volume(0.3)  # Lower volume for background music
        pygame.mixer.music.play(-1)
        
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
                        scroll_offset += event.y * 30
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        for index, poke in enumerate(self.game.pokemon):
                            y = 50 + index * 30 + scroll_offset
                            rect = pygame.Rect(50, y, 200, 25)
                            if rect.collidepoint(event.pos) and poke not in chosen_cards:
                                chosen_cards.append(poke)
                                self.set_message(f"Player {player.name} selected {poke['Name']} ({len(chosen_cards)}/10)")
                self.screen.fill(self.bg_color)
                prompt = self.font.render(f"Player {player.name}: Select 10 cards.", True, (0, 0, 0))
                self.screen.blit(prompt, (50, 10))
                for index, poke in enumerate(self.game.pokemon):
                    y = 50 + index * 30 + scroll_offset
                    poke_text = self.font.render(f"{poke['Number']}: {poke['Name']}", True, (0, 0, 0))
                    self.screen.blit(poke_text, (50, y))
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
            player.set_deck(deck)
            player.hand = []
            if len(player.deck) >= 5:
                starting_hand = random.sample(player.deck, 5)
            else:
                starting_hand = player.deck[:]
            for card in starting_hand:
                player.hand.append(card)
                player.deck.remove(card)
            self.set_message(f"Player {player.name} deck selection complete.")
        
        # Stop opening music once deck selection is finished.
        pygame.mixer.music.stop()

    '''
    Draws the current message for the user above the buttons.
    
    return: None
    '''
    def draw_message(self, x=None, y=None):
        # Display only the most recent message at the bottom middle of the screen.
        if self.message_log:
            msg = self.message_log[-1]
            text_surface = self.font.render(msg, True, (255, 0, 0))
            text_rect = text_surface.get_rect()
            screen_width = self.screen.get_width()
            screen_height = self.screen.get_height()
            text_rect.x = x if x != None else 20
            text_rect.y = y if y != None else screen_height - 140
            self.screen.blit(text_surface, text_rect)

    '''
    Handles drawing the attack button.

    return: None
    '''
    def draw_attack_button(self, mouse_pos):
        normal, hover = (255, 0, 0), (255, 100, 100)
        color = hover if self.attack_button_rect.collidepoint(mouse_pos) else normal
        pygame.draw.rect(self.screen, color, self.attack_button_rect, border_radius=10)
        text_surface = self.font.render("Attack", True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.attack_button_rect.center)
        self.screen.blit(text_surface, text_rect)
        pygame.display.update(self.attack_button_rect)

    '''
    Handles drawing the active button.

    return: None
    '''
    def draw_active_button(self, mouse_pos):
        normal, hover = (0, 0, 200), (100, 100, 255)
        color = hover if self.active_button_rect.collidepoint(mouse_pos) else normal
        pygame.draw.rect(self.screen, color, self.active_button_rect, border_radius=10)
        text_surface = self.font.render("Set Active", True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.active_button_rect.center)
        self.screen.blit(text_surface, text_rect)
        pygame.display.update(self.active_button_rect)

    '''
    Handles drawing the draw button.

    return: None
    '''
    def draw_draw_button(self, mouse_pos):
        normal, hover = (0, 0, 200), (100, 100, 255)
        color = hover if self.draw_button_rect.collidepoint(mouse_pos) else normal
        pygame.draw.rect(self.screen, color, self.draw_button_rect, border_radius=10)
        text_surface = self.font.render("Draw", True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.draw_button_rect.center)
        self.screen.blit(text_surface, text_rect)
        pygame.display.update(self.draw_button_rect)

    '''
    Handles drawing the bench button.

    return: None
    '''
    def draw_bench_button(self, mouse_pos):
        normal, hover = (0, 200, 0), (100, 255, 100)
        color = hover if self.bench_button_rect.collidepoint(mouse_pos) else normal
        pygame.draw.rect(self.screen, color, self.bench_button_rect, border_radius=10)
        text_surface = self.font.render("Bench", True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.bench_button_rect.center)
        self.screen.blit(text_surface, text_rect)
        pygame.display.update(self.bench_button_rect)

    '''
    Handles drawing the attach button.

    return: None
    '''
    def draw_attach_button(self, mouse_pos):
        normal, hover = (0, 0, 200), (100, 100, 255)
        color = hover if self.attach_button_rect.collidepoint(mouse_pos) else normal
        pygame.draw.rect(self.screen, color, self.attach_button_rect, border_radius=10)
        text_surface = self.font.render("Attach", True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.attach_button_rect.center)
        self.screen.blit(text_surface, text_rect)
        pygame.display.update(self.attach_button_rect)
    
    '''
    Handles drawing the pass button.

    return: None
    '''
    def draw_pass_button(self, mouse_pos):
        normal, hover = (0, 0, 200), (100, 100, 255)
        color = hover if self.pass_button_rect.collidepoint(mouse_pos) else normal
        pygame.draw.rect(self.screen, color, self.pass_button_rect, border_radius=10)
        text_surface = self.font.render("Pass", True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.pass_button_rect.center)
        self.screen.blit(text_surface, text_rect)
        pygame.display.update(self.pass_button_rect)

    '''
    Handles drawing the input box (for entering card indexes).

    return: None
    '''
    def draw_input_box(self):
        # Draw the input rectangle and the current text.
        pygame.draw.rect(self.screen, (200, 200, 200), self.input_box_rect)
        pygame.draw.rect(self.screen, (0, 0, 0), self.input_box_rect, 2)
        text_surface = self.font.render(self.active_input_text, True, (0, 0, 0))
        self.screen.blit(text_surface, (self.input_box_rect.x + 5, self.input_box_rect.y + 5))
        pygame.display.update(self.input_box_rect)

    '''
    Handles drawing the text that displays whose turn it is.

    return: None
    '''
    def draw_turn_info(self):
        turn_text = f"Turn: Player {self.game.state.current_player.name}"
        text_surface = self.font.render(turn_text, True, (0, 0, 0))
        # Adjust the position as needed
        self.screen.blit(text_surface, (425, 20))

    '''
    Handles drawing the text that displays how many points each player has.

    return: None
    '''
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

    '''
    Handles drawing the text that displays how much energy current player has.

    return: None
    '''
    def draw_energy(self):
        self.screen.blit(self.font.render(f"Current Energy: {self.game.state.current_player.energy}", True, (0, 0, 0)), (850, 570))

    '''
    Handles drawing the text that displays the move of the active card.

    return: None
    '''
    def draw_active_card_move(self):
        if self.game.state.current_player.active_card is not None:
            self.screen.blit(self.font.render(f"Active Card Move: {self.game.state.current_player.active_card.moves[0]}", True, (0, 0, 0)), (20, self.screen.get_height() - 180))

    '''
    Handles drawing the active card text for each player.

    return: None
    '''
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

    '''
    Handles drawing the current player's hand.

    return: None
    '''
    def draw_hand_options(self):
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

    '''
    Handles drawing the bench for each player.

    return: None
    '''
    def draw_benched_cards(self):
        # Draw Player A's bench underneath active card (active card drawn at (20, 110))
        bench_text_surface_a = self.font.render("Bench:", True, (0, 0, 0))
        self.screen.blit(bench_text_surface_a, (20, 150))
        player_a_bench = self.game.state.playerA.benched_cards
        for index, card in enumerate(player_a_bench):
            card_text = f"{index + 1}: {card.name} (HP: {card.hp})"
            text_surface = self.font.render(card_text, True, (0, 0, 0))
            self.screen.blit(text_surface, (20, 180 + index * 20))

        # Draw Player B's bench underneath active card (active card drawn at (650, 110))
        bench_text_surface_b = self.font.render("Bench:", True, (0, 0, 0))
        self.screen.blit(bench_text_surface_b, (650, 150))
        player_b_bench = self.game.state.playerB.benched_cards
        for index, card in enumerate(player_b_bench):
            card_text = f"{index + 1}: {card.name} (HP: {card.hp})"
            text_surface = self.font.render(card_text, True, (0, 0, 0))
            self.screen.blit(text_surface, (650, 180 + index * 20))

    '''
    Handles the attack action.

    return: None
    '''
    def attack_action(self):
        current_card = self.game.state.current_player.active_card
        if current_card is not None:
            # Load the tackle sound and set its volume to maximum (1.0)
            tackle_sound = pygame.mixer.Sound('sounds/Tackle.mp3')
            tackle_sound.set_volume(1.0)
            tackle_sound.play()
            try:
                if 0 <= 0 < len(current_card.moves):
                    move = current_card.moves[0]
                    players = self.game.state.get_player_list()
                    other_player = players[0] if self.game.state.current_player != players[0] else players[1]
                    attack_message = current_card.attack(other_player.active_card, move)
                    self.game.state.change_player()
                    self.set_message(attack_message)
                else:
                    self.set_message("The specified move is not valid for the active card")
            except Exception as ex:
                self.set_message("Attack error: " + str(ex))
        else:
            self.set_message("You cannot attack without an active card")

    '''
    Handles event logic for UI inputs.

    return: None
    '''
    def events(self):
        mouse_pos = pygame.mouse.get_pos()
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
                    self.input_box_rect = pygame.Rect(self.input_box_rect_positions[0][0], self.input_box_rect_positions[0][1], self.input_box_rect.width, self.input_box_rect.height)
                elif self.draw_button_rect.collidepoint(event.pos):
                    res = self.game.state.current_player.draw_card()
                    if res is not None:
                        self.set_message(res)
                        self.should_draw_message = True
                    else:
                        self.should_draw_message = False
                        self.game.state.change_player()
                elif self.bench_button_rect.collidepoint(event.pos):
                    if len(self.game.state.current_player.benched_cards) < 3:
                        self.input_active = True
                        self.current_input_src = self.bench_button_rect
                        self.active_input_text = ""
                        self.input_box_rect = pygame.Rect(self.input_box_rect_positions[1][0], self.input_box_rect_positions[1][1], self.input_box_rect.width, self.input_box_rect.height)
                    else:
                        self.set_message("Your bench is already full.")
                elif self.attach_button_rect.collidepoint(event.pos):
                    if self.game.state.current_player.active_card is None and len(self.game.state.current_player.benched_cards) == 0: 
                        self.set_message("You must have an active or benched card to attach energy.")
                    elif self.game.state.current_player.energy <= 0:
                        self.set_message("You have no energy to attach to a card.")
                    else:
                        self.input_active = True
                        self.current_input_src = self.attach_button_rect
                        self.active_input_text = ""
                        self.input_box_rect = pygame.Rect(self.input_box_rect_positions[2][0], self.input_box_rect_positions[2][1], self.input_box_rect.width, self.input_box_rect.height)
                        self.should_draw_message = False
                elif self.pass_button_rect.collidepoint(event.pos):
                    self.game.state.change_player()
            elif event.type == pygame.KEYDOWN and self.input_active:
                if event.key == pygame.K_RETURN:
                    # Finalize input and attempt to set the active card.
                    try:
                        if self.current_input_src is self.active_button_rect:
                            index = int(self.active_input_text)
                            res = self.game.state.current_player.set_active_from_bench(index - 1)
                            if res is not None:
                                self.set_message(res)
                            else:
                                self.should_draw_message = False
                        elif self.current_input_src is self.bench_button_rect:
                            index = int(self.active_input_text)
                            res = self.game.state.current_player.bench_card(index)
                            if res is not None:
                                self.set_message(res)
                            else:
                                self.should_draw_message = False
                        elif self.current_input_src is self.attach_button_rect:
                            index = int(self.active_input_text)
                            if index == 0 and self.game.state.current_player.active_card is not None: 
                                self.game.state.current_player.active_card.attach_energy()
                                self.game.state.current_player.energy -= 1
                            else:
                                if len(self.game.state.current_player.benched_cards) > 0 and index - 1 < len(self.game.state.current_player.benched_cards):
                                    self.game.state.current_player.benched_cards[index - 1].attach_energy()
                                    self.game.state.current_player.energy -= 1
                                else:
                                    self.set_message("You must enter a valid index.")
                    except ValueError:
                        self.set_message("Please enter a valid integer for the card index")
                    self.input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    self.active_input_text = self.active_input_text[:-1]
                else:
                    self.active_input_text += event.unicode
   
    '''
    The main loop of the game.

    return: None
    '''
    def run(self):
        # Start battle phase music
        pygame.mixer.music.load("sounds/battle.mp3")
        pygame.mixer.music.set_volume(0.3)  # Lower volume for background music
        pygame.mixer.music.play(-1)
        
        while self.running:
            self.events()
            mouse_pos = pygame.mouse.get_pos()
            # Draw the background image
            self.screen.blit(self.bg_image, (0, 0))

            self.draw_turn_info()
            self.draw_points()
            self.draw_active_cards()
            self.draw_hand_options()
            self.draw_benched_cards()
            self.draw_attack_button(mouse_pos)
            self.draw_active_button(mouse_pos)
            self.draw_draw_button(mouse_pos)
            self.draw_bench_button(mouse_pos)
            self.draw_attach_button(mouse_pos)
            self.draw_pass_button(mouse_pos)
            self.draw_energy()
            self.draw_active_card_move()
            
            if self.input_active:
                self.draw_input_box()
            
            if self.should_draw_message:
                self.draw_message()

            # Winning condition check...
            if self.game.state.playerA.points >= 3 or self.game.state.playerB.points >= 3:
                self.should_draw_game_ui = False
                
                winner = "Player A" if self.game.state.playerA.points >= 3 else "Player B"
                self.set_message(f"{winner} won!")
                self.draw_message(425, self.screen.get_height() // 2)
            
            pygame.display.flip()
            pygame.time.delay(100)


if __name__ == '__main__':
    game_app = PokemonCardGame()
    game_app.run()