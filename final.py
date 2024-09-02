#putting it all together: cleaner program doc without testing cells

import math
import time
from random import randrange
import logging
from inputimeout import inputimeout 

class player:
    def __init__(self, name_, pool_size, num, pieces=0, score=0) -> None:    
        self.name=name_

        # if num != -1:
        self.number=num #generated indep so multiple people can have the same number
        # else:
        #     self.number = randrange(1,100)
        
        self.cards = ["+","x","/", "z"]
        self.pieces =pieces
        self.score = score
        self.guesses = [0] * pool_size

def csvline2list(line): #input processing
    acc=""
    end_list = []
    for c in line:
        if (c==","):
            end_list+=[acc]
            acc=""
        elif(c==" "):
            pass
        else:
            acc = acc+c
    end_list+=[acc]
    return end_list

def handle_op(op, n1, n2): #BSN LOGIC
    if (op == "+"):
        result = n1 + n2 #both nums should already be ints
        if (result <20):
            return "between 3-20"
        elif (result>180):
            return "between 180-198"
        else:
            return str(result)
    elif (op=="x"):
        return str(n1*n2)[-1]
    elif(op=="/"):
        return str(math.floor(max(abs(n1/n2), abs(n2/n1))))
    elif(op=="z"):
        v1 = math.floor(n1/10)
        v2 = math.floor(n2/10)
        return str(max(v1-v2, v2-v1))
    else:
        print("Error, invalid operation")
        return "non-existent move"
    

def print_players(pp):#Utility
    for p in pp:
        attributes = vars(p)
        print(', '.join("%s: %s" % item for item in attributes.items()))

def print_ids(pp, show_pieces = False):
    n=0
    for p in pp:
        if show_pieces:
            print(n, p.name,p.pieces)
        else:
            print(n,p.name)    
        n=n+1

def init_players(players): #Business LOGIC
    #proc input
    p_input= input("Enter a comma separated list of all participants. The order will determine your player id (starting at 0). ") #does not check for duplicates
    p_names = csvline2list(p_input)

    #init players
    p_size = len(p_names)
    answers = []

    for p in p_names:
        p_num = randrange(1,100)
        players+= [player(p, p_size, p_num)]
        answers+=[p_num]

    #assign pieces
    for r in range(math.floor(p_size/2)): #a third of the players get pieces
        players[randrange(p_size)].pieces= players[randrange(p_size)].pieces+1 #done w replacement so worst case 1 person could get all

    print("==============PLAYER LIST==============")
    print("id name pieces")
    print_ids(players, show_pieces=True)

    return answers


def proc_play(id1, id2, op, players): #ids are int #BSN LOGIC

    try:
        p1 = players[id1]
        p2 = players[id2]

        if(p1 is p2): print("Error, cannot check operand card with yourself")
            
    except(IndexError):
        print("Error, Unknown player id. Please retry your request.")
        return

    if (op in p1.cards and op in p2.cards):
        print("The result of operation " +op+ "between players"+id1+id2+ "is"+ handle_op(op, p1.number, p2.number))
        p1.cards.remove(op)
        p2.cards.remove(op)
    else:
        print("Error, at least one card is missing.")
    
    return

def handle_stdin(players):
    print("Welcome to numguesser!")

    # answers = test_init_players(players)
    answers = init_players(players)

    #explain rules TODO


    #set up timing logistics
    limit = 10 #seconds
    start = time.time()

    #main loop
    # while(True):
    while (time.time()-start<=limit):
        curr = time.time()


        # instr = input( "Enter your request (play, buy, hand, check, roster or end)")

        try: 
        # Take timed input using inputimeout() function 
            instr = inputimeout(prompt='Enter your request (play, buy, hand, check, roster or end)', timeout=limit-(curr-start)) 
    
        # Catch the timeout error 
        except Exception: 
        
            # Declare the timeout statement 
            time_over = 'Your time is over!'
            print(time_over, time.time()-start) 
            return answers

        instr = instr.strip()

        if (instr =="play"):#play cards to get info
            op = input("Enter the operand card you would like to play:")
            p1 = input("Enter player 1 id:")
            p2 = input ("Enter player 2 id:")
            
            proc_play(int(p1.strip()), int(p2.strip()),op.strip(), players)
        
        elif (instr=="buy"): #buy extra set of cards
            p1 = input("Enter player id:")
        
            #start proc_buy

            try:
                p1 = players[int(p1.strip())]
            except(IndexError):
                print("Error, Unknown player id. Please retry your request.")
                continue
            
            if (p1.pieces>0): 
                p1.pieces = p1.pieces-1
                p1.cards += ["+","x","/","z"]
                print("you have successfully bought another set of 4 cards, new piece count is " + str(p1.pieces))
            else:
                print("Error, you do not have enough pieces.")
            #end proc_buy
        
        elif(instr =="hand"): #see player's cards
            p1 = input("Enter player id:")
            
            try:
                p1 = players[int(p1.strip())]
            except(IndexError):
                print("Error, Unknown player id. Please retry your request.")
                continue

            print("Your current hand is ", p1.cards)

        elif (instr=="check"): #view everyone, partly for debugging
            print_players(players)

        elif(instr=="roster"): #view all names and ids
            print_ids(players)

        elif(instr=="end"): #end game
            break

        else:
            print("Error, unknown command. Please try again.")
    return answers


def make_guesses(players):
    print("=============== Guessing phase ===================")
    print_ids(players)
    for p in players:
        guess = csvline2list(input("PLAYER "+p.name+"--- Enter a list of guesses for all players in the game."))
        p.guesses = [ (lambda a:0 if a=="" else int(a)) (g) for g in guess]

        # print(p.guesses)


def test_make_guesses(players):
    players[0].guesses=[93, 43, 90]
    players[1].guesses=[93, 43, 91]
    players[2].guesses=[92, 44, 91]

def score2piece(scores):
    tie = True
    pieces = [0]*len(scores)

    first = scores[0]

    for i in range(len(scores)):
        if (scores[i]!=first):tie = False #check tie

        if (scores[i]>= 16): pieces[i]=3 
        elif (scores[i]>= 11): pieces[i]=2
        elif (scores[i]>= 6): pieces[i]=1 
        elif (scores[i]>= 4): pieces[i]=-1
        elif (scores[i]>= -1): pieces[i]=-2 #assign pieces value
        else: pieces[i]=-3

    lowest= min(scores)
    for i in range(len(scores)):
        if scores[i]==lowest: pieces[i]=-3
        
    if tie: pieces = [-1]*len(scores)
    return pieces

def check_guesses(players, answers):
    n_players = len(players)
    tally = [0]*n_players
    scoreboard = [None]*n_players
    
    for j in range(n_players):
        p=players[j]
        grades = [0]*n_players
        
        #grade all
        for i in range(n_players):
            if p.guesses[i]==answers[i]: 
                grades[i]=1
                if (i!=j):#no penalty for guessing self correctly
                    tally[i]=tally[i]+1 #update tally
            else: grades[i]=-1

            if (i==j):
                grades[i]=grades[i]*5 #grade self
        
        scoreboard[j] = sum(grades)
        p.score=scoreboard[j]


    #add tally to scoreboard
    scoreboard = [scoreboard[i] - tally[i] for i in range(n_players) ]

    d_pieces = score2piece(scoreboard) #change in pieces

    for i in range(n_players):
        players[i].pieces = players[i].pieces + d_pieces[i]

    #should probably do some sort of final podium scores
    return scoreboard,d_pieces


def main():
    logger = logging.getLogger(__name__)
    logging.basicConfig(filename='numguesser.log', level=logging.INFO)
    logger.info("hello world")
    
    players = []
    answers = handle_stdin(players) #done
    make_guesses(players)
    check_guesses(players, answers) 
    print("**** The final results are: ******")
    print_players(players)
    print("exit program woo")


if __name__ == "__main__":
    main()