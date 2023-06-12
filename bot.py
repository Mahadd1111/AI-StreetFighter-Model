from command import Command
import numpy as np
from buttons import Buttons
import pickle

class Bot:

    def __init__(self):
        #< - v + < - v - v + > - > + Y
        self.fire_code=["<","!<","v+<","!v+!<","v","!v","v+>","!v+!>",">+Y","!>+!Y"]
        self.exe_code = 0
        self.start_fire=True
        self.remaining_code=[]
        self.my_command = Command()
        self.buttn= Buttons()
        with open('model2.pkl','rb') as f:
            self.model = pickle.load(f)

    def fight(self,current_game_state,player):
        #python Videos\gamebot-competition-master\PythonAPI\controller.py 1
        counter = 0
        if player=="1":

            # BOT == PLAYER 1, HUMAN == PLAYER 2
            print("EXECUTING MODEL 1")
            #v - < + v - < + B spinning

            # IN OUR MODEL P1 is the opponent and P2 is the current (bot) to perform move
            bot_player = current_game_state.player1
            opponent = current_game_state.player2

            p1_id,p1_hp,p1_xc,p1_yc,p1_ismove,p1_moveid,p1_isjump,p1_iscrouch = opponent.player_id,opponent.health,opponent.x_coord,opponent.y_coord,opponent.is_player_in_move,opponent.move_id,opponent.is_jumping,opponent.is_crouching
            p2_id, p2_hp, p2_xc, p2_yc, p2_ismove, p2_moveid, p2_isjump, p2_iscrouch = bot_player.player_id, bot_player.health, bot_player.x_coord, bot_player.y_coord, bot_player.is_player_in_move, bot_player.move_id, bot_player.is_jumping, bot_player.is_crouching

            new_data = np.array([p1_id,p1_hp,p1_xc,p1_yc,p1_ismove,p1_moveid,p1_isjump,p1_iscrouch,p2_id,p2_hp,p2_xc,p2_yc,p2_ismove,p2_moveid,p2_isjump,p2_iscrouch])
            new_data = new_data.reshape(1,-1)
            if counter%30==0:
                predicted_output = self.model.predict(new_data)
                print("Predicted Output: ",predicted_output)
            res = predicted_output[0]
            self.buttn.A,self.buttn.up,self.buttn.left,self.buttn.right,self.buttn.R,self.buttn.down,self.buttn.X,self.buttn.L,self.buttn.B,self.buttn.Y = False,False,False,False,False,False,False,False,False,False
            if res[0]==1:
                self.buttn.A = True
            if res[1]==1:
                self.buttn.B=True
            if res[2]==1:
                self.buttn.R=True
            if res[3]==1:
                self.buttn.L=True
            if res[4]==1:
                self.buttn.Y=True
            if res[5]==1:
                self.buttn.X=True
            if res[6]==1:
                self.buttn.left=True
            if res[7]==1:
                self.buttn.right=True
            if res[8]==1:
                self.buttn.up=True
            if res[9]==1:
                self.buttn.down=True

            counter = counter+1

            self.my_command.player_buttons=self.buttn

        elif player=="2":

            # BOT == PLAYER 2, HUMAN == PLAYER 1
            print("EXECUTING MODEL 2")
            # v - < + v - < + B spinning

            # IN OUR MODEL P1 is the opponent and P2 is the current (bot) to perform move
            bot_player = current_game_state.player2
            opponent = current_game_state.player1

            p1_id, p1_hp, p1_xc, p1_yc, p1_ismove, p1_moveid, p1_isjump, p1_iscrouch = opponent.player_id, opponent.health, opponent.x_coord, opponent.y_coord, opponent.is_player_in_move, opponent.move_id, opponent.is_jumping, opponent.is_crouching
            p2_id, p2_hp, p2_xc, p2_yc, p2_ismove, p2_moveid, p2_isjump, p2_iscrouch = bot_player.player_id, bot_player.health, bot_player.x_coord, bot_player.y_coord, bot_player.is_player_in_move, bot_player.move_id, bot_player.is_jumping, bot_player.is_crouching

            new_data = np.array([p1_id, p1_hp, p1_xc, p1_yc, p1_ismove, p1_moveid, p1_isjump, p1_iscrouch, p2_id, p2_hp, p2_xc, p2_yc, p2_ismove, p2_moveid, p2_isjump, p2_iscrouch])
            new_data = new_data.reshape(1, -1)
            if counter%30==0:
                predicted_output = self.model.predict(new_data)
                print("Prediction : ",predicted_output)
            res = predicted_output[0]
            self.buttn.A, self.buttn.up, self.buttn.left, self.buttn.right, self.buttn.R, self.buttn.down, self.buttn.X, self.buttn.L, self.buttn.B, self.buttn.Y = False, False, False, False, False, False, False, False, False, False
            if res[0] == 1:
                self.buttn.A = True
            if res[1] == 1:
                self.buttn.B = True
            if res[2] == 1:
                self.buttn.R = True
            if res[3] == 1:
                self.buttn.L = True
            if res[4] == 1:
                self.buttn.Y = True
            if res[5] == 1:
                self.buttn.X = True
            if res[6] == 1:
                self.buttn.left = True
            if res[7] == 1:
                self.buttn.right = True
            if res[8] == 1:
                self.buttn.up = True
            if res[9] == 1:
                self.buttn.down = True

            counter = counter + 1
        return self.my_command



    def run_command( self , com , player   ):

        if self.exe_code-1==len(self.fire_code):
            self.exe_code=0
            self.start_fire=False
            print ("compelete")
            #exit()
            # print ( "left:",player.player_buttons.left )
            # print ( "right:",player.player_buttons.right )
            # print ( "up:",player.player_buttons.up )
            # print ( "down:",player.player_buttons.down )
            # print ( "Y:",player.player_buttons.Y )

        elif len(self.remaining_code)==0 :

            self.fire_code=com
            #self.my_command=Command()
            self.exe_code+=1

            self.remaining_code=self.fire_code[0:]

        else:
            self.exe_code+=1
            if self.remaining_code[0]=="v+<":
                self.buttn.down=True
                self.buttn.left=True
                print("v+<")
            elif self.remaining_code[0]=="!v+!<":
                self.buttn.down=False
                self.buttn.left=False
                print("!v+!<")
            elif self.remaining_code[0]=="v+>":
                self.buttn.down=True
                self.buttn.right=True
                print("v+>")
            elif self.remaining_code[0]=="!v+!>":
                self.buttn.down=False
                self.buttn.right=False
                print("!v+!>")

            elif self.remaining_code[0]==">+Y":
                self.buttn.Y= True #not (player.player_buttons.Y)
                self.buttn.right=True
                print(">+Y")
            elif self.remaining_code[0]=="!>+!Y":
                self.buttn.Y= False #not (player.player_buttons.Y)
                self.buttn.right=False
                print("!>+!Y")

            elif self.remaining_code[0]=="<+Y":
                self.buttn.Y= True #not (player.player_buttons.Y)
                self.buttn.left=True
                print("<+Y")
            elif self.remaining_code[0]=="!<+!Y":
                self.buttn.Y= False #not (player.player_buttons.Y)
                self.buttn.left=False
                print("!<+!Y")

            elif self.remaining_code[0]== ">+^+L" :
                self.buttn.right=True
                self.buttn.up=True
                self.buttn.L= not (player.player_buttons.L)
                print(">+^+L")
            elif self.remaining_code[0]== "!>+!^+!L" :
                self.buttn.right=False
                self.buttn.up=False
                self.buttn.L= False #not (player.player_buttons.L)
                print("!>+!^+!L")

            elif self.remaining_code[0]== ">+^+Y" :
                self.buttn.right=True
                self.buttn.up=True
                self.buttn.Y= not (player.player_buttons.Y)
                print(">+^+Y")
            elif self.remaining_code[0]== "!>+!^+!Y" :
                self.buttn.right=False
                self.buttn.up=False
                self.buttn.Y= False #not (player.player_buttons.L)
                print("!>+!^+!Y")


            elif self.remaining_code[0]== ">+^+R" :
                self.buttn.right=True
                self.buttn.up=True
                self.buttn.R= not (player.player_buttons.R)
                print(">+^+R")
            elif self.remaining_code[0]== "!>+!^+!R" :
                self.buttn.right=False
                self.buttn.up=False
                self.buttn.R= False #ot (player.player_buttons.R)
                print("!>+!^+!R")

            elif self.remaining_code[0]== ">+^+A" :
                self.buttn.right=True
                self.buttn.up=True
                self.buttn.A= not (player.player_buttons.A)
                print(">+^+A")
            elif self.remaining_code[0]== "!>+!^+!A" :
                self.buttn.right=False
                self.buttn.up=False
                self.buttn.A= False #not (player.player_buttons.A)
                print("!>+!^+!A")

            elif self.remaining_code[0]== ">+^+B" :
                self.buttn.right=True
                self.buttn.up=True
                self.buttn.B= not (player.player_buttons.B)
                print(">+^+B")
            elif self.remaining_code[0]== "!>+!^+!B" :
                self.buttn.right=False
                self.buttn.up=False
                self.buttn.B= False #not (player.player_buttons.A)
                print("!>+!^+!B")

            elif self.remaining_code[0]== "<+^+L" :
                self.buttn.left=True
                self.buttn.up=True
                self.buttn.L= not (player.player_buttons.L)
                print("<+^+L")
            elif self.remaining_code[0]== "!<+!^+!L" :
                self.buttn.left=False
                self.buttn.up=False
                self.buttn.L= False  #not (player.player_buttons.Y)
                print("!<+!^+!L")

            elif self.remaining_code[0]== "<+^+Y" :
                self.buttn.left=True
                self.buttn.up=True
                self.buttn.Y= not (player.player_buttons.Y)
                print("<+^+Y")
            elif self.remaining_code[0]== "!<+!^+!Y" :
                self.buttn.left=False
                self.buttn.up=False
                self.buttn.Y= False  #not (player.player_buttons.Y)
                print("!<+!^+!Y")

            elif self.remaining_code[0]== "<+^+R" :
                self.buttn.left=True
                self.buttn.up=True
                self.buttn.R= not (player.player_buttons.R)
                print("<+^+R")
            elif self.remaining_code[0]== "!<+!^+!R" :
                self.buttn.left=False
                self.buttn.up=False
                self.buttn.R= False  #not (player.player_buttons.Y)
                print("!<+!^+!R")

            elif self.remaining_code[0]== "<+^+A" :
                self.buttn.left=True
                self.buttn.up=True
                self.buttn.A= not (player.player_buttons.A)
                print("<+^+A")
            elif self.remaining_code[0]== "!<+!^+!A" :
                self.buttn.left=False
                self.buttn.up=False
                self.buttn.A= False  #not (player.player_buttons.Y)
                print("!<+!^+!A")

            elif self.remaining_code[0]== "<+^+B" :
                self.buttn.left=True
                self.buttn.up=True
                self.buttn.B= not (player.player_buttons.B)
                print("<+^+B")
            elif self.remaining_code[0]== "!<+!^+!B" :
                self.buttn.left=False
                self.buttn.up=False
                self.buttn.B= False  #not (player.player_buttons.Y)
                print("!<+!^+!B")

            elif self.remaining_code[0]== "v+R" :
                self.buttn.down=True
                self.buttn.R= not (player.player_buttons.R)
                print("v+R")
            elif self.remaining_code[0]== "!v+!R" :
                self.buttn.down=False
                self.buttn.R= False  #not (player.player_buttons.Y)
                print("!v+!R")

            else:
                if self.remaining_code[0] =="v" :
                    self.buttn.down=True
                    print ( "down" )
                elif self.remaining_code[0] =="!v":
                    self.buttn.down=False
                    print ( "Not down" )
                elif self.remaining_code[0] =="<" :
                    print ( "left" )
                    self.buttn.left=True
                elif self.remaining_code[0] =="!<" :
                    print ( "Not left" )
                    self.buttn.left=False
                elif self.remaining_code[0] ==">" :
                    print ( "right" )
                    self.buttn.right=True
                elif self.remaining_code[0] =="!>" :
                    print ( "Not right" )
                    self.buttn.right=False

                elif self.remaining_code[0] =="^" :
                    print ( "up" )
                    self.buttn.up=True
                elif self.remaining_code[0] =="!^" :
                    print ( "Not up" )
                    self.buttn.up=False
            self.remaining_code=self.remaining_code[1:]
        return
