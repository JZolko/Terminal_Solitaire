"""
    This program is based off a variant of traditional solitaire called Aces Up.
    The user starts out with 4 cards and can either move within the tableau, move to
    foundation or have more cards dealt to the tableau.  The game can only be won
    once all colums are aces and have a length of 1.
"""


import cards  # required !!!

RULES = '''
Aces High Card Game:
     Tableau columns are numbered 1,2,3,4.
     Only the card at the bottom of a Tableau column can be moved.
     A card can be moved to the Foundation only if a higher ranked card 
        of the same suit is at the bottom of another Tableau column.
     To win, all cards except aces must be in the Foundation.'''

MENU = '''     
Input options:
    D: Deal to the Tableau (one card on each column).
    F x: Move card from Tableau column x to the Foundation.
    T x y: Move card from Tableau column x to empty Tableau column y.
    R: Restart the game (after shuffling)
    H: Display the menu of choices
    Q: Quit the game        
'''

def init_game():
    
    '''
        This function creates a shuffled deck, a list of 4 cards, each with 
        a length of 1, a foundation, which is an empty list
    '''
    foundation, tableau = [], []
    d = cards.Deck() # uses the imported class
    d.shuffle # shuffles the deck
    stock = d
    for i in range(4): # adds cards to the list
        tableau.append([stock.deal()])
    return (stock, tableau, foundation)  # stub so that the skeleton compiles; delete 
                               # and replace it with your code
    
def deal_to_tableau( stock, tableau ):
        
    '''
        This function adds a card to each column in the tableau
    '''
    for i in range(4):
                tableau[i].append(stock.deal())
            


def display( stock, tableau, foundation ):
    '''Display the stock, tableau, and foundation.'''
    
    print("\n{:<8s}{:^13s}{:s}".format( "stock", "tableau", "  foundation"))
    
    # determine the number of rows to be printed -- determined by the most
    #           cards in any tableau column
    max_rows = 0
    for col in tableau:
        if len(col) > max_rows:
            max_rows = len(col)

    for i in range(max_rows):
        # display stock (only in first row)
        if i == 0:
            display_char = "" if stock.is_empty() else "XX"
            print("{:<8s}".format(display_char),end='')
        else:
            print("{:<8s}".format(""),end='')

        # display tableau
        for col in tableau:
            if len(col) <= i:
                print("{:4s}".format(''), end='')
            else:
                print("{:4s}".format( str(col[i]) ), end='' )

        # display foundation (only in first row)
        if i == 0:
            if len(foundation) != 0:
                print("    {}".format(foundation[-1]), end='')

        print()

def get_option():
    
    '''
        This function prompts the user for an input with correct formatting
        based on the first item entered
    '''
    acceptable = ['D','F','T','R','H','Q'] # the okay inputs
    sing_accept = ['D','R','H','Q'] # the okay inputs that only expect one char
    opt = input("\nInput an option (DFTRHQ): ")
    opt = opt.strip() # strips any spacing
    lst = opt.split() # splits at the spacing
    lst[0] = lst[0].upper() # capitalizes the first letter
    #print(lst[0])
    
    if not opt or (lst[0] in sing_accept and len(lst) != 1): # if the list is longer than one or its a wrong letter
        print("Error in option: ", *lst)
        return None
    if lst[0] not in acceptable: # if its the wrong letter
        print("Error in option: ", *lst)
        return None
    
    if lst[0] == 'F' and ((len(lst) != (2)) or (len(lst) == 2\
        and not(lst[1].isdigit()))): # if its not F and 2 ints
        print("Error in option: ", *lst)
        return None
    
    elif lst[0] == 'F' and len(lst) == (2) and lst[1].isdigit(): # if the input is correct
        return lst
    
    
    if lst[0] == 'T' and (len(lst) != 3 or len(lst) == 3 and\
          not(lst[1].isdigit()) or not(lst[2].isdigit())): # if its T and doesnt have 2 ints
        print("Error in option: ", *lst)
        return None
    
    elif lst[0] == 'T' and len(lst) == 3: # if its the correct input
        return lst
    return lst
    
    
    #return final   # stub; delete and replace with your code

def validate_move_to_foundation( tableau, from_col ):
    
    '''
        This function checks to see if the card can actually be moved to the foundation
        by looking at the suits and ranks of other cards in the tableau
    '''
    
    mov = 0
    if from_col < 1 or from_col > 4:
        print("Error, cannot move {}.".format(from_col))
        return False
    from_col -= 1
    
    try:
        tableau[from_col][-1]
        
        for i in range(4): # goes through the last card in all the columns
            if tableau[i]:    
                if tableau[i][-1].rank() > tableau[from_col][-1].rank()\
                and tableau[i][-1].suit() == tableau[from_col][-1].suit()\
                and tableau[from_col][-1].rank() != 1 and i != from_col: # if theres a larger card of the same suit
                    mov += 1
                if tableau[i][-1].rank() == 1 and tableau[from_col][-1].rank() != 1\
                and tableau[from_col][-1].suit() == tableau[i][-1].suit(): # if the card is an ace and of the same suit
                    mov += 1
                    
        if mov == 0: # if there arent any moves available
            print("Error, cannot move {}.".format(tableau[from_col][-1]))
            return False
        else: # if you can move it
            
            return True
        

    except:
        print("Error, empty column:")
        return False
    #return False  # stub; delete and replace it with your code   

def move_to_foundation( tableau, foundation, from_col ):
    
    '''
        This function moves the movable card from the tableau to the foundation
    '''
    valid = validate_move_to_foundation(tableau, from_col)
    if valid: # if the card is movable
        from_col -= 1
        move = tableau[from_col].pop() # removes from tableau
        foundation.append(move) # adds to foundation

def validate_move_within_tableau( tableau, from_col, to_col ):
    
    '''
        This function checks to see if a card can be moved within the tableau
        A card can only be moved to an empty column
    '''
    mov = 0
    if from_col < 1 or from_col > 4: # if the input is out of the column range
        print("Invalid move")
        return False
    from_col -= 1
    
    if to_col < 1 or to_col > 4:
        print("Invalid move")
        return False
    to_col -= 1
    
    try:
 
        if not(tableau[to_col]) and tableau[from_col][-1]: # if the to column is empty and the from column isnt
            mov += 1
        if mov > 0:
            return True
        else:
            print("Invalid move")
            return False
        
    except:
        print("Invalid move")
        return False



def move_within_tableau( tableau, from_col, to_col ):
    
    '''
        This function moves a card from one column to another within the tableau
    '''
    valid = validate_move_within_tableau(tableau, from_col, to_col)
    from_col -= 1
    to_col -= 1
    if valid: # if the move is valid
        mov = tableau[from_col].pop() # takes it from the from column
        tableau[to_col].append(mov) # adds it to the to column


        
def check_for_win( stock, tableau ):
    
    '''
        This function checks to see if the user has won the game.
        They can only take the W if each column only contains
        one ace and the stock has to be empty
    '''
    w = 0
    try:
        for i in range(len(tableau)): # goes through each column and checks for aces
            if tableau[i][0].rank() == 1 and len(tableau[i]) == 1 and not(stock):
                w += 1 # if the column only has an ace
    except: 
        return False 
    if w == 4: # if the former condition is true for all columns
        return True
    else:
        return False
        
def main():
        
    '''
        This is what the user interacts with * where the magic happens *
        The user is given a menu and some rules to try and win the game
    '''
    stock, tableau, foundation = init_game()
    acceptable = ['D','F','T','R','H','Q'] # the good inputs
    print( MENU )
    display( stock, tableau, foundation ) # displays the stock tableau and foundation

    #init_game()
    while True:
        
        opt = get_option() # gets an input from the user
        
        #print(opt)    
        try:
            opt[0]
            while opt[0] not in acceptable: # if the input is invalid
                opt = get_option()
        except: # if the inout is empty
            while opt == None:
                print('Invalid option.')
                display( stock, tableau, foundation)
                opt = get_option()
        # Your code goes here
        
        
        if opt[0] == 'D' and stock: # this deals to the tableau
            for i in range(4):
                tableau[i].append(stock.deal())
        elif opt[0] == 'F': # move to foundation
            move_to_foundation( tableau, foundation, int(opt[1])) # calls move function

            #print(foundation, '\n', tableau)
        elif opt[0] == 'T': # move within tableau
            move_within_tableau( tableau, int(opt[1]), int(opt[2]) ) # calls move function

                
        elif opt[0] == 'R': # resets the tableau and foundation
            for item in tableau: # delets everything in tableau
                item.pop()
            for item in foundation: # deletes everything in foundation
                item.pop()
            
            print("=========== Restarting: new game ============") 
            print( RULES ) 
            print( MENU )
            
            stock = cards.Deck()
            stock.shuffle()
            stock, tableau, foundation = init_game() # restarts the whole deck, tableau, and foundation

        elif opt[0] == 'H': # prints the menu
            print(MENU)
        
        elif opt[0] == 'Q': # quits and breaks
            print("You have chosen to quit.")
            break
        
        w = check_for_win( stock, tableau ) # checks for win after every move
        
        if not w: # displays only if theres not a W
            display( stock, tableau, foundation)
                
        
        if w: # if the user wins
            print("You won!")
            break

if __name__ == "__main__":
    main()
