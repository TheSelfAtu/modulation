#coding: utf-8
import wave
import struct
import numpy as np
from pylab import *

def black_man(wave):
    N = 65536
    new_wave = []
    for n,s in enumerate(wave):
        W = 0.35875 - 0.48829 * cos(2*np.pi * n /N) + 0.14128 * cos(2*np.pi *2*n / N) - 0.01168 * cos(2*np.pi *3*n/N) 
        new_wave.append(W*s)
    return new_wave


def quantization(wave):
    s_8 = wave * ((2 ** 4) - 1) #プラスで4bit，マイナスで4bit
    s_8 = np.floor(s_8) #小数部切り捨て
    s_8 = s_8 / np.max(np.abs(s_8)) 

    return s_8 

def createSineWave (A, f0, fs, length):
    """振幅A、基本周波数f0、サンプリング周波数 fs、
    長さlength秒の正弦波を作成して返す"""
    N = 65536
    data = []
    # [-1.0, 1.0]の小数値が入った波を作成
    for n in arange(length * fs):  # nはサンプルインデックス
        s = A * np.sin(2 * np.pi * f0 * n / fs)
        # 振幅が大きい時はクリッピング
        if s > 1.0:  s = 1.0
        if s < -1.0: s = -1.0
        data.append(s)
    # [-32768, 32767]の整数値に変換
    # black = np.blackman(65536)
    # data = black_man(data[65536*3:-50000])
    # data = [int(x * 32767.0) for x in data]
    # data = quantization(data[-512:])
    plot(data[-512:])
    show()
    # バイナリに変換
    data = struct.pack("h" * len(data), *data)  # listに*をつけると引数展開される
    return data

if __name__ == "__main__" :
    f = 103/65536 
    data = createSineWave(0.25, f, 1, 65536*4)
    numpy.fft.fft(a, n=None, axis=-1, norm=None)

    # data = createSineWave(1, 440, 8000, 9)
    

