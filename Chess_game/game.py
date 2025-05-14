import pygame
from .Pieces import King, Rook, Pawn, Queen, Bishop
from .board import newBoard
from .constants import *
from copy import deepcopy

class Game:
    def __init__(self, Width, Height, Rows, Cols, Square, Win):
        self.Width  = Width
        self.Height = Height
        self.Rows   = Rows
        self.Cols   = Cols
        self.Win = Win
        self.Board = newBoard(Width, Height, Rows, Cols, Square, Win)
        self.Square = Square
        self.selected = None
        self.turn = White
        self.valid_moves  = []
        self.Black_pieces_left = 16
        self.White_pieces_left = 16

    def update_window(self):
        self.Board.draw_Board()
        self.Board.draw_pieces()
        self.draw_available_moves()
        pygame.display.update()

    def reset(self):
        self.Board = newBoard(self.Width, self.Height, self.Rows, self.Cols, self.Square, self.Win)
        self.turn = White
        self.valid_moves = []
        self.Black_pieces_left = 16
        self.White_pieces_left = 16
        self.selected = None

    def check_game(self):
        if self.checkmate(self.Board):
            if self.turn == White :
                print ("Les noirs gagnent !")
            else: 
                print ("Les blancs gagnent !")
            return True
        return False

    def enemies_moves(self, piece, Board):
        enemies_moves = []
        for r in range(len(Board)):
            for c in range(len(Board[r])):
                if Board[r][c] != 0:
                    if Board[r][c].color != piece.color:
                        moves = Board[r][c].get_available_moves(r,c, Board)
                        for move in moves:
                            enemies_moves.append(move)
        return enemies_moves

    def get_King_pos(self, Board):
        for r in range(len(Board)):
            for c in range(len(Board)):
                if Board[r][c] != 0:
                    if Board[r][c].type == "King" and Board[r][c].color == self.turn:
                        return (r,c)

    def simulate_move(self, piece, row, col):
        piece_row, piece_col = piece.row, piece.col
        save_piece = self.Board.Board[row][col]

        if self.Board.Board[row][col] != 0:
            self.Board.Board[row][col] = 0

        self.Board.Board[piece.row][piece.col], self.Board.Board[row][col] = self.Board.Board[row][col], self.Board.Board[piece.row][piece.col]

        king_pos = self.get_King_pos(self.Board.Board)
        if king_pos in self.enemies_moves(piece, self.Board.Board):
            piece.row, piece.col = piece_row, piece_col
            self.Board.Board[piece_row][piece_col] = piece
            self.Board.Board[row][col] = save_piece
            return False
        
        piece.row, piece.col = piece_row, piece_col
        self.Board.Board[piece_row][piece_col] = piece
        self.Board.Board[row][col] = save_piece
        return True

    def possible_moves(self, Board):
        possible_moves = []
        for r in range(len(Board)):
            for c in range(len(Board[r])):
                if Board[r][c] != 0:
                    if Board[r][c].color == self.turn and Board[r][c].type != "King":
                        moves = Board[r][c].get_available_moves(r,c, Board)

                        for move in moves :
                            possible_moves.append(move)
        return possible_moves

    def checkmate(self, Board):
        king_pos = self.get_King_pos(Board.Board)
        king_piece = Board.get_piece(king_pos[0], king_pos[1])

        attacked = set(self.enemies_moves(king_piece, Board.Board))
        if king_pos not in attacked:
            return False

        legal_king_moves = set(king_piece.get_available_moves(king_pos[0], king_pos[1], Board.Board)) - attacked
        if legal_king_moves:
            return False

        attackers = []
        for r in range(self.Rows):
            for c in range(self.Cols):
                p = Board.Board[r][c]
                if p != 0 and p.color != self.turn:
                    if king_pos in p.get_available_moves(r, c, Board.Board):
                        attackers.append((r, c, p))
        if len(attackers) >= 2:
            return True

        ar, ac, ap = attackers[0]
        path = [(ar, ac)]
        if ap.type in ("Rook", "Bishop", "Queen"):
            dr = king_pos[0] - ar
            dc = king_pos[1] - ac
            step_r = (dr and (dr // abs(dr))) or 0
            step_c = (dc and (dc // abs(dc))) or 0
            rr, cc = ar + step_r, ac + step_c
            while (rr, cc) != king_pos:
                path.append((rr, cc))
                rr += step_r; cc += step_c

        for r in range(self.Rows):
            for c in range(self.Cols):
                p = Board.Board[r][c]
                if p != 0 and p.color == self.turn and not isinstance(p, King):
                    for move in p.get_available_moves(r, c, Board.Board):
                        if move in path:
                            return False

        return True

    def change_turn(self):
        if self.turn == White:
            self.turn = Black
        else:
            self.turn = White

    def select(self, row, col):
        if self.selected:
            move = self._move(row, col)
            if not move:
                self.selected = None
                self.select(row, col)
        piece = self.Board.get_piece(row, col)
        if piece != 0 and self.turn == piece.color:
            self.selected = piece
            self.valid_moves = piece.get_available_moves(row, col, self.Board.Board)
        if isinstance(self.selected, King):
            self.add_castling_moves(self.selected)

    def _move(self, row, col):
        target = self.Board.get_piece(row, col)
        if not self.selected or (row, col) not in self.valid_moves:
            return False

        if isinstance(self.selected, King) and abs(col - self.selected.col) == 2:
            if not self.simulate_move(self.selected, row, col):
                return False

            if col > self.selected.col:
                rook_start, rook_end = 7, col - 1
            else:
                rook_start, rook_end = 0, col + 1

            rook = self.Board.get_piece(self.selected.row, rook_start)
            self.Board.move(self.selected, row, col)
            self.Board.move(rook, row, rook_end)

        else:
            if not self.simulate_move(self.selected, row, col):
                return False
            self.remove(self.Board.Board, target, row, col)
            self.Board.move(self.selected, row, col)

            if isinstance(self.selected, Pawn):
                if (self.selected.color == White and row == 0) or (self.selected.color == Black and row == self.Rows - 1):
                    promoting = White_Queen if self.selected.color == White else Black_Queen
                    self.Board.Board[row][col] = Queen(self.Square, promoting, self.selected.color, "Queen", row, col)
        
        self.change_turn()
        self.valid_moves = []
        self.selected = None
        return True

    
    def remove(self, board, piece, row, col):
        if piece != 0:
            board[row][col] = 0
            if piece.color == White:
                self.White_pieces_left -= 1
            else:
                self.Black_pieces_left -= 1

    def draw_available_moves(self):
        if len(self.valid_moves) > 0:
            for pos in self.valid_moves:
                row,col = pos[0],pos[1]
                pygame.draw.circle(self.Win, Grey, (col*self.Square + self.Square//2, row*self.Square + self.Square//2),self.Square//8)

    def get_board(self):
        return self.Board.Board
    
    def add_castling_moves(self, king):
        row, col = king.row, king.col
        if not king.first_move:
            return

        attacked = set(self.enemies_moves(king, self.Board.Board))
        if (row, col) in attacked:
            return

        if all(self.Board.Board[row][c] == 0 for c in range(1, col)):
            rook = self.Board.get_piece(row, 0)
            if isinstance(rook, Rook) and rook.first_move:
                path = [(row, col-1), (row, col-2)]
                if not any(p in attacked for p in path):
                    self.valid_moves.append((row, col-2))

        if all(self.Board.Board[row][c] == 0 for c in range(col+1, 7)):
            rook = self.Board.get_piece(row, 7)
            if isinstance(rook, Rook) and rook.first_move:
                path = [(row, col+1), (row, col+2)]
                if not any(p in attacked for p in path):
                    self.valid_moves.append((row, col+2))
