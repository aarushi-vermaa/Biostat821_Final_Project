"""Tic Tac Toe Game"""

import numpy as np
import sys
from typing import List, Dict, Tuple, Union


class tic_tac_toe:
    """Tic Tac Toe Class."""

    def __init__(self) -> None:
        """Initiate Class."""
        self.board = np.array([["", "", ""], ["", "", ""], ["", "", ""]])

        self.place_maps = {
            1: (0, 0),
            2: (0, 1),
            3: (0, 2),
            4: (1, 0),
            5: (1, 1),
            6: (1, 2),
            7: (2, 0),
            8: (2, 1),
            9: (2, 2),
        }

        # keys are comp_turn arguement
        # values are list of list
        # the first list is list of board states
        # the second list corresponds to the
        # minimax for the board states in the
        # first list
        self.minimax_cache: Dict[bool, List[Union[List[], List[]]]] = {
            False: [[], []],
            True: [[], []],
        }

        self.game_mode = input(
            "Would you like to play against the computer or another player?\
(Answer: Computer/Player):  "
        )
        # keep asking until user gives the a desired anwer without throwing an error
        while self.game_mode not in ["Computer", "Player"]:
            print("Please respond with either 'Computer' or 'Player'")
            self.game_mode = input(
                "Would you like to play against the computer or another player?\
(Answer: Computer/Player):  "
            )

        # create game players in accordance with the game mode
        if self.game_mode == "Computer":
            self.player_maps = {"User": "X", "Computer": "O"}
        else:
            self.player_maps = {"Player 1": "X", "Player 2": "O"}

        self.players = list(self.player_maps.keys())
        self.player_turn = np.random.choice(self.players)
        self.turns_played = 0
        self.score_board = {self.players[0]: 0, self.players[1]: 0, "Ties": 0}

    def check_in_cache(
        self, board_state: np.ndarray, Comp_turn: bool
    ) -> Union[int, str]:
        """Check if minimax for a particular board state for a
        Comp_turn has been calculated. If yes return the minimax value.
        Else return Not found."""
        for i in range(len(self.minimax_cache[Comp_turn][0])):
            if np.array_equiv(self.minimax_cache[Comp_turn][0][i], board_state):
                return self.minimax_cache[Comp_turn][1][i]
        return "Not found"

    # during the game we ask users serveral questions
    # like which move to play. If user accidentaly answers something
    # wrong, this method will ask the user to answer again. Otherwise,
    # the game would end prematurely and the user would have to start over.
    def ask_question(self, input_string: str, desired_answers: List[str]) -> str:
        """Ask user the question and keep asking until answered correctly."""
        answer = input(input_string)
        while answer not in desired_answers:
            print("Please respond with one of the following: ", desired_answers)
            answer = input(input_string)
        return answer

    def change_player(self) -> None:
        """Change the game player who is taking turn."""
        # count the number of turns played
        if self.player_turn == self.players[0]:
            self.player_turn = self.players[1]
        else:
            self.player_turn = self.players[0]

    def check_repeating_letter(self, a: np.ndarray) -> bool:
        """Check if an array has all the same letter."""
        flag = True
        for i in range(1, len(a)):
            if a[i] != a[i - 1]:
                flag = False
                return flag
        return flag

    def diagonal(self) -> Tuple[np.ndarray, np.ndarray]:
        """Create the two diagonals of the board."""
        diagonal1 = []
        diagonal2 = []
        for i in range(3):
            for j in range(3):
                if i == j:
                    diagonal1.append(self.board[i, j])
                    diagonal_1 = np.array(diagonal1)
                if i + j == 2:
                    diagonal2.append(self.board[i, j])
                    diagonal_2 = np.array(diagonal2)
        return diagonal_1, diagonal_2

    def create_check_arrays(self) -> List[np.ndarray]:
        """Create arrays that need to be checked to determine if the game is over"""
        check_these = []
        for i in range(3):
            if ("O" in self.board[:, i]) or ("X" in self.board[:, i]):
                check_these.append(self.board[:, i])
            if ("O" in self.board[i, :]) or ("X" in self.board[i, :]):
                check_these.append(self.board[i, :])
        diagonal_1, diagonal_2 = self.diagonal()
        if ("O" in list(diagonal_1)) or ("X" in list(diagonal_1)):
            check_these.append(diagonal_1)
        if ("O" in list(diagonal_2)) or ("X" in list(diagonal_2)):
            check_these.append(diagonal_2)
        return check_these

    def isTie(self) -> bool:
        """Check if it's a tie."""
        if "" not in self.board:
            return True
        else:
            return False

    def check_game_over(self) -> bool:
        """Check if the game is over."""
        arr_tb_check = self.create_check_arrays()
        if len(arr_tb_check) > 0:
            for i in arr_tb_check:
                if self.check_repeating_letter(i):
                    return True
            if self.isTie():
                return True
        return False

    # will only work if game is over
    def winning_player(self) -> str:
        """Return the winning player."""
        arr_tb_check2 = self.create_check_arrays()
        if self.isTie():
            return "Tie"
        else:
            for i in arr_tb_check2:
                if self.check_repeating_letter(i):
                    if np.unique(i)[0] == self.player_maps[self.players[0]]:
                        return self.players[0]
                    elif np.unique(i)[0] == self.player_maps[self.players[1]]:
                        return self.players[1]

    # a recursive function
    # aims to maximie computer rewards but also assumes that the user will always play the optimal move.
    # Computer will play its best move. Then the computer puts itself in users place
    # and place the best move from user's perspective.
    # Then the computer plays its own best move again
    # The Comp_turn is bool arguement that indicates if the computer is playing
    # from a user perspective or a computer perspective.

    def minimax(self, Comp_turn: bool) -> int:
        """Impliment minimax."""
        # if minimax for board state stored in cache
        # return its value else compute minimax
        if self.check_in_cache(self.board, Comp_turn) in [-1, 0, 1]:
            return self.check_in_cache(self.board, Comp_turn)
        else:

            # we define rewards for the computer
            # these rewards are maximised by computer
            # while minimized by user
            if self.check_game_over():
                if self.winning_player() == "Computer":
                    return 1
                elif self.winning_player() == "User":
                    return -1
                elif self.winning_player() == "Tie":
                    return 0
                else:
                    pass
            else:
                # checks if its computer turn or not
                if Comp_turn:
                    # if it is computers turn it will play the move below
                    scores = []
                    # go over each available move
                    for i, j in enumerate(self.board.flatten()):
                        if j == "":
                            # play that move
                            self.board[self.place_maps[i + 1]] = self.player_maps[
                                "Computer"
                            ]
                            # now that computer has played its move
                            # we call minimax again to but with comp_turn as False
                            # so computer plays from a users perpective
                            ans = self.minimax(False)
                            # Add minimax value for the board state to cache
                            self.minimax_cache[False][0].append(self.board.copy())
                            self.minimax_cache[False][1].append(ans)
                            scores.append(ans)
                            # undo the move as the next time the computer is experimenting
                            # with different moves. If we do not undo all the previous hypothetical moves
                            # played will be retained in the board.
                            self.board[self.place_maps[i + 1]] = ""
                    # scores are maximized as the computer is playing that move
                    return max(scores)

                else:
                    # if computer plays from a user perspective then the following is done
                    # all literally the same
                    # plays every possible move from user perspective
                    scores = []
                    for i, j in enumerate(self.board.flatten()):
                        if j == "":
                            self.board[self.place_maps[i + 1]] = self.player_maps[
                                "User"
                            ]
                            # once move is played the minimax below with comp-turn true is called
                            # so the computer than plays its move from its own perspective
                            ans = self.minimax(True)
                            # add minimax value for board state to cache
                            self.minimax_cache[True][0].append(self.board.copy())
                            self.minimax_cache[True][1].append(ans)
                            scores.append(ans)

                            # undo the move
                            self.board[self.place_maps[i + 1]] = ""
                    # as the move is played by the computer from a users perspective
                    # and the fact that user wants to minimize computer scores here
                    # we write computers move
                    return min(scores)

    def computer_play(self) -> int:
        """Plays the computer move."""
        # Minimax function above only keeps track of the scores at each position
        # here we keep track of scores and move to be played.
        # It is the optimal move we want
        # Given the current state if the board, the computer plays each possible move
        # then calls the minimax on board that incorporates that move
        # keeps track of the scores achived on that move
        move = []
        score = []
        for i, j in enumerate(self.board.flatten()):
            if j == "":

                self.board[self.place_maps[i + 1]] = self.player_maps["Computer"]
                move.append(i + 1)
                score.append(self.minimax(False))

                self.board[self.place_maps[i + 1]] = ""
        # returns the best move
        return move[np.argmax(score)]

    def game(self):
        """Plays an episode of the game till the end."""
        while self.check_game_over() == False:
            # played if game.mode is One Player
            # in that case the chunk of code below will
            # play the computers move
            if self.player_turn == "Computer":
                print("\nComputer's Turn")
                # hardcoded part for if computer plays the first turn
                if self.turns_played == 0:
                    self.board[0, 0] = self.player_maps["Computer"]
                elif self.turns_played == 1:
                    print("Computer is thinking...")
                    self.board[
                        self.place_maps[self.computer_play()]
                    ] = self.player_maps["Computer"]
                else:
                    self.board[
                        self.place_maps[self.computer_play()]
                    ] = self.player_maps["Computer"]
                print(self.board)
                if self.check_game_over():
                    break
                self.turns_played += 1
                self.change_player()

            else:
                # the code plays the players move
                # if game.mode is One Player
                # it will play the users move
                # if the game.mode is two players
                # it will play the move of each player
                # one by one
                print(f"\n{self.player_turn}'s Turn")
                potential_moves = [str(i) for i in self.place_maps.keys()]
                move = self.ask_question(
                    "Please enter the position you want to play:  ", potential_moves
                )

                if self.board[self.place_maps[int(move)]] != "":
                    print("INVALID MOVE: position occupied. Please try again.\n")
                    self.game()
                else:
                    self.board[self.place_maps[int(move)]] = self.player_maps[
                        self.player_turn
                    ]

                    print(self.board)
                    self.turns_played += 1
                    self.change_player()

        # now that the game is over we check who wins
        # and add points to the score board accordingly
        if self.winning_player() == "Tie":
            print("Its a Tie")
            self.score_board["Ties"] += 1
        elif self.winning_player() == self.players[0]:
            print(f"{self.players[0]} Won.")
            self.score_board[self.players[0]] += 1
        elif self.winning_player() == self.players[1]:
            print(f"{self.players[1]} Won.")
            self.score_board[self.players[1]] += 1

        # asks if the game needs to be played again.
        self.play_again()

    def reset_game(self) -> None:
        """This will reset the game"""
        self.player_turn = np.random.choice(self.players)
        self.turns_played = 0
        self.board = np.array([["", "", ""], ["", "", ""], ["", "", ""]])

    def play_again(self) -> None:
        """Asks if the player wants to play again or quit the game."""

        # ask if wants to play again
        game_again = self.ask_question(
            "Do you want to play again? (Answer Y/N): ", ["Y", "N"]
        )
        player0wins = self.score_board[self.players[0]]
        player1wins = self.score_board[self.players[1]]
        totalgames = sum(self.score_board.values())

        if game_again == "N":
            # if no more games to be played print the player who won the most games
            if player0wins > player1wins:
                print(
                    f"\n{self.players[0]} won {player0wins} out of {totalgames} game(s). They are the winner!\n"
                )
            elif player0wins < player1wins:
                print(
                    f"\n{self.players[1]} won {player1wins} out of {totalgames} game(s). They are the winner!\n"
                )
            else:
                print(
                    f"\n{self.players[0]} and {self.players[1]} won equal number of games.\n"
                )
            # print a farewell line
            print("Hope you enjoyed playing Tic Tac Toe. See you next time. Bye!")
        # if more game to be played than reset the game and play on
        else:
            # after each episode of the game the score board is displayed
            print("\nTotal games Played:", totalgames)
            print(f"Player 1 win count: {player0wins}")
            print(f"Player 2 win count: {player1wins}")
            print(f"Ties: {self.score_board['Ties']}")
            self.reset_game()
            self.game()


if __name__ == "__main__":
    game = tic_tac_toe()
    game.game()
