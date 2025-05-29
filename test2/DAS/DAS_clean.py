import scipy.io as sio
import numpy as np
import pywt
import matplotlib.pyplot as plt

def DAS_orgin(filename):
    data = sio.loadmat(filename)
    print(data.keys())
    data_or = data['data_original']
    plt.specgram(data_or, NFFT=256, Fs=500, noverlap=150)
    plt.title('Data_original_waterfall')
    plt.ylabel('Time [s]')
    plt.xlabel('Chanel')
    plt.savefig("Data_original_waterfall.png")
    return data_or

def denoise(data):
    for i in range(data.shape[0]):
        n = data[i]
        # 对信号进行小波变换
        coeffs = pywt.wavedec(n, 'db4', level=1)
        # 通过阈值处理细节系数
        threshold = np.sqrt(2 * np.log(len(n)))
        coeffs = [pywt.threshold(coeff, threshold, mode='soft') for coeff in coeffs]
        # 通过逆小波变换重构信号
        denoised_signal = pywt.waverec(coeffs, 'db4')
        data[i] =denoised_signal
    return data

def waterfall_pic(data,n):
    plt.specgram(data, NFFT=256, Fs=500, noverlap=150)
    plt.title('Data_original_waterfall')
    plt.ylabel('Time [s]')
    plt.xlabel('Chanel')
    plt.savefig("Data_denoise_"+str(n)+"_waterfall.png")

if __name__ == "__main__":
    datapath = r"G:\IOT\专题作业-发学生2024-04-23【第十周】\【专题二】数据智能处理-作业数据\DAS数据处理\数据\三破数据-电镐施工\data_original.mat"
    data_or = DAS_orgin(datapath)
    print(data_or.shape)
    data_denoise = denoise(data_or)
    waterfall_pic(data_denoise, 1)