import numpy as np
import math as ma
import random
import matplotlib.pyplot as plt


#Generate spectrum of FZP
def FZP_gen(H_DIM,lamda,psize,z):
    f=np.array(np.zeros((H_DIM,H_DIM)))
    fr=np.array(np.zeros((H_DIM,H_DIM)))
    fi=np.array(np.zeros((H_DIM,H_DIM)))
    wn=2*ma.pi/lamda
    hdim=int(H_DIM/2)
    for row in range(0,H_DIM):
        for col in range(0,H_DIM):
            x=(row-hdim)*psize
            y=(col-hdim)*psize
            r=wn*ma.sqrt(x**2+y**2+z**2)
            vr=ma.cos(r)
            vi=ma.sin(r)
            fr[row][col]=vr
            fi[row][col]=vi
    fzp=np.fft.fft2(fr+1j*fi)
    return fzp


def Holo_gen(fzp,img):
    A=np.fft.fft2(img)
    B=np.multiply(A,fzp)
    H=np.fft.ifft2(B)
    return np.fft.fftshift(H)

def Holo_recon(fzp,H):
    A=np.fft.fft2(H)
    B=np.multiply(A,np.conj(fzp))
    I=np.fft.ifft2(B)
    return np.fft.fftshift(I)

def Ger_Sax_algo(img, max_iter):
    h, w = img.shape
    pm_s = np.random.rand(h, w)
    pm_f = np.ones((h, w))
    am_s = np.sqrt(img)
    am_f = np.ones((h, w))

    signal_s = am_s*np.exp(pm_s * 1j)

    for iter in range(max_iter):
        signal_f = np.fft.fft2(signal_s)
        pm_f = np.angle(signal_f)
        signal_f = am_f*np.exp(pm_f * 1j)
        signal_s = np.fft.ifft2(signal_f)
        pm_s = np.angle(signal_s)
        signal_s = am_s*np.exp(pm_s * 1j)

    pm =pm_f
    return pm

def RNA(img):
    nrow = img.shape[0]
    ncol = img.shape[1]
    a = [[1j*random.uniform(0, 2 * ma.pi) for j in range(0, ncol)] for i in range(0, nrow)]
    img= img * np.exp(a)
    return img

def Down_samp(img):
    img_list = img.tolist()
    L= len(img_list[0])
    img_new = tm = [[0] * L for i in range(L)]
    M=8
    for i in range(L):
        for j in range(L):
            ym = i%M
            xm = j%M
            if ym == 0 or xm ==0 or xm==ym or xm==M-1-ym:
                img_new[i][j]=img_list[i][j]
            else:
                img_new[i][j]=0
                
    img = np.array(img_new)
    return img