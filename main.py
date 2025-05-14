import pygame
from Chess_game.constants import *
from Chess_game.game import Game

pygame.init()
pygame.font.init()
font = pygame.font.SysFont(None, 72)
clock = pygame.time.Clock()

Win = pygame.display.set_mode((Width, Height))

def get_position(x,y):
    row=y//Square
    col=x//Square
    return row,col

def main():
    run = True
    game_over = False
    FPS = 60
    game = Game(Width, Height, Rows, Cols, Square, Win)
    while run:
        clock.tick(FPS)
        if not game_over:
            game.update_window()
            if not game_over and game.check_game():
                game_over = True

        else:
            overlay = pygame.Surface((Width, Height))
            overlay.set_alpha(150)
            overlay.fill((0, 0, 0))
            Win.blit(overlay, (0, 0))

            if game.turn == White:
                msg = "Les noirs gagnent !"
            else:
                msg = "Les blancs gagnent !"
            text_surf = font.render(msg, True, White)
            text_rect = text_surf.get_rect(center=(Width//2, Height//2))
            Win.blit(text_surf, text_rect)

            pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and game_over:
                    game.reset()
                    game_over = False
                
            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                if pygame.mouse.get_pressed()[0]:
                    location = pygame.mouse.get_pos()
                    row, col = get_position(location[0], location[1])
                    game.select(row, col)

    pygame.quit()

if __name__ == "__main__":
    main()