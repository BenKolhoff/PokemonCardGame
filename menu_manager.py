import pygame
import pygame_gui

class MenuManager:
    def __init__(self, game, screen_size, ui_manager):
        self.game = game
        self.SCREEN_SIZE = screen_size
        self.ui_manager = ui_manager
        self.current_elements = []

    def flush_elements(self):
        for element in self.current_elements:
            element.kill()

    def create_start_menu(self):
        self.flush_elements()

        start_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(((self.SCREEN_SIZE[0] / 2) - 100, 275), (200, 50)), text='Start', manager=self.ui_manager)
        self.current_elements.append(start_button)

        return self.current_elements

    def create_game_menu(self):
        self.flush_elements()

        current_player_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(((self.SCREEN_SIZE[0] / 2) - 100, 0), (200, 50)), text=f'Current Player: Player {self.game.state.current_player.name}', manager=self.ui_manager)
        self.current_elements.append(current_player_label)

        return self.current_elements