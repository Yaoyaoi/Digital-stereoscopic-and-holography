from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
from PIL import ImageTk, Image
from pylab import *
import numpy as np
import os
import cmath


from FZP import FZP_gen, Holo_gen, Holo_recon,Ger_Sax_algo,RNA,Down_samp

class Window(Frame):

    # Define settings upon initialization. Here you can specify
    def __init__(self, master=None):
        Frame.__init__(self, master)   
        self.master = master
        self.pack(fill=BOTH, expand=1)
        self.index = 0
        self.init_window()
        self.hashologen = False
        self.hashologen_noise = False
        self.hashologen_downsample = False
        self.hasdouble_depth_image = False
        self.hasOSPR_method = False

    #Creation of init_window
    def init_window(self):

        # Project title      
        self.master.title("Miniproject 2 by Group 9")
        self.pack(fill=BOTH, expand=1)

        # Menu bar
        menu = Menu(self.master)
        self.master.config(menu=menu)

        # Create a 'File' menu item
        file = Menu(menu)
        file.add_command(label="Open", command=self.open)
        file.add_command(label="Save", command=self.save)
        file.add_command(label="Exit", command=self.exit)
        menu.add_cascade(label="File", menu=file)

        generate=Menu(menu)
        generate.add_command(label="Generate phase-only hologram", command=self.hologen)
        generate.add_command(label="Generate with the noise addition", command=self.hologen_noise)
        generate.add_command(label="Generate with the GCD", command=self.hologen_downsample)
        generate.add_command(label="Double depth image with the noise addition and GCD", command=self.double_depth_image)
        generate.add_command(label="Double depth image with OPSR method", command=self.OSPR_method)
        menu.add_cascade(label="Generate", menu=generate)


    #Callback function to open an image file                
    def open(self):
        global I,source,filename,img
        
        filepath = askopenfilename()
        filename=os.path.basename(filepath)
        source = Image.open(filepath)
        I=array(source)

        source = source.resize((128, 128), Image.ANTIALIAS)
        source = ImageTk.PhotoImage(source)
        panel = Label(image=source).place(x=10,y=10)

        file_label=Label(justify=CENTER,text=filename,width=18).place(x=10,y=142)
        
        #file_label.pack()
        
    #Callback function to save real/imaginery parts of hologram and its reconstructed images
    def save(self):
        global filename
        filename=os.path.splitext(filename)[0]
        
        if self.hashologen:
            plt.imsave(filename+"HP.jpg", HP_array, cmap='gray')
            plt.imsave(filename+"_recovery.jpg", recovery_array, cmap='gray')
            messagebox.showinfo(None, 'Hologen Images are saved')
        if self.hashologen_noise:
            plt.imsave(filename + "HP_noise.jpg", HP_noise_array, cmap='gray')
            plt.imsave(filename + "_recovery_noise.jpg", recovery_noise_array, cmap='gray')
            messagebox.showinfo(None, 'Hologen with noise Images are saved')
        if self.hashologen_downsample:
            plt.imsave(filename + "HP_ds.jpg", HP_ds_array, cmap='gray')
            plt.imsave(filename + "_recovery_gcd.jpg", recovery_gcd_array, cmap='gray')
            messagebox.showinfo(None, 'Hologen with downsample Images are saved')
        if self.hasdouble_depth_image:
            plt.imsave(filename+"HP_noise_double.jpg", HP_noise_double_array, cmap='gray')
            plt.imsave(filename+"_recovery_noise_up.jpg", recovery_noise_up_array, cmap='gray')
            plt.imsave(filename+"_recovery_noise_down.jpg", recovery_noise_down_array, cmap='gray')
            plt.imsave(filename+"HP_DS_double.jpg", HP_DS_double_array,cmap='gray')
            plt.imsave(filename+"_recovery_DS_up.jpg", recovery_DS_up_array, cmap='gray')
            plt.imsave(filename+"_recovery_DS_down.jpg", recovery_DS_down_array, cmap='gray')
            messagebox.showinfo(None, 'Double depth image Images are saved')
        '''if self.hasOSPR_method:
            self.saveWobbling()
            messagebox.showinfo(None, 'OSPR Images are saved')'''

    #Callback function to terminate program
    def exit(self):
        os._exit(0)


    #Hologram generation and reconstruction function
    def hologen(self):
        global I,source,img,HP,recovery,HP_array,recovery_array
        
        self.hashologen = True
        #Function to normalize input array to range [0,255]
        def normalize(H_image):
            range=np.amax(H_image)-np.amin(H_image)
            NH=255*(H_image-np.amin(H_image))/range
            NH=Image.fromarray(NH)
            NH=NH.resize((128, 128), Image.ANTIALIAS)
            NH=ImageTk.PhotoImage(NH)
            return NH

        #Optical settings 
        H_DIM=1024
        lamda=520e-9
        psize=6.4e-6
        z=0.16

        #Dimension of source image
        nrow=I.shape[0]
        ncol=I.shape[1]
        I=I.astype('float32')
        
        #Place input image to center of canvas within window bounded by (sx,sy,ex,ey)
        sx=round((H_DIM-ncol)/2)
        ex=round((H_DIM+ncol)/2)
        sy=round((H_DIM-nrow)/2)
        ey=round((H_DIM+nrow)/2)

        img=np.array(np.zeros((H_DIM,H_DIM)))
        img[sy:ey, sx:ex]=I
        
        #Display source image
        #panel = Label(image=source).place(x=10,y=10)

        # Generate Fresnel Zone Plate
        fzp = FZP_gen(H_DIM, lamda, psize, z)

        # Generate hologram
        H = Holo_gen(fzp, img)
        # Get phase parts of the complex-valued hologram
        HP_array= np.angle(H)
        HP_array1 = np.zeros((1024,1024),dtype = complex)
        for i in range(1024):
            for j in range(1024):
                HP_array1[i][j] = H[i][j]/abs(H[i][j])
        # Reconstruct image from hologram
        recovery_array = abs(Holo_recon(fzp, HP_array1))

        # Normalize images to range [0,255]
        HP = normalize(HP_array)
        recovery = normalize(recovery_array)

        phase_mask_panel = Label(image=HP).place(x=160,y=10)
        file_label=Label(justify=CENTER,text="Phase Only Hologram",width=30).place(x=120,y=142)

        # Phase only recovery image
        recovery_panel = Label(image=recovery).place(x=320,y=10)
        file_label=Label(justify=CENTER,text="Reconstruct",width=24).place(x=300,y=142)


        messagebox.showinfo(None, 'Hologram generated and reconstructed')

        #panel.pack

    def hologen_noise(self):
        global I, source, img, HP_noise, recovery_noise,HP_noise_array, recovery_noise_array
        self.hashologen_noise = True
        # Function to normalize input array to range [0,255]
        def normalize(H_image):
            range = np.amax(H_image) - np.amin(H_image)
            NH = 255 * (H_image - np.amin(H_image)) / range
            NH = Image.fromarray(NH)
            NH = NH.resize((128, 128), Image.ANTIALIAS)
            NH = ImageTk.PhotoImage(NH)
            return NH

        # Optical settings
        H_DIM = 1024
        lamda = 520e-9
        psize = 6.4e-6
        z = 0.16

        nrow = I.shape[0]
        ncol = I.shape[1]
        I = I.astype('float32')

        # Place input image to center of canvas within window bounded by (sx,sy,ex,ey)
        sx = round((H_DIM - ncol) / 2)
        ex = round((H_DIM + ncol) / 2)
        sy = round((H_DIM - nrow) / 2)
        ey = round((H_DIM + nrow) / 2)

        img = np.array(np.zeros((H_DIM, H_DIM)))
        img[sy:ey, sx:ex] = I

        # Generate Fresnel Zone Plate
        fzp = FZP_gen(H_DIM, lamda, psize, z)

        # RNA
        img = RNA(img)
        # Generate hologram
        H = Holo_gen(fzp, img)
        # Get phase parts of the complex-valued hologram
        HP_noise_array = np.angle(H)
        HP_noise_array1 = np.zeros((1024,1024),dtype = complex)
        for i in range(1024):
            for j in range(1024):
                HP_noise_array1[i][j] = H[i][j]/abs(H[i][j])

        # Reconstruct image from hologram
        recovery_noise_array = abs(Holo_recon(fzp, HP_noise_array1))

        # Normalize images to range [0,255]
        HP_noise = normalize(HP_noise_array)
        recovery_noise = normalize(recovery_noise_array)

        phase_mask_panel = Label(image=HP_noise).place(x=160, y=200)
        file_label = Label(justify=CENTER, text="Phase Only Hologarm\nwith the noise addition", width=30).place(x=120, y=332)

        # Phase only recovery image
        recovery_panel = Label(image=recovery_noise).place(x=320, y=200)
        file_label = Label(justify=CENTER, text="Reconstruct ", width=24).place(x=300, y=332)

        messagebox.showinfo(None, 'Hologram generated and reconstructed')

        #panel.pack

    def hologen_downsample(self):
        global I,HP_ds,recovery_gcd,source,HP_ds_array,recovery_gcd_array
        
        self.hashologen_downsample = True
        #Function to normalize input array to range [0,255]
        def normalize(H_image):
            range=np.amax(H_image)-np.amin(H_image)
            NH=255*(H_image-np.amin(H_image))/range
            NH=Image.fromarray(NH)
            NH=NH.resize((128, 128), Image.ANTIALIAS)
            NH=ImageTk.PhotoImage(NH)
            return NH
        #Optical settings 
        H_DIM=1024
        lamda=520e-9
        psize=6.4e-6
        z=0.16
         
        #Dimension of source image
        nrow=I.shape[0]
        ncol=I.shape[1]
        I=I.astype('float32')
        #Place input image to center of canvas within window bounded by (sx,sy,ex,ey)
        sx=round((H_DIM-ncol)/2)
        ex=round((H_DIM+ncol)/2)
        sy=round((H_DIM-nrow)/2)
        ey=round((H_DIM+nrow)/2)
         
        img=np.array(np.zeros((H_DIM,H_DIM)))
        img[sy:ey, sx:ex]=I

         
        #Generate Fresnel Zone Plate
        fzp=FZP_gen(H_DIM,lamda,psize,z)
        
        #down sample
        img=Down_samp(img)
        #Generate hologram
        H=Holo_gen(fzp,img)
        #print(H)
        HP_ds_array = np.angle(H)
        # Get phase parts of the complex-valued hologram
        HP_ds_array1 = np.zeros((1024,1024),dtype = complex)
        for i in range(1024):
            for j in range(1024):
                HP_ds_array1[i][j] = H[i][j]/abs(H[i][j])
        #Reconstruct image from hologram
        recovery_gcd_array=abs(Holo_recon(fzp,HP_ds_array1))

        #Normalize images to range [0,255]
        HP_ds=normalize(HP_ds_array)
        recovery_gcd=normalize(recovery_gcd_array)
         
        #Display phase of hologram and its reconstructed images
        HR_panel = Label(image=HP_ds).place(x=160,y=390)
        RES_panel = Label(image=recovery_gcd).place(x=320,y=390)
         
        file_label=Label(justify=CENTER,text="Phase Only Hologarm\nwith grid-cross downsample",width=30).place(x=120,y=522)
        file_label=Label(justify=CENTER,text="Reconstruct ",width=24).place(x=300,y=522)
        messagebox.showinfo(None, 'Hologram generated and reconstructed')

        
    def double_depth_image(self):
        # image to show
        global I,HP_noise_double,recovery_noise_up,recovery_noise_down,HP_DS_double,recovery_DS_up,recovery_DS_down
        # image to save
        global HP_noise_double_array,recovery_noise_up_array,recovery_noise_down_array,HP_DS_double_array,recovery_DS_up_array,recovery_DS_down_array
        self.hasdouble_depth_image = True
        zu = 0.16
        zd = 0.18
        H_DIM = 1024
        lamda = 520e-9
        psize = 6.4e-6
        # Function to normalize input array to range [0,255]
        def normalize(H_image):
            range = np.amax(H_image) - np.amin(H_image)
            NH = 255 * (H_image - np.amin(H_image)) / range
            NH = Image.fromarray(NH)
            NH = NH.resize((128, 128), Image.ANTIALIAS)
            NH = ImageTk.PhotoImage(NH)
            return NH

        high = len(I)
        Iup = I[:high//2]
        Idown = I[high//2:]
        HupR, HupDS= self.half_hologen_noise_downsample(Iup,zu,'u')
        HdownR, HdownDS = self.half_hologen_noise_downsample(Idown,zd,'d')
        HupR[H_DIM//2:] = HdownR[H_DIM//2:]
        HupDS[H_DIM//2:] = HdownDS[H_DIM//2:]

        # Get phase parts of the complex-valued hologram
        HP_noise_double_array = np.angle(HupR)
        HP_noise_double_array1 = np.zeros((1024,1024),dtype = complex)
        for i in range(1024):
            for j in range(1024):
                HP_noise_double_array1[i][j] = HupR[i][j]/abs(HupR[i][j])
        HP_DS_double_array = np.angle(HupDS)
        HP_DS_double_array1 = np.zeros((1024,1024),dtype = complex)
        for i in range(1024):
            for j in range(1024):
                HP_DS_double_array1[i][j] = HupDS[i][j]/abs(HupDS[i][j])

        fzpu = FZP_gen(H_DIM, lamda, psize, zu)
        fzpd = FZP_gen(H_DIM, lamda, psize, zd)

        # Reconstruct image from hologram
        recovery_noise_up_array = abs(Holo_recon(fzpu, HP_noise_double_array1))
        recovery_noise_down_array = abs(Holo_recon(fzpd, HP_noise_double_array1))
        recovery_DS_up_array = abs(Holo_recon(fzpu, HP_DS_double_array1))
        recovery_DS_down_array = abs(Holo_recon(fzpd, HP_DS_double_array1))
        
        # Normalize images to range [0,255]
        HP_noise_double = normalize(HP_noise_double_array)
        recovery_noise_up = normalize(recovery_noise_up_array)
        recovery_noise_down = normalize(recovery_noise_down_array) 
        HP_DS_double = normalize(HP_DS_double_array)
        recovery_DS_up = normalize(recovery_DS_up_array)
        recovery_DS_down = normalize(recovery_DS_down_array)

        # H image
        phase_mask_panel = Label(image=HP_noise_double).place(x=480, y=200)
        file_label = Label(justify=CENTER, text="Double depth image\nPhase Only Hologarm\nwith the noise addition", width=30).place(x=440, y=332)

        # Phase only recovery image
        recovery_panel_up = Label(image = recovery_noise_up).place(x=640, y=200)
        file_label_up = Label(justify=CENTER, text="Reconstructed\nfirst depth plane", width=24).place(x=600, y=332)
        recovery_panel_down = Label(image = recovery_noise_down).place(x=800, y=200)
        file_label_down = Label(justify=CENTER, text="Reconstructed\nsecond depth plane", width=24).place(x=760, y=332)

        # H image
        phase_mask_panel = Label(image=HP_DS_double).place(x=480, y=390)
        file_label = Label(justify=CENTER, text="Double depth image\nPhase Only Hologarm\nwith grid-cross downsample", width=30).place(x=440, y=522)

        # Phase only recovery image
        recovery_panel_up = Label(image = recovery_DS_up).place(x=640, y=390)
        file_label_up = Label(justify=CENTER, text="Reconstructed\nfirst depth plane", width=24).place(x=600, y=522)
        recovery_panel_down = Label(image = recovery_DS_down).place(x=800, y=390)
        file_label_down = Label(justify=CENTER, text="Reconstructed\nsecond depth plane", width=24).place(x=760, y=522)

        messagebox.showinfo(None, 'Hologram generated and reconstructed')
        

    def half_hologen_noise_downsample(self,I,z,side='u'):
        # Optical settings
        H_DIM = 1024
        lamda = 520e-9
        psize = 6.4e-6

        nrow = I.shape[0]
        ncol = I.shape[1]
        I = I.astype('float32')

        # Place input image to center of canvas within window bounded by (sx,sy,ex,ey)
        if side == 'u':
            sx = round((H_DIM - ncol) / 2)
            ex = round((H_DIM + ncol) / 2)
            sy = round((H_DIM / 2) - nrow)
            ey = round(H_DIM / 2)
        elif side == 'd':
            sx = round((H_DIM - ncol) / 2)
            ex = round((H_DIM + ncol) / 2)
            sy = round(H_DIM / 2) 
            ey = round((H_DIM / 2) + nrow)
        else:
            sx = round((H_DIM - ncol) / 2)
            ex = round((H_DIM + ncol) / 2)
            sy = round((H_DIM - nrow) / 2)
            ey = round((H_DIM + nrow) / 2)

        img = np.array(np.zeros((H_DIM, H_DIM)))
        img[sy:ey, sx:ex] = I

        # Generate Fresnel Zone Plate
        fzp = FZP_gen(H_DIM, lamda, psize, z)

        # RNA
        imgR = RNA(img)
        # Generate hologram
        Hr = Holo_gen(fzp, imgR)

        #downSample
        imgDS=Down_samp(img)
        # Generate hologram
        Hds = Holo_gen(fzp, imgDS)

        return Hr,Hds

    def half_hologen_random_noise(self,I,z,side='u'):
        # Optical settings
        H_DIM = 1024
        lamda = 520e-9
        psize = 6.4e-6

        nrow = I.shape[0]
        ncol = I.shape[1]
        I = I.astype('float32')

        # Place input image to center of canvas within window bounded by (sx,sy,ex,ey)
        if side == 'u':
            sx = round((H_DIM - ncol) / 2)
            ex = round((H_DIM + ncol) / 2)
            sy = round((H_DIM / 2) - nrow)
            ey = round(H_DIM / 2)
        elif side == 'd':
            sx = round((H_DIM - ncol) / 2)
            ex = round((H_DIM + ncol) / 2)
            sy = round(H_DIM / 2)
            ey = round((H_DIM / 2) + nrow)
        else:
            sx = round((H_DIM - ncol) / 2)
            ex = round((H_DIM + ncol) / 2)
            sy = round((H_DIM - nrow) / 2)
            ey = round((H_DIM + nrow) / 2)

        img = np.array(np.zeros((H_DIM, H_DIM)))
        img[sy:ey, sx:ex] = I

        # dumplicate 5 imgs
        ''' Hr = []
        for i in range(5):'''
            # Generate Fresnel Zone Plate
        fzp = FZP_gen(H_DIM, lamda, psize, z)

        # RNA
        imgR = RNA(img)
        # Generate hologram
        Hr1 = Holo_gen(fzp, imgR)
            #Hr.append(Hr1)

        return Hr1


    def OSPR_method(self):
        # image to show
        global I, HP_noise_double, recovery_noise_up, recovery_noise_down, complete_image,complete_nor
        # image to save
        global HP_noise_double_array, recovery_noise_up_array, recovery_noise_down_array,complete_image_array,recovery_noise_complete_array
        self.hasOSPR_method = True
        zu = 0.16
        zd = 0.18
        H_DIM = 1024
        lamda = 520e-9
        psize = 6.4e-6

        # Function to normalize input array to range [0,255]
        def normalize(H_image):
            range = np.amax(H_image) - np.amin(H_image)
            NH = 255 * (H_image - np.amin(H_image)) / range
            NH = Image.fromarray(NH)
            NH = NH.resize((128, 128), Image.ANTIALIAS)
            NH = ImageTk.PhotoImage(NH)
            return NH

        fzpu = FZP_gen(H_DIM, lamda, psize, zu)
        fzpd = FZP_gen(H_DIM, lamda, psize, zd)

        high = len(I)
        Iup = I[:high // 2]
        Idown = I[high // 2:]
        complete_image_array=[]#array全息保存
        complete_image_array1=[]
        for i in range(5):
            HupR = self.half_hologen_random_noise(Iup, zu, 'u')
            HdownR = self.half_hologen_random_noise(Idown, zd, 'd')
            HupR[H_DIM // 2:] = HdownR[H_DIM // 2:]
            HP_noise_double_array = np.angle(HupR)  # 取图片的相位 整张图片 array用于save
            HP_noise_double_array1 = np.zeros((1024,1024),dtype = complex)
            for i in range(1024):
                for j in range(1024):
                    HP_noise_double_array1[i][j] = HupR[i][j]/abs(HupR[i][j])
            complete_image_array.append(HP_noise_double_array)
            complete_image_array1.append(HP_noise_double_array1)

        recovery_noise_complete_array=[]
        for item in complete_image_array1:#整张图片重构
            # Get phase parts of the complex-valued hologram

            # Reconstruct image from hologram
            recovery_noise_up_array1 = abs(Holo_recon(fzpu, item))
            recovery_noise_down_array1 = abs(Holo_recon(fzpd, item))

            recovery_noise_up_array1[H_DIM // 2:] = recovery_noise_down_array1[H_DIM // 2:]
            recovery_noise_complete_array.append(recovery_noise_up_array1)
        #需要保存的array，直接展示的是图像
        # Normalize images to range [0,255]
        complete_nor=[]
        complete_image=[]
        for item in complete_image_array:
            complete_image1 = normalize(item)
            complete_image.append(complete_image1)

        for item in recovery_noise_complete_array:
            recovery_noise_complete = normalize(item)
            complete_nor.append(recovery_noise_complete)

        self.wobbling()
        # H image
        file_label = Label(justify=CENTER, text="Double depth image\nPhase Only Hologarm\nwith the noise addition",
                           width=30).place(x=120, y=712)
        file_label_up = Label(justify=CENTER, text="Reconstructed\ndouble depth image", width=24).place(x=280, y=712)


        messagebox.showinfo(None, 'Hologram generated and reconstructed')

    def wobbling(self):
        global index
        Label(image = complete_image[self.index]).place(x=160, y=580)
        Label(image = complete_nor[self.index]).place(x=320,y=580)
        self.index += 1
        if self.index > 4:
            self.index = 0
        self.after(10, self.wobbling)  # 在5ms重复他自己

    def saveWobbling(self):
        imgsWobbling = complete_image_array[0]  # 等于第一个图片
        imgsWobbling1 = recovery_noise_complete_array[0]
        imgsWobbling.save('Double depth image_OSPR.gif', save_all=True, append_images=complete_image_array, duration=0.01)
        imgsWobbling1.save('Reconstructed double depth.gif', save_all=True, append_images=recovery_noise_complete_array, duration=0.01)


# Root window created
root = Tk()
root.geometry("640x240")
app = Window(root)
root.mainloop()
