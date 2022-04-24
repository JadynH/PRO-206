import socket
from tkinter import *
from threading import Thread
import random

from sklearn.compose import ColumnTransformer


def setup():
    global SERVER
    global PORT 
    global IP_ADDRESS

    PORT = 6000
    IP_ADDRESS = '192.168.1.26'

    SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SERVER.connect((IP_ADDRESS, PORT))

    thread = Thread(target=recivedMsg)
    thread.start()


def askPlayerName():
    global playerName 
    global nameEntry 
    global nameWindow 
    global canvas1

    nameWindow = Tk()
    nameWindow.title("TAMBOLA FAMILY FUN")
    nameWindow.geometry('800x600')
    

    screen_width = nameWindow.winfo_screenwidth()
    screen_height = nameWindow.winfo_screenheight()

    bg = ImageTK.PhotoImage(file = "./assets/background.png")
    
    canvas1 = Canvas(nameWindow, width = 500, height=500)
    canvas1.pack(fill="both", expand=True)
    canvas1.create_image(0,0, image=bg, anchor="nw")
    canvas1.create_text(screen_width/74.5, y=screen_height/8, text="Enter Name", font=("Chalkboard SE",60), fill="black")

    nameEntry = Entry(nameWindow, width=15, justify='center', font=("Chalkboard SE", 30), bd=5, bg="white")
    nameEntry.place(x=screen_width/7, y=screen_height/5.5)

    button = Button(nameWindow, text="Save", font=("Chalkboard SE",30),width=11, command=saveName, height=2, bg="#80deea", bd=3)
    button.place(x=screen_width/6, y=screen_height/4)

    nameWindow.resizable(True, True)
    nameWindow.mainloop()


def gameWindow():
    global gameWindow
    global canvas2
    global screen_width
    global screen_height
    global dice
    global winingMessage
    global resetButton


    gameWindow = Tk()
    gameWindow.title("Ludo Ladder")
    gameWindow.attributes('-fullscreen',True)

    screen_width = gameWindow.winfo_screenwidth()
    screen_height = gameWindow.winfo_screenheight()

    bg = ImageTk.PhotoImage(file = "./assets/background.png")

    canvas2 = Canvas( gameWindow, width = 500,height = 500)
    canvas2.pack(fill = "both", expand = True)

    # Display image
    canvas2.create_image( 0, 0, image = bg, anchor = "nw")

    # Add Text
    canvas2.create_text( screen_width/2, screen_height/5, text = "Ludo Ladder", font=("Chalkboard SE",100), fill="white")

    flashNumberLabel = canvas2.create_text(400,screen_height/2.3,text=
    "Waiting for others to join...", font=("Chalkboard SE",30), fill="#3e2723")


def createTicket():
    global gameWindow
    global ticketGrid

    mainLable = Label(gameWindow, width=65, height=16, relief='ridge', borderwidth=5, bg='white')
    mainLable.place(x=95, y=119)

    xPos = 105
    yPos = 130
    for row in range(0, 3):
        rowlist = []
        for col in range(0, 9):
            if(platform.system() == 'Darwin'):
                boxButton = tk.Button(gameWindow, font=("Chalkboard SE", 30), width=3, height=2, borderwidth=5, bg="#fff176")
                boxButton.place(x=xPos, y=yPos)

            rowlist.append(boxButton)
            xPos += 64

        ticketGrid.append(rowlist)
        xPos = 105
        yPos += 82



def placeNumbers():
    global ticketGrid
    global currentNumberList

    for row in range(0,3):
        randomColList = []
        counter = 0
        while counter<=4:
            randomCol = random.randint(0,8)
            if(randomCol not in randomColList):
                randomColList.append(randomCol)
                counter+=1
numberContainer = {
     "0": [1, 2, 3, 4, 5, 6, 7, 8, 9],
     "1": [10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
     "2": [20, 21, 22, 23, 24, 25, 26, 27, 28, 29],
     "3": [30, 31, 32, 33, 34, 35, 36, 37, 38, 39],
     "4": [40, 41, 42, 43, 44, 45, 46, 47, 48, 49],
     "5": [50, 51, 52, 53, 54, 55, 56, 57, 58, 59],
     "6": [60, 61, 62, 63, 64, 65, 66, 67, 68, 69],
     "7": [70, 71, 72, 73, 74, 74, 76, 77, 78, 79],
     "8": [80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90],
    }

counter = 0
while (counter < len(randomColList)):
    colNum = randomColList[counter]
    numbersListByIndex = numberContainer[str(colNum)]
    randomNumber = random.choice(numbersListByIndex)

    if(randomNumber not in currentNumberList):
        numberBox = ticketGrid[row][colNum]
        numberBox.configure(text=randomNumber, fg="black")
        currentNumberList.append(randomNumber)

        counter+=1


def recivedMsg():
    global SERVER
    global displayedNumberList
    global flashNumberLabel
    global canvas2
    global gameOver

    numbers = [str(i) for i in range(1, 91)]

    while True:
        chunk = SERVER.recv(2048).decode()
        if(chunk in numbers and flashNumberLabel and not gameOver):
            flashNumberList.append(int(chunk))
            canvas2.itemconfigure(flashNumberLabel, text = chunk, font=('Chalkboard SE', 60))
        elif('wins the game.' in chunk):
            gameOver = True
            canvas2.itemconfigure(flashNumberLabel, text=chunk, font=('Chalkboard SE', 40))

        








def saveName():
    global SERVER
    global playerName 
    global nameWindow
    global nameEntry

    playerName = nameEntry.get()
    nameEntry.delete(0, END)
    nameWindow.destroy()

    SERVER.send(playerName.encode())