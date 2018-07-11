import random
import numpy as np

def create_table():
    """Create an invisible table with 10 randomly assigned bombs"""
    sample_list =[]
    a = [range((11*i+1),(11*i+10)) for i in range(1,10)]
    for i in range(9):
        for j in range(9):
            sample_list.append(a[i][j])
    bombs_id = np.array(random.sample(sample_list,10))
    pos_col = bombs_id % 11 # get the col index
    pos_row = bombs_id / 11 # get the row index
    table = np.zeros((11,11), int)
    table[pos_row,pos_col] = 9 # creat an assistant board to determine the position of bombs
    return table

class Cell:
    """Set up a class Cell to give properties to each cell"""
    def __init__(self, nrow, ncol, table):
        self.row = nrow # row index of the cell
        self.col = ncol # column index of the cell
        self.visible = False
        self.flag = False
        self.bomb = table[nrow][ncol] # if the value of this cell is 9, then it is a bomb.

    def num_nearby(self, table):
        """calculate the number of bombs near each cell"""
        num = 0
        if self.bomb == 9:
            num = 9 # indicates it is a bomb
            return num
        else:
            if (self.row in range(1,10)) & (self.col in range(1,10)):
                for i in range(self.row-1,self.row+2):
                    for j in range(self.col-1,self.col+2):
                        if table[i][j] == 9:
                            num += 1
            return num

def create_base(table):
    """Create a list of cells containing properties from class Cell"""
    base = []
    for i in range(1,10):
        for j in range(1,10): # loop by row first
            base.append(Cell(i, j, table))
    return base # the base include all information about each cell

def input_check(move):
    """Check whether the input is valid."""
    if str(len(move)) not in "2 3":
        print  "Invalid input! You should type in 2 or 3 characters."
        return False
    elif str(len(move)) == "2":
        try:
            [int(i) for i in move]
        except ValueError:
            print "Invalid input! You should only type in 2 digits or 'f' plus 2 digits."
            return False
        for i in range(2):
            if move[i] not in "1 2 3 4 5 6 7 8 9":
                print "Invalid input! You should only type in row or column index from 1 to 9."
                return False
    else:
        if move[0] !="f":
            print "Invalid input! You should only type in 2 digits or 'f' plus 2 digits."
            return False
        else:
            for i in range(1,3):
                if move[i] not in "1 2 3 4 5 6 7 8 9":
                    print "Invalid input! You should only type in row or column index from 1 to 9."
                    return False
    return True

def is_available(m_pos, base):
    """Check whether the cell chosen by user is available"""
    visible_status = [i.visible for i in base]
    flag_status = [i.flag for i in base]
    ava = True
    if len(m_pos) == 2: # user wants to go to there
        id_num =  (int(m_pos[0]) - 1) * 9 + (int(m_pos[1]) - 1)
        if visible_status[id_num] == True or flag_status[id_num] == True:
            print "You have revealed that cell or that cell is flagged, please choose another one"
            ava = False
    else: # user wants to mark there
        if sum(flag_status) == 10:
            print "You are only allowed to mark at most 10 cells"
            ava = False
        else:
            id_num = (int(m_pos[1]) - 1) * 9 + (int(m_pos[2]) - 1)
            if visible_status[id_num] == True:
                print "You have revealed that cell, please flag another one"
                ava = False
    return ava

def next_action(base):
    """Ask the user to type in their action, check the input and return the position list they want to go."""
    print "Please enter the row index first ( choose one in 1 ~ 9 ),\nThen type in column index ( choose from 1 ~ 9 ).\nIf you want to put or remove a flag , please type in 'f' before the cell . eg, f12."
    move = raw_input("Please enter your move now :")
    m_pos = [i for i in move]
    judge = input_check(m_pos) # check whether the input is valid
    while not judge:
        move = raw_input("Please enter your move again :")
        m_pos = [i for i in move]
        judge = input_check(m_pos)
    ava = is_available(m_pos, base) # check whether the input is available
    while not ava:
        move = raw_input("Please enter your move again :")
        m_pos = [i for i in move]
        ava = is_available(m_pos, base)
    return m_pos # a list of input which is avaliable and valid

def end_or_not(m_pos, base):
    """check whether the game ends or not. Print "you win" or "you lose" if game ends"""
    judge = True
    if len(m_pos) == 2: # check whether the user is lose
        id_num =  (int(m_pos[0]) - 1) * 9 + (int(m_pos[1]) - 1)
        if base[id_num].bomb == 9:
            print "You lose."
            judge = False
    # check whether the user is win
    visible_status = [i.visible for i in base]
    bomb = [i.bomb for i in base]
    index = [i for i in range(81) if bomb[i] != 9] # the index for all cell without bomb
    if sum([visible_status[i] for i in index]) == 71:
        print "You win !"
        judge = False
    return judge

def update_list(m_pos, base):
    """update the base list after each step"""
    if len(m_pos) == 2:
        id_num = (int(m_pos[0]) - 1) * 9 + (int(m_pos[1]) - 1)
        base[id_num].visible = True
    else:
        id_num = (int(m_pos[1]) - 1) * 9 + (int(m_pos[2]) - 1)
        base[id_num].flag = not base[id_num].flag
    return base

def print_broad(base, table):
    """print the updated table"""
    visible_status = [i.visible for i in base]
    flag_status = [i.flag for i in base]
    nearby = [i.num_nearby(table) for i in base]
    print "    1   2   3   4   5   6   7   8   9 "
    for i in range(9): # row index
        print " "," ---" * 9
        print i+1,
        for j in range(8):
            id_num = i * 9 + j
            if visible_status[id_num] == True:
                print "|",nearby[(i*9+j)],
            elif flag_status[id_num] == True:
                print "|","F",
            else:
                print "|  ",
        j= 8
        id_num = i * 9 + j
        if visible_status[id_num] == True:
            print "|",nearby[(i*9+j)],"|"
        elif flag_status[id_num] ==True:
            print "|","F","|"
        else:
            print "|  ","|"
    print " "," ---" * 9

def restart():
    """Check whether the user wants to play again"""
    restart = raw_input("Do you want to restart the game ? please choose 'yes' or 'no'")
    while (restart != "yes") and (restart != "no"):
       restart = raw_input("Invalid input! please type 'yes' or 'no'.")

    if restart == "yes":
        return True
    else:
        return False

def main():
    """Combine all the other functions and start the game"""
    program = True
    while program == True:
        table = create_table()
        base = create_base(table)

        print "Welcome to this Minesweeper Game !"
        print "The Following is basic rule of this game:"
        print "You are allowed to type in a position of a cell "
        print "Please enter the row index first ( choose one in 1 ~ 9 ),\nThen type in column index ( choose from 1 ~ 9 ).\nIf you want to put or remove a flag , please type in 'f' before the cell . eg, f12."
        print "Here is the board :"

        print_broad(base,table)

        print "Let's begin !"

        game = True
        while game == True:
            m_pos = next_action(base)
            base = update_list(m_pos, base)
            continue_game =end_or_not(m_pos, base)
            if continue_game:
                print_broad(base,table)
            else:
                game = False
                print "Here is the position of mines"
                print "    1   2   3   4   5   6   7   8   9 "
                print " "," ---" * 9
                bomb = [i.bomb for i in base]
                for i in range(9): # row index
                    print i+1,
                    for j in range(8):
                        id_num = i * 9 + j
                        if bomb[id_num] == 9:
                            print "|","*",
                        else:
                            print "|  ",
                    j= 8
                    id_num = i * 9 + j
                    if bomb[id_num] == 9:
                        print "|","*","|"
                    else:
                        print "|  ","|"
                    print " "," ---" * 9
                choice = restart()
                if not choice: # the user wants to quit
                    print " Goodbye!"
                    program = False

if __name__ == "__main__":
    main()

