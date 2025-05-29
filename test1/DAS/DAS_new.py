import csv
import struct
import wave
import numpy as np
import matplotlib.pyplot as plt
import pywt


def write_data_csv(values):
    with open(f"caculate_data.csv", 'a') as f:
        writer = csv.writer(f)
        for value in values:
            writer.writerow([value])


def draw(data):
    plt.figure(figsize=(16, 8))
    plt.plot(data)
    plt.xlabel("Time")
    plt.ylabel("data")
    plt.title("Origin_data")
    plt.savefig("Origin_data.png")


def parse_one_point(packet):
    try:
        values = []
        for byte_data in packet:
            value = struct.unpack('<h', byte_data)[0]
            values.append(value)
        write_data_csv(values)
        #draw(values)
    except Exception as e:
        print(f"2解析错误：{e}")


def save_one_point_dat(wav_dat):
    with open("data.dat", 'wb') as file:
        for i in range(len(wav_dat)):
            file.write(wav_dat[i])
        file.close()


def parse_one_seconds(buffer):
    plt.figure(1)
    h = plt.imshow(buffer.T, aspect='auto', cmap='turbo', origin='lower')
    plt.colorbar(h)
    clim = [0, 40]
    h.set_clim(clim)
    plt.xlabel('Channels')
    plt.ylabel('Times(s)')
    plt.ylim(0, buffer.shape[1])
    plt.xlim(0, buffer.shape[0])
    plt.gca().invert_yaxis()
    plt.gca().set_aspect('auto')
    plt.gca().tick_params(axis='both', which='major', labelsize=15)
    plt.savefig("Figure.png")
    plt.close()


def read_dat_file(filename):
    try:
        # 读取文件信息
        with open(filename, 'rb') as file:
            datas = file.read()
            length = len(datas)
            packet_len = int(length / 4000)
            print(f"文件读取完成,包含{length}字节,采样点数{packet_len},采样时间{int(packet_len/2000)}")
            one_point_pack = [];
            wav_dat = [];
            values = []
            for i in range(packet_len):
                data = datas[i * 4000: i * 4000 + 2]
                one_point_pack.append(data)
                wav_dat.append(data)
            for i in range(2000 * 2000, 2 * 2000 * 2000):
                data = datas[i * 2: i * 2 + 2]
                value = struct.unpack('<h', data)[0]
                values.append(value)
            parse_one_point(one_point_pack)
            save_one_point_dat(wav_dat)
            #print(len(wav_dat[0]))

            # 获取某一秒的所有数据，生成瀑布图
            #values = denoise(values)
            parse_one_seconds(np.reshape(np.array(values), (2000, 2000)))
    except Exception as e:
        print(f"1解析错误：{e}")


if __name__ == "__main__":
    filePath = r"G:\竞赛学术\IOT\专题作业-发学生2024-04-23【第十周】\【专题一】数据解析-文件解析(2)\数据文件解析\DAS文件解析\DASNo20CH1Diff_0_2000_240318.dat"
    read_dat_file(filePath)
    channels = 1
    sample_width = 2
    sample_rate = 2000
    with open("data.dat", 'rb') as file:
        byte_data = file.read()
    audio_data = np.frombuffer(byte_data, dtype=np.int16)
    print(audio_data.shape)
    with wave.open("output.wav", 'wb') as wav_file:
        wav_file.setnchannels(channels)
        wav_file.setsampwidth(sample_width)
        wav_file.setframerate(sample_rate)
        wav_file.setnframes(len(audio_data))
        wav_file.writeframes(audio_data.tobytes())

    print("转化完成")
