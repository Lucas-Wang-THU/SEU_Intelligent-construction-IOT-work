import scipy.io as sio
import numpy as np
import pywt
import matplotlib.pyplot as plt

def draw(data,name,n, num):
    plt.figure(1)
    h = plt.imshow(data.T, aspect='auto', cmap='turbo', origin='lower')
    plt.colorbar(h)
    clim = [0, num]
    h.set_clim(clim)
    plt.xlabel('Channels')
    plt.ylabel('Times(s)')
    plt.ylim(0, data.shape[1])
    plt.xlim(0, data.shape[0])
    plt.gca().invert_yaxis()
    plt.gca().set_aspect('auto')
    plt.gca().tick_params(axis='both', which='major', labelsize=15)
    plt.savefig(name+str(n)+".png")
    plt.close()

def DAS_orgin(filename):
    data = sio.loadmat(filename)
    print(data.keys())
    data_or = data['data_original']
    draw(data_or, "Original_data_waterfall", 0, 10)
    return data_or

def denoise(data):
    for i in range(25):
        for j in range(data.shape[1]):
            data[i][j] = 0
    # 进行小波变换
    coeffs = pywt.wavedec(data, 'db4', level=15)
    # 设置软阈值
    threshold = np.median(np.abs(coeffs[-1])) / 0.6745
    coeffs = [pywt.threshold(coeff, threshold, mode='soft') for coeff in coeffs]
    coeffs = [pywt.threshold(coeff, threshold, mode='less') for coeff in coeffs]
    data = pywt.waverec(coeffs, 'db4')
    # 进行小波变换
    coeffs = pywt.wavedec(data, 'db2', level=15)
    # 设置软阈值
    threshold = np.sqrt(2 * np.log(len(coeffs)))
    coeffs = [pywt.threshold(coeff, threshold, mode='less') for coeff in coeffs]
    data = pywt.waverec(coeffs, 'db2')
    return data

if __name__ == "__main__":
    datapath = r"G:\竞赛学术\IOT\专题作业-发学生2024-04-23【第十周】\【专题二】数据智能处理-作业数据\DAS数据处理\数据\三破数据-电镐施工\data_original.mat"
    data_or = DAS_orgin(datapath)
    print(data_or.shape)
    data_denoise = denoise(data_or)
    draw(data_denoise, "Data_denoise_waterfall", 0, 2)