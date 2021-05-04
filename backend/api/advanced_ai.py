from api.chess_game import ChessGame
from api.piece.piece_interface import Color
import math


class AdvancedAI:
    """
    Implements an easy computer AI to play against the user
    """
    def __init__(self, game: ChessGame):
        self.best_move = None
        self.game = game
        self.values = {"p": -1.0, "P": 1.0,
                       "n": -3.25, "N": 3.25,
                       "b": -3.5, "B": 3.5,
                       "r": -5.0, "R": 5.0,
                       "q": -9.75, "Q": 9.75,
                       "k": -100, "K": 100,
                       "1": 0, "2": 0,
                       "3": 0, "4": 0,
                       "5": 0, "6": 0,
                       "7": 0, "8": 0,
                       "/": 0}

    def game_evaluation(self, color: Color):
        index = 0
        score = 0
        while self.game.fen[index] != ' ':
            score += self.values[self.game.fen[index]]
            index += 1

        if color == Color.BLACK:
            return -score
        else:
            return score

    def get_next_move(self, depth=3):
        self.min_max_search(self.game, depth, self.game.turn, math.inf, -math.inf, True)
        # print(self.min_max_search2(self.game, depth, self.game.turn))
        return self.best_move[0][0], self.best_move[0][1], self.best_move[1][0], self.best_move[1][1]

    def min_max_search(self, game: ChessGame, depth: int, maximize_color: Color, parent_max: int, parent_min: int,
                       first_move: bool):
        board = game.board
        game_status = game.check_game_status()
        if not depth or game_status != 'Continue':
            if (game_status == "BlackLoss" and maximize_color == Color.WHITE) or (game_status == "WhiteLoss" and
                                                                                  maximize_color == Color.BLACK):
                return math.inf
            ret = self.game_evaluation(maximize_color)
            return ret
        else:
            turn = game.turn

            if turn == maximize_color:
                max_score = parent_min
                for row in range(8):
                    for col in range(8):
                        piece = board[row][col]
                        if piece.color == turn:
                            moves = piece.get_checked_moves()["moves"]
                            src = (row, col)
                            for tar in moves:
                                game.update(src, tar, 'Queen', is_ai=True)
                                child_score = self.min_max_search(game, depth - 1, maximize_color, parent_max, max_score, False)
                                game.undo()
                                if child_score > max_score:
                                    if first_move:
                                        self.best_move = [src, tar]
                                    max_score = child_score
                                if max_score > parent_max:
                                    return parent_max
                return max_score
            else:
                min_score = parent_max
                for row in range(8):
                    for col in range(8):
                        piece = board[row][col]
                        if piece.color == turn:
                            moves = piece.get_checked_moves()["moves"]
                            src = (row, col)
                            for tar in moves:
                                game.update(src, tar, 'Queen', is_ai=True)
                                child_score = self.min_max_search(game, depth - 1, maximize_color, min_score, parent_min, False)
                                game.undo()
                                if child_score < min_score:
                                    if first_move:
                                        self.best_move = [src, tar]
                                    min_score = child_score
                                if min_score < parent_min:
                                    return parent_min
                return min_score

    def min_max_search2(self, game: ChessGame, level: int, maximize_color: Color):
        board = game.board
        if not level or game.check_game_status() != 'Continue':
            return self.game_evaluation(maximize_color)
        else:
            turn = game.turn

            if turn == maximize_color:
                max_score = -math.inf
                for row in range(8):
                    for col in range(8):
                        piece = board[row][col]
                        if piece.color == turn:
                            moves = piece.get_checked_moves()["moves"]
                            src = (row, col)
                            for tar in moves:
                                game.update(src, tar, 'Queen', is_ai=True)
                                max_score = max(max_score, self.min_max_search2(game, level - 1, maximize_color))
                                game.undo()
                return max_score
            else:
                min_score = math.inf
                for row in range(8):
                    for col in range(8):
                        piece = board[row][col]
                        if piece.color == turn:
                            moves = piece.get_checked_moves()["moves"]
                            src = (row, col)
                            for tar in moves:
                                game.update(src, tar, 'Queen', is_ai=True)
                                min_score = min(min_score, self.min_max_search2(game, level - 1, maximize_color))
                                game.undo()
                return min_score

