import tkinter as tk
import tkinter.messagebox as mb
from tkinter.filedialog import askopenfilename
from PIL import ImageTk, Image
from pylab import *
import numpy as np
import os
import time

imgNList = []
imgsFromReconstruction = []
for i in range(9):
    imgNList.append('imgs/Image {}.jpg'.format(i+1))

class Window(tk.Frame):

    # Define settings upon initialization. Here you can specify
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)   
        self.master = master
        self.isWobbling = False
        self.index = 0
        self.init_window()

    #Creation of init_window
    def init_window(self):

        # Project title      
        self.master.title("Miniproject 1 by Group 9")
        self.pack(fill=tk.BOTH, expand=1)
        self.canvas1 = tk.Canvas(self, height = '225', width = '1280', bg= '#E0FFFF')
        self.canvas1.place(x=0,y=0)
        self.canvas2 = tk.Canvas(self, height = '225', width = '640', bg= '#FFF0F5')
        self.canvas2.place(x=0,y=225)
        self.canvas4 = tk.Canvas(self, height = '225', width ='640',bg='#98FB98')
        self.canvas4.place(x=640,y=225)
        self.canvas3 = tk.Canvas(self, height = '225', width = '1280', bg= '#FFFFF0')
        self.canvas3.place(x=0,y=450)
        tk.Label(self.canvas1,text='origin images',width='10').place(x=10,y=100)
        self.impo()
        #btnImport = tk.Button(self, text='Import images',width='10',command=self.impo)
        #btnImport.place(x=10, y=100)
        btnIntegrate = tk.Button(self, text = 'Integrate',width='10',command=self.N2One)
        btnIntegrate.place(x=10,y=330)
        btnReconstruct = tk.Button(self, text = 'Reconstruct',width='10',command=self.One2N)
        btnReconstruct.place(x=10,y=550)
        btnStartWobble = tk.Button(self, text = 'Start Wobble 3D',width='15',command=self.startWobbling)
        btnStartWobble.place(x=650,y=300)
        btnStopWobble = tk.Button(self, text = 'Stop Wobble 3D',width='15',command=self.stopWobbling)
        btnStopWobble.place(x=650,y=330)
        btnSaveWobble = tk.Button(self, text = 'Save Wobble 3D gif',width='15',command=self.saveWobbling)
        btnSaveWobble.place(x=650,y=360)
        # Menu bar
        menu = tk.Menu(self.master)
        self.master.config(menu=menu)

        # Create a 'File' menu item
        file = tk.Menu(menu)
        file.add_command(label="Exit", command=self.exit)
        menu.add_cascade(label="File", menu=file)

    def impo(self):
        global imgNList

        for i in range(len(imgNList)):
            img = Image.open(imgNList[i])
            img = img.resize((128, 128), Image.ANTIALIAS)
            img=ImageTk.PhotoImage(img)
            label = tk.Label(self.canvas1)
            label.place(x=130*i+100,y=40)
            label.config(image=img)
            label.image=img


    def exit(self):
        os._exit(0)
    
    def N2One(self):
        panList = []
        imgList = []

        for imgFile in imgNList:
            img = Image.open(imgFile)
            img = img.resize((320, 320), Image.ANTIALIAS)
            pan = ImageTk.PhotoImage(img)
            panList.append(pan)
            imgList.append(array(img))
        
        I=array(img)

        #print(I[0])

        k = 0
        # mask
        mask=[
            [0,1,2,6,7,8,3,4,5],
            [8,0,1,5,6,7,2,3,4],
            [7,8,0,4,5,6,1,2,2],
            [6,7,8,3,4,5,0,1,2],
            [5,6,7,2,3,4,8,0,1],
            [4,5,6,1,2,3,7,8,0],
            [3,4,5,0,1,2,6,7,8],
            [2,3,4,8,0,1,5,6,7],
            [1,2,3,7,8,0,4,5,6],
            ]
        

        color=0
        for i in range(0,len(I)):
            for j in range(0,len(I[i])):
                index = mask[i%len(mask)][j%len(mask[0])]
                col=j%3
                index_r = mask[i%len(mask)][col*3]
                index_g = mask[i%len(mask)][col*3+1]
                index_b = mask[i%len(mask)][col*3+2]
                I[i][j][0]=imgList[index_r][i][j][0]
                I[i][j][1]=imgList[index_g][i][j][1]
                I[i][j][2]=imgList[index_b][i][j][2]
                color+=1
                if color>=2:
                    color=0
                
        img_IS = Image.fromarray(I)
        img_I = img_IS.resize((200, 200), Image.ANTIALIAS)
        img_I = ImageTk.PhotoImage(img_I)
        label = tk.Label(self.canvas2)
        label.config(image = img_I)
        label.image = img_I
        label.place(x=200,y=10)
        
        img_IS.save("integrate.jpg")
        mb.showinfo('saved','a integrate picture named \'integrate.jpg\' saved')
        

    def wobbling(self):
        if self.isWobbling:
            if imgsFromReconstruction:
                imgWList = imgsFromReconstruction[:]
            else:
                imgWList = imgNList[:]
            
            imgWList.extend(imgWList[-2::-1])
            img = Image.open(imgWList[self.index])
            img = img.resize((200, 200), Image.ANTIALIAS)
            img=ImageTk.PhotoImage(img)
            label = tk.Label(self.canvas4)
            label.place(x=200,y=10)
            label.config(image=img)
            label.image=img
            self.index += 1
            if self.index > 16:
                self.index = 0
        self.after(10, self.wobbling)

    def saveWobbling(self):
        imgs = []
        imgWList = imgNList[:]
        imgWList.extend(imgWList[-2::-1])
        for imageName in imgWList:
            imgs.append(Image.open(imageName))
        imgsWobbling = imgs[0]
        imgsWobbling.save('Wobbling3D.gif', save_all=True, append_images=imgs, duration=0.01)
        mb.showinfo('file saved', 'A gif file named \"Wobbling3D.gif\" has been saved')

    def startWobbling(self):
        if not imgsFromReconstruction:
            mb.showwarning('step error','You haven\'t reconstruct, the origin images are used to create the wobbling 3D')
        self.isWobbling = True

    def stopWobbling(self):
        self.isWobbling = False

    def One2N(self):
        mb.showwarning('Sorry','we haven\'t finished that function.')





        
# Root window created

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1280x900")
    app = Window(root)
    app.wobbling()
    root.mainloop()  