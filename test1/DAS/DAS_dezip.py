import struct
import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams["font.sans-serif"] = ["SimHei"]  # windows系统
plt.rcParams['axes.unicode_minus'] = False      #正常显示符号

def Dat_analyze(filename, num):
    datalist = []
    with open(filename, 'rb') as file:
        data = []
        try:
            while True:
                a = file.read(2)
                if a:
                    data.append(struct.unpack('<h', a)[0])
                else:
                    break
        except:
            print("读写失败,请检查给定的数值是否超过了其长度")
        file.close()
    for i in range(num):
        datalist.append(data[i])
    return datalist

def save_to_csv(data, num):
    time = []
    for i in range(num):
        time.append(i/2000)
        data[i] = float(data[i])
    datalist = {"data": data, "time": time}
    df = pd.DataFrame(datalist)
    plt.specgram(data, NFFT=1024, Fs=2000, scale_by_freq=True)
    plt.title('Data 瀑布图')
    plt.ylabel('Point [Hz]')
    plt.xlabel('Time [s]')
    plt.show()
    # 保存为CSV文件
    df.to_csv('data.csv', index=False)

if __name__ == "__main__":
    file_str01 = "G:\IOT\专题作业-发学生2024-04-23【第十周】\【专题一】数据解析-文件解析(2)\数据文件解析\DAS文件解析\DASNo20CH1Diff_0_2000_240318.dat"
    file_str02 = "G:\IOT\专题作业-发学生2024-04-23【第十周】\【专题一】数据解析-文件解析(2)\数据文件解析\DAS文件解析\DASNo21CH1Diff_0_2000_240318.dat"
    num = int(input("请输入需要的数据多少："))
    data = Dat_analyze(file_str01, num)
    save_to_csv(data, num)
    with open("data.dat", 'w') as file:
        for i in range(len(data)):
            file.write(str(data[i]))
        file.close()