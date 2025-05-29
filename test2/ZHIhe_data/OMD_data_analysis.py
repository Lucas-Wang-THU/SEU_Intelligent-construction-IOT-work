from matplotlib import pyplot as plt
import numpy as np
import pywt

# 读取文件数据并将其转换为浮点数列表
def read_data(file_name):
    with open(file_name, 'r') as file:
        data = file.read().split()
        return [float(x) for x in data]

def draw(data, t_str, f_str):
    plt.figure(figsize=(16,8))
    plt.plot(data)
    plt.xlabel("Time")
    plt.ylabel("data")
    plt.title(t_str)
    plt.savefig(f_str)

def denoise(data):
    coeffs = pywt.wavedec(data, 'db4', level=5)
    coeffs[0] = np.zeros_like(coeffs[0])
    denoised_signal = pywt.waverec(coeffs, 'db4')
    return denoised_signal

if __name__ == "__main__":
    path = r"G:\IOT\专题作业-发学生2024-04-23【第十周】\【专题二】数据智能处理-作业数据\智盒数据处理\泗安塘大桥3月份位移数据\OneMonthData.txt"
    data = read_data(path)
    draw(data, "OMD_Original_data", "OMD_Original_data.jpg")
    data_cl = denoise(data)
    draw(data_cl, "OMD_Clean_data", "OMD_Clean_data.jpg")