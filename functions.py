from constants import *

FONT = pygame.font.match_font('arial')


def draw_text(surface, text, size, color, pos):
    x, y = pos
    font = pygame.font.Font(FONT, size)
    text_surface = font.render(text, True, color, YELLOW)
    text_rect = text_surface.get_rect()
    text_rect.topright = (x, y)
    surface.blit(text_surface, text_rect)
