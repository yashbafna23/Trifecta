import tkinter,chess,os
class GUI:
    def __init__(self,master):
        master.geometry('400x350+400+200')  # Set window geometry in tkinter
        master.resizable(0, 0)
        master.title('Choose Piece:')

        self.master = master
        self.piece =None
        self.paddingx = 110
        self.paddingy = 20

        self.game = None

        self.QueenButton = tkinter.Button(master,width=20,height=2,text = 'Queen',command = self.Queen)
        self.QueenButton.grid(padx=self.paddingx,pady=self.paddingy,row=0,column =10)

        self.RookButton = tkinter.Button(master,width=20,height=2,text = 'Rook',command = self.Rook)
        self.RookButton.grid(padx=self.paddingx,pady=self.paddingy,row=1,column =10)

        self.KnightButton = tkinter.Button(master,width=20,height=2,text = 'Knight',command = self.Knight)
        self.KnightButton.grid(padx=self.paddingx,pady=self.paddingy,row=2,column =10)


        self.KnightButton = tkinter.Button(master,width=20,height=2,text = 'Bishop',command = self.Bishop)
        self.KnightButton.grid(padx=self.paddingx,pady=self.paddingy,row=3,column =10)


    def Queen(self):
        self.piece = chess.QUEEN
        self.master.quit()

    def Rook(self):
        self.piece = chess.ROOK
        self.master.quit()

    def Knight(self):
        self.piece = chess.KNIGHT
        self.master.quit()

    def Bishop(self):
        self.piece = chess.BISHOP
        self.master.quit()

def choosepiece():
    root = tkinter.Tk()
    b = GUI(root)
    root.mainloop()
    print(b.piece)
    root.destroy()
    return b.piece
