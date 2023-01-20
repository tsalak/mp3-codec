import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
from mp3 import make_mp3_analysisfb, make_mp3_synthesisfb
from nothing import donothing,idonothing
from frame import frame_sub_analysis,frame_sub_synthesis


def plot_frequency(H,fs):

    vals = np.zeros(H.shape)

    for i in np.arange(H.shape[1]):
        freq, Hf = signal.freqz(H[:,i],fs=fs)
        Hfabs = np.absolute(Hf)
        vals[:,i] = 10 *  np.log10(Hfabs*Hfabs)

    plt.figure()
    plt.plot(freq,vals)
    plt.xlabel("Hz")
    plt.ylabel("dB")
    plt.title("Μέτρο των συναρτήσεων μεταφοράς των φίλτρων στη συχνοτητα f")

    z = 13*np.arctan(0.00076*freq) + 3.5*np.arctan((freq/7500)**2)
    
    plt.figure()
    plt.plot(z,vals)
    plt.xlabel("Barks")
    plt.ylabel("dB")
    plt.title("Μέτρο των συναρτήσεων μεταφοράς των φίλτρων στη συχνοτητα z")
    plt.show()


def codec0(wavin, h, M, N):

    Ytot = coder0(wavin,h,M,N)
    xhat = decoder0(Ytot, h, M, N)

    return xhat,Ytot




def coder0(wavin, h, M, N):

    H = make_mp3_analysisfb(h, M)

    L,_ = H.shape
    xbuffsize, ybuffsize = M*N, N
    i = 0
    Ytot = np.empty((0,M))

    while (i+1)*xbuffsize <= wavin.shape[0]:
        if (i+1)*xbuffsize + L - M <= wavin.shape[0]:
            xbuff = wavin[i*xbuffsize:(i+1)*xbuffsize + L - M]
        else:
            xbuff = np.r_[wavin[i*xbuffsize:(i+1)*xbuffsize],np.zeros(L-M)]
        Y = frame_sub_analysis(xbuff,H,N)        
        Yc = donothing(Y)
        Ytot = np.r_[Ytot,Yc]
        i = i + 1

    return Ytot


def decoder0(Ytot, h, M, N):
    
    G = make_mp3_synthesisfb(h,M)

    L,_ = G.shape
    ybuffsize = N


    i = 0
    Yhtot = np.empty((0,M))
    while (i+1)*ybuffsize <= Ytot.shape[0]:
        Yc = Ytot[i*ybuffsize:(i+1)*ybuffsize, :]
        Yh = idonothing(Yc)
        Yhtot = np.r_[Yhtot,Yh]
        i = i + 1

    i = 0
    xhat = np.empty(0)
    while (i+1)*ybuffsize <= Ytot.shape[0]:
        if (i+1)*ybuffsize + L//M - 1 <= Ytot.shape[0]:
            ybuff = Yhtot[i*ybuffsize:(i+1)*ybuffsize + L//M - 1, :]
        else:
            ybuff = np.r_[Yhtot[i*ybuffsize:(i+1)*ybuffsize, :],np.zeros((L//M - 1,M))]
        xsynth = frame_sub_synthesis(ybuff,G)
        xhat = np.r_[xhat,xsynth]
        i = i + 1

    return xhat

