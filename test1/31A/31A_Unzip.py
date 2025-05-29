import json
import math
from matplotlib import pyplot as plt

""".31A文件的解析代码"""
def Dezip_31A(file_name):
    with open(file_name, 'rb+') as file:
        if file:
            info = file.read()
            value = []
            for i in range(len(info) - 3):
                if info[i] == 0x49 and info[i+1] == 0x53 and info[i+2] == 0x58:
                    n = []
                    for j in range(i, len(info)):
                        if info[j] == 0xFC:
                            n.append(int(info[j]))
                            break
                        else:
                            n.append(int(info[j]))
                    value.append(n)
        else:
            print("未找到制定文件!")
    file.close()
    return value

range_index = ['25.0 cm','50.0 cm','75.0 cm','1.0 cm','2.0 cm','3.0 cm','4.0 cm','5.0 cm','6.0 cm']
range_n = [4,6,8,10,20,30,40,50,60]

def Revalue(value):
    js = []
    for i in range(len(value)):
        info = value[i]
        if len(info) > 11:
            head_str = 'ISX' #之前有判断过文件头
            ID = hex(info[3])[2:]
            Serial_Status = bin(info[4] - 0b10000011)
            byte_high = (info[5] & 0x3E) >> 1
            byte_low = ((info[6] & 0x01) << 7) | (info[5] & 0x7F)
            Head_Pos = (byte_high << 8) | byte_low
            for j in range(len(range_n)):
                if info[7] == range_n[j]:
                    Rang_index_byte = range_index[j]
            High_Byte = (info[11] & 0x7E) >> 1
            Low_Byte = ((info[11] & 0x01) << 7) | (info[10] & 0x7F)
            Data_Bytes = (High_Byte << 8) | Low_Byte
            num = 400
            Termination_Byte = hex(info[-1])[2:]
            values = []
            for i in range(2,802,2):
                Rng_High_Byte = (info[11+i] & 0x7E) >> 1
                Rng_Low_Byte = ((info[11+i] & 0x01) << 7) | (info[10+i] & 0x7F)
                Range = (Rng_High_Byte<<8)|Rng_Low_Byte
                if Range < 1:
                    values.append(Rng_High_Byte)
                else:
                    values.append(Rng_Low_Byte)
            js.append(In_dir(head_str,ID,Serial_Status,Head_Pos,Rang_index_byte,Data_Bytes,num,Termination_Byte,values))
        else:
            print("值为空!")
    return js

def In_dir(head_str,ID,Serial_Status,Head_Pos,Rang_index_byte,Data_Bytes,num,Termination_Byte,values):
    #将数据存储为链表
    data_n = {
        "Header": head_str,
        "Head_ID": str(ID),
        "Serial_Status": str(Serial_Status),
        "Head_Position": Head_Pos,
        "Rang_index_byte": Rang_index_byte,
        "Number_of_Shots": num,
        "Data_Bytes": Data_Bytes,
        "Termination_Byte": Termination_Byte,
        "values":values
    }
    return data_n

def D3_plot(js):
    x = [];y = [];z = []
    for i in range(len(js)):
        if js[i]:
            value = js[i]["values"]
            head_pos = js[i]["Head_Position"]
            #坐标转化
            for j in range(0, len(value)):
                x.append(value[j]*math.cos(math.radians(0.9*j)+head_pos))
                y.append(value[j]*math.sin(math.radians(0.9*j)+head_pos))
                z.append(i)
        else:
            print(f"js{j}为空!")
    # 创建一个三维坐标系
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    # 绘制三维点云图
    ax.scatter(x, y, z, c='r')
   # 设置坐标轴标签
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title("31A 3D Figuer")
    # 显示图形
    plt.show()

if __name__ == "__main__":
    value = Dezip_31A(r"G:\竞赛学术\IOT\专题作业-发学生2024-04-23【第十周】\【专题一】数据解析-文件解析(2)\数据文件解析\31A声纳解析\houst.31A")
    js = Revalue(value)
    #用json格式存储
    with open("data.json",'w') as file:
        json.dump(js, file, indent=4)
        file.close()
    D3_plot(js[:50])#切50个数据画图，太大了跑不动