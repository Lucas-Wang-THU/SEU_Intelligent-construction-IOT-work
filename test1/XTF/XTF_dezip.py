import struct
import os
import json
import matplotlib.pyplot as plt
import numpy as np


def Write_json(js, name):
    with open(name,'w') as file:
        json.dump(js, file, indent=4)
        file.close()

def Dezip_XTFFILEHEADER(filename):
    file_size = os.path.getsize(filename)
    with open(filename, 'rb') as f:
        xtf_file_header = f.read(1024)
        RecordingProgramVersion = xtf_file_header[10:18].decode().strip(b'\x00'.decode())
        SonarName = xtf_file_header[18:34].decode().strip(b'\x00'.decode())
        HXTFFILHEADER = {
            "FileFormat": int.from_bytes(xtf_file_header[0:1], 'little'),
            "SystemType": int.from_bytes(xtf_file_header[1:2], 'little'),
            "RecordingProgramName": xtf_file_header[2:10].decode(),
            "RecordingProgramVersion": RecordingProgramVersion,
            "SonarName": SonarName,
            "SensorsType": int.from_bytes(xtf_file_header[34:36], "little"),
            "NoteString": xtf_file_header[36:100].decode().strip(b'\x00'.decode()),
            "ThisFileName": xtf_file_header[100:164].decode().strip(b'\x00'.decode()),
            "NavUnits": int.from_bytes(xtf_file_header[164:166], "little"),
            "NumberOfSonarChannels": int.from_bytes(xtf_file_header[166:168], "little"),
            "NumberOfBathymetryChannels": int.from_bytes(xtf_file_header[168:170], "little"),
            "NumberOfSnippetChannels": int.from_bytes(xtf_file_header[170:171], "little"),
            "NumberOfForwardLookArrays": int.from_bytes(xtf_file_header[171:172], "little"),
            "NumberOfEchoStrengthChannels": int.from_bytes(xtf_file_header[172:174], "little"),
            "NumberOfInterferometryChannels":int.from_bytes(xtf_file_header[174:175], "little"),
            "Reserved1": int.from_bytes(xtf_file_header[174:175], "little"),
            "Reserved2": int.from_bytes(xtf_file_header[175:176], "little"),
            "Reserved3": int.from_bytes(xtf_file_header[176:177], "little"),
            "ReferencePointHeight": struct.unpack('<f', xtf_file_header[178:182])[0],
            "ProjectionType": int.from_bytes(xtf_file_header[182:194], "little"),
            "SpheriodType": int.from_bytes(xtf_file_header[194:204], "little"),
            "NavigationLatency": struct.unpack('<f', xtf_file_header[204:208])[0],
            "OriginY": struct.unpack('<f', xtf_file_header[208:212])[0],
            "OriginX": struct.unpack('<f', xtf_file_header[212:216])[0],
            "NavOffsetY": struct.unpack('<f', xtf_file_header[216:220])[0],
            "NavOffsetX": struct.unpack('<f', xtf_file_header[220:224])[0],
            "NavOffSetZ": struct.unpack('<f', xtf_file_header[224:228])[0],
            "NavOffsetYaw": struct.unpack('<f', xtf_file_header[228:232])[0],
            "MRUOffsetY": struct.unpack('<f', xtf_file_header[232:236])[0],
            "MRUOffsetX": struct.unpack('<f', xtf_file_header[236:240])[0],
            "MRUOffsetZ": struct.unpack('<f', xtf_file_header[240:244])[0],
            "MRUOffsetYaw": struct.unpack('<f', xtf_file_header[244:248])[0],
            "MRUOffsetPitch": struct.unpack('<f', xtf_file_header[248:252])[0],
            "MRUOffsetRoll": struct.unpack('<f', xtf_file_header[252:256])[0],
            "ChanInfo": int.from_bytes(xtf_file_header[256:257], "little"),
        }
        Write_json(HXTFFILHEADER, "HXTFFILHEADER.json")
        firstBuf = f.read(20)
        bytesNum = struct.unpack('<i', firstBuf[10:14])[0]

        # 获取所有的XTFPING数据包数量
        msgbuf = f.read(file_size)
        msgStr = msgbuf.hex()
        last = msgStr.rfind('208e0000')
        total_packet_num = int((last / 2 + 10 + bytesNum) / bytesNum) + 1
        xtf_ping = []
        #f.close()
        # 循环读取
        for i in range(total_packet_num):
            if f.closed == False:
                f.seek(bytesNum * i)
                buffer = f.read(bytesNum)
                # XTF头文件
                XTFPINGHEADER = {
                    "MagicNumber": f"0x{format(int.from_bytes(buffer[0:2], 'little'), '04x')}",
                    "HeaderType": int.from_bytes(buffer[2:3], 'little'),
                    "SubChannelNumber": int.from_bytes(buffer[3:4], 'little'),
                    "NumChansToFollow": struct.unpack('<H', buffer[4:6])[0],
                    "Reserved1": struct.unpack('<H', buffer[6:8])[0],
                    "NumBytesThisRecord": struct.unpack('<H', buffer[10:12])[0],
                    "Year": struct.unpack('<H', buffer[14:16])[0],
                    "Month": int.from_bytes(buffer[16:17], 'little'),
                    "Hour": int.from_bytes(buffer[17:18], 'little'),
                    "Minute": int.from_bytes(buffer[18:19], 'little'),
                    "Second": int.from_bytes(buffer[19:20], 'little'),
                    "HSeconds": int.from_bytes(buffer[20:21], 'little'),
                    "JulianDay": struct.unpack('<H', buffer[22:24])[0],
                    "EventNumber": struct.unpack('<H', buffer[24:26])[0],
                    "PingNumber": struct.unpack('<H', buffer[28:30])[0],
                    "SoundVelocity": struct.unpack('<I', buffer[32:36])[0],
                    "OceanTide": struct.unpack('<I', buffer[36:40])[0],
                    "Reserved2": struct.unpack('<H', buffer[40:42])[0],
                    "ConductivityFreq": struct.unpack('<f', buffer[44:48])[0],
                    "TemperatureFreq": struct.unpack('<f', buffer[48:52])[0],
                    "PressureFreq": struct.unpack('<f', buffer[52:56])[0],
                    "PressureTemp": struct.unpack('<f', buffer[56:60])[0],
                    "Conductivity": struct.unpack('<f', buffer[60:64])[0],
                    "WaterTemperature": struct.unpack('<f', buffer[64:68])[0],
                    "Pressure": struct.unpack('<f', buffer[68:72])[0],
                    "ComputedSoundVelocity": struct.unpack('<f', buffer[72:76])[0],
                    "MagX": struct.unpack('<f', buffer[76:80])[0],
                    "MagY": struct.unpack('<f', buffer[80:84])[0],
                    "MagZ": struct.unpack('<f', buffer[84:88])[0],
                    "AuxVal1": struct.unpack('<f', buffer[88:92])[0],
                    "AuxVal2": struct.unpack('<f', buffer[92:96])[0],
                    "AuxVal3": struct.unpack('<f', buffer[96:100])[0],
                    "Reserved3": struct.unpack('<f', buffer[100:104])[0],
                    "Reserved4": struct.unpack('<f', buffer[104:108])[0],
                    "Reserved5": struct.unpack('<f', buffer[108:112])[0],
                    "SpeedLog": struct.unpack('<f', buffer[112:116])[0],
                    "Turbidity": struct.unpack('<f', buffer[116:120])[0],
                    "ShipSpeed": struct.unpack('<f', buffer[120:124])[0],
                    "ShipGyro": struct.unpack('<f', buffer[124:128])[0],
                    "ShipYcoordinate": struct.unpack('<d', buffer[128:136])[0],
                    "ShipXcoordinate": struct.unpack('<d', buffer[136:144])[0],
                    "ShipAltitude": struct.unpack('<H', buffer[144:146])[0],
                    "ShipDepth": struct.unpack('<H', buffer[146:148])[0],
                    "FixTimeHour": int.from_bytes(buffer[148:149], 'little'),
                    "FixTimeMinute": int.from_bytes(buffer[149:150], 'little'),
                    "FixTimesecond": int.from_bytes(buffer[150:151], 'little'),
                    "FixTimeHsecond": int.from_bytes(buffer[151:152], 'little'),
                    "SensorSpeed": struct.unpack('<f', buffer[152:156])[0],
                    "KP": struct.unpack('<f', buffer[156:160])[0],
                    "SensorYcoordinate": struct.unpack('<d', buffer[160:168])[0],
                    "SensorXcoordinate": struct.unpack('<d', buffer[168:176])[0],
                    "SonarStatus": struct.unpack('<H', buffer[176:178])[0],
                    "RangeToFish": struct.unpack('<H', buffer[178:180])[0],
                    "CableOut": struct.unpack('<H', buffer[180:182])[0],
                    "Layback": struct.unpack('<f', buffer[184:188])[0],
                    "CableTension": struct.unpack('<f', buffer[188:192])[0],
                    "SensorDepth": struct.unpack('<f', buffer[192:196])[0],
                    "SensorPrimaryAltitude": struct.unpack('<f', buffer[196:200])[0],
                    "SensorAuxAltitude": struct.unpack('<f', buffer[200:204])[0],
                    "SensorPitch": struct.unpack('<f', buffer[204:208])[0],
                    "SensorRoll": struct.unpack('<f', buffer[208:212])[0],
                    "SensorHeading": struct.unpack('<f', buffer[212:216])[0],
                    "Heave": struct.unpack('<f', buffer[216:220])[0],
                    "Yaw": struct.unpack('<f', buffer[220:224])[0],
                    "AltitudeTimeTeg": struct.unpack('<I', buffer[224:228])[0],
                    "DOT": struct.unpack('<f', buffer[228:232])[0],
                    "NavFixMilliseconds": struct.unpack('<I', buffer[232:236])[0],
                    "ComputerClockHour": int.from_bytes(buffer[236:237], 'little'),
                    "ComputerClockMinute": int.from_bytes(buffer[237:238], 'little'),
                    "ComputerClockSecond": int.from_bytes(buffer[238:239], 'little'),
                    "ComputerClockHsec": int.from_bytes(buffer[239:240], 'little'),
                    "FishPositionDeltaX": struct.unpack('<h', buffer[240:242])[0],
                    "FishPositionDeltaY": struct.unpack('<h', buffer[242:244])[0],
                    "FishPositionErrorCode": int.from_bytes(buffer[244:245], 'little'),
                    "OptionalOffset": struct.unpack('<I', buffer[245:249])[0],
                    "CableOutHundredths": int.from_bytes(buffer[249:250], 'little'),
                    "ReservedSpace2": int.from_bytes(buffer[250:256], 'little'),
                }

                # 第一个XTF通道数据
                XTFPINGCHANHEADER_1 = {
                    "ChannelNumber": int.from_bytes(buffer[256:258], 'little'),
                    "DownsampleMethod": int.from_bytes(buffer[258:260], 'little'),
                    "SlantRange": struct.unpack('<f', buffer[260:264])[0],
                    "GroundRange": struct.unpack('<f', buffer[264:268])[0],
                    "TimeDelay": struct.unpack('<f', buffer[268:272])[0],
                    "TimeDuraytion": struct.unpack('<f', buffer[272:276])[0],
                    "SecondPerPing": struct.unpack('<f', buffer[276:280])[0],
                    "ProcessingFlags": struct.unpack('<H', buffer[280:282])[0],
                    "Frequecy": struct.unpack('<H', buffer[282:284])[0],
                    "InitialGainCode": struct.unpack('<H', buffer[284:286])[0],
                    "GainCode": struct.unpack('<H', buffer[286:288])[0],
                    "BandWidth": struct.unpack('<H', buffer[288:290])[0],
                    "ContactyNumber": struct.unpack('<I', buffer[290:294])[0],
                    "ContactClassification": struct.unpack('<H', buffer[294:296])[0],
                    "ContactSubNumber": int.from_bytes(buffer[296:297], 'little'),
                    "ContactType": int.from_bytes(buffer[297:298], 'little'),
                    "NumSamples": struct.unpack('<I', buffer[298:302])[0],
                    "MillivoltScale": struct.unpack('<H', buffer[302:304])[0],
                    "ContactTimeOffTrack": struct.unpack('<f', buffer[304:308])[0],
                    "ContactCloseNumber": int.from_bytes(buffer[308:309], 'little'),
                    "Reserved2": int.from_bytes(buffer[309:310], 'little'),
                    "FixedVSOP": struct.unpack('<f', buffer[310:314])[0],
                    "Weight": struct.unpack('<h', buffer[314:316])[0],
                    "ReservedSpace": int.from_bytes(buffer[316:320], 'little'),
                }

                # 最后一个数据包长度可能会不一样，所以增加一个判断
                # 根据CHAN通道后的数据长度解析出图片数据
                """if i == total_packet_num - 1:
                    photo_data_length = int((bytesNum - 384) / 2) + 320
                    channel_data = buffer[320:photo_data_length]
                    packet_length = int(len(channel_data) / 2)
                    print("图片数据包长度：", len(channel_data))
                    data = struct.unpack('>' + 'h' * packet_length, channel_data)

                    # 图片的reshape中的大小根据packet_length设置
                    data = np.array(data).reshape((60, 150))
                    plt.imshow(data, cmap='gray')
                    plt.savefig(f"/pic/channel_1_{i}.png")
                else:
                    photo_data_length = int((bytesNum - 384) / 2) + 320
                    channel_data = buffer[320:photo_data_length]
                    packet_length = int(len(channel_data) / 2)
                    print("图片数据包长度：", len(channel_data))
                    data = struct.unpack('>' + 'h' * packet_length, channel_data)
                    # 图片的reshape中的大小根据packet_length设置
                    data = np.array(data).reshape((60, 150))
                    plt.imshow(data, cmap='gray')
                    plt.savefig(f"/pic/channel_1_{i}.png")

                # 解析第二个通道数据包
                if i != total_packet_num - 1:
                    photo_data_length = int((bytesNum - 384) / 2) + 320
                    buf = buffer[photo_data_length:]
                    channel_data = buf[64:]
                    packet_length = int(len(channel_data) / 2)
                    #print("图片数据包长度：", len(channel_data))
                    data = struct.unpack('>' + 'h' * packet_length, channel_data)

                    # 图片的reshape中的大小根据packet_length设置
                    data = np.array(data).reshape((60, 150))
                    plt.imshow(data, cmap='gray')
                    plt.savefig(f"/pic/channel_2_{i}.png")
                else:
                    photo_data_length = int((bytesNum - 384) / 2) + 320
                    buf = buffer[photo_data_length:]
                    channel_data = buf[64:int((bytesNum - 384) / 2) + 64]
                    packet_length = int(len(channel_data) / 2)
                    #print("图片数据包长度：", len(channel_data))
                    data = struct.unpack('>' + 'h' * packet_length, channel_data)
                    # D:/pycharm/pythonProject2/XTF/
                    # 图片的reshape中的大小根据packet_length设置
                    data = np.array(data).reshape((60, 150))
                    plt.imshow(data, cmap='gray')
                    plt.savefig(f"/pic/channel_2_{i}.png")"""

                # 第二个XTF通道数据
                XTFPINGCHANHEADER_2 = {
                    "ChannelNumber": int.from_bytes(buffer[320:322], 'little'),
                    "DownsampleMethod": int.from_bytes(buffer[322:324], 'little'),
                    "SlantRange": struct.unpack('<f', buffer[324:328])[0],
                    "GroundRange": struct.unpack('<f', buffer[328:332])[0],
                    "TimeDelay": struct.unpack('<f', buffer[332:336])[0],
                    "TimeDuraytion": struct.unpack('<f', buffer[336:340])[0],
                    "SecondPerPing": struct.unpack('<f', buffer[340:344])[0],
                    "ProcessingFlags": struct.unpack('<H', buffer[344:346])[0],
                    "Frequecy": struct.unpack('<H', buffer[346:348])[0],
                    "InitialGainCode": struct.unpack('<H', buffer[348:350])[0],
                    "GainCode": struct.unpack('<H', buffer[350:352])[0],
                    "BandWidth": struct.unpack('<H', buffer[352:354])[0],
                    "ContactyNumber": struct.unpack('<I', buffer[354:358])[0],
                    "ContactClassification": struct.unpack('<H', buffer[358:360])[0],
                    "ContactSubNumber": int.from_bytes(buffer[360:361], 'little'),
                    "ContactType": int.from_bytes(buffer[361:362], 'little'),
                    "NumSamples": struct.unpack('<I', buffer[362:366])[0],
                    "MillivoltScale": struct.unpack('<H', buffer[366:368])[0],
                    "ContactTimeOffTrack": struct.unpack('<f', buffer[368:372])[0],
                    "ContactCloseNumber": int.from_bytes(buffer[372:373], 'little'),
                    "Reserved2": int.from_bytes(buffer[373:374], 'little'),
                    "FixedVSOP": struct.unpack('<f', buffer[374:378])[0],
                    "Weight": struct.unpack('<h', buffer[378:380])[0],
                    "ReservedSpace": int.from_bytes(buffer[380:384], 'little'),
                }
                # 保存缓冲区
                xtf_ping.append({f"XTFPINGHEADER_{i}": XTFPINGHEADER, f"XTFPINGCHANHEADER_1_{i}": XTFPINGCHANHEADER_1,
                                 f"XTFPINGCHANHEADER_2_{i}": XTFPINGCHANHEADER_2})

    with open("XTFPING.json", 'w') as file:
        json.dump(xtf_ping, file, indent=4)
        file.close()

if __name__ == "__main__":
    file_path = r"G:\竞赛学术\IOT\专题作业-发学生2024-04-23【第十周】\【专题一】数据解析-文件解析(2)\数据文件解析\XTF声纳解析\20221118_113232_01.XTF"
    XTFFILEHEADER = Dezip_XTFFILEHEADER(file_path)

