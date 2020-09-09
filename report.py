import wave
import math
from numpy import *
from pylab import *
from struct import *


def printWaveInfo(wf):
    """WAVEファイルの情報を取得"""
    print("チャンネル数:", wf.getnchannels())
    print ("サンプル幅:", wf.getsampwidth())
    print ("サンプリング周波数:", wf.getframerate())
    print ("フレーム数:", wf.getnframes())
    print ("パラメータ:", wf.getparams())
    print ("長さ（秒）:", float(wf.getnframes()) / wf.getframerate())


# 振幅スペクトルを考えるため絶対値をとる。最大振幅が１に正規化
def regularization(np_array):
    np_array = np.abs(np_array)
    max = np.max(np_array)
    # print(max,'max_value')
    np_array = np_array/np.max(np_array)
    return np_array

# Anを計算 
def rep_an_data(np_array, data, num):
    for n in range(num):
        area = 0
        for ft,t in enumerate(data):
            area += ft * math.cos(2*math.pi*n*t/T0)
        np_array = np.append(np_array, area*2/T0)
    return np_array

# Bnを計算
def rep_bn_data(np_array, data, num):
    for n in range(num):
        area = 0
        for ft,t in enumerate(data):
            area += ft * math.sin(2*math.pi*n*t/T0)
        np_array = np.append(np_array, area*2/T0)
    return np_array

# 時間遅延
def shift_n_time(f,n):
    new_f = f[n:]
    return new_f

# 時間遅延の信号の重ね合わせ
def low_pass_fillter(f,n):
    low_pass_list = np.zeros(len(f)-n)
    for i in range(n):
        shifted_n_data = shift_n_time(f,i)
        low_pass_list  += shifted_n_data[:-10+i]
    print(len(low_pass_list))
    return low_pass_list

def output_wav_file(name):
    pass


if __name__ == '__main__':
    wf = wave.open("r3.wav", "rb")
    buffer = wf.readframes(wf.getnframes())
    printWaveInfo(wf)

    N= 512
    fs = 44100
    T0 = N/fs
    freqList = [N/T0 for N in range(int(N/2))]
    han = np.hanning(N)    # ハニング窓e

    #  bufferはバイナリなので2バイトずつ整数（-32768から32767）にまとめる
    originaldata = frombuffer(buffer, dtype="int16")
    datafloat = originaldata[:N] * han

    dataint = np.array(datafloat, dtype=int)
    # print(dataint)
    plot(datafloat[:N])
    plot(originaldata[:N])
    show()

    an_array = np.array([])
    a0 = dataint.sum()/T0

    an_array = np.append(an_array,a0)
    an_array = rep_an_data(an_array,dataint, int(N/2))
    an_array = regularization(an_array)
    # plot([0]+freqList, an_array, marker='o', linestyle='-')
    # xlabel("frequency [Hz]")
    # ylabel("amplitude spectrum")

    # show()
    
    bn_array = np.array([])
    bn_array = rep_bn_data(bn_array,dataint, int(N/2))
    bn_array = regularization(bn_array)
    # plot(freqList, bn_array, marker='o', linestyle='-')
    # xlabel("frequency [Hz]")
    # ylabel("amplitude spectrum")

    # show()


    y = low_pass_fillter(dataint,10)

    an_array = np.array([])
    a0 = y.sum()/T0

    an_array = np.append(an_array,a0)
    an_array = rep_an_data(an_array,y, int(len(y)/2))
    an_array = regularization(an_array)
    # plot(freqList[:-4], an_array, marker='o', linestyle='-')
    # xlabel("frequency [Hz]")
    # ylabel("amplitude spectrum")

    # show()
    
    bn_array = np.array([])
    bn_array = rep_bn_data(bn_array, y, int(len(y)/2))
    bn_array = regularization(bn_array)
    
    # plot(freqList[:-5], bn_array, marker='o', linestyle='-')
    # xlabel("frequency [Hz]")
    # ylabel("amplitude spectrum")

    # show()
