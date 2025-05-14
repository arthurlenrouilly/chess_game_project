import pygame
import os

#Sizeavailable_moves
Width, Height = 760,760
Rows, Cols = 8,8
Square = Width//Rows

#Colors
White =(223,227,230)
Blue = (144,161,172)
Black = (0,0,0)
Grey = (110, 110, 110)

Path = "Chess_game/Chess-pieces"

#Images
#Black pieces
Black_Knight = pygame.transform.scale(pygame.image.load(os.path.join(Path,"Chess_ndt60.png")), (Square, Square))
Black_Bishop = pygame.transform.scale(pygame.image.load(os.path.join(Path, "Chess_bdt60.png")), (Square, Square))
Black_King = pygame.transform.scale(pygame.image.load(os.path.join(Path, "Chess_kdt60.png")), (Square, Square))
Black_Pawn = pygame.transform.scale(pygame.image.load(os.path.join(Path, "Chess_pdt60.png")), (Square, Square))
Black_Queen = pygame.transform.scale(pygame.image.load(os.path.join(Path, "Chess_qdt60.png")), (Square, Square))
Black_Rook = pygame.transform.scale(pygame.image.load(os.path.join(Path, "Chess_rdt60.png")), (Square, Square))
#White pieces
White_Knight = pygame.transform.scale(pygame.image.load(os.path.join(Path, "Chess_nlt60.png")), (Square, Square))
White_Bishop = pygame.transform.scale(pygame.image.load(os.path.join(Path, "Chess_blt60.png")), (Square, Square))
White_King = pygame.transform.scale(pygame.image.load(os.path.join(Path, "Chess_klt60.png")), (Square, Square))
White_Pawn = pygame.transform.scale(pygame.image.load(os.path.join(Path, "Chess_plt60.png")), (Square, Square))
White_Queen = pygame.transform.scale(pygame.image.load(os.path.join(Path, "Chess_qlt60.png")), (Square, Square))
White_Rook = pygame.transform.scale(pygame.image.load(os.path.join(Path, "Chess_rlt60.png")), (Square, Square))
