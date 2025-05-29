import pandas as pd
from pykalman import KalmanFilter
from matplotlib import pyplot as plt

def Kalman1D(x, damping=1):
    """
    卡尔曼滤波，缺点：耗时较长
    :param x 时间序列
    :damping 协方差，控制参数
    :return x_hat 平滑后的时间序列
    """
    # To return the smoothed time series data
    observation_covariance = damping
    initial_value_guess = x[0]
    transition_matrix = 1
    transition_covariance = 0.1
    kf = KalmanFilter(
        initial_state_mean=initial_value_guess,
        initial_state_covariance=observation_covariance,
        observation_covariance=observation_covariance,
        transition_covariance=transition_covariance,
        transition_matrices=transition_matrix
    )
    x_hat, state_cov = kf.smooth(x)
    return x_hat

def Read_xlsx(filename):
    xlsx = pd.read_excel(filename)
    xlsx.info()
    data = xlsx.values
    return data

def draw(data, t_str, f_str):
    plt.figure(figsize=(16,8))
    plt.plot(data)
    plt.xlabel("Time")
    plt.ylabel("data")
    plt.title(t_str)
    plt.savefig(f_str)

if __name__ == "__main__":
    path = r"G:\IOT\专题作业-发学生2024-04-23【第十周】\【专题二】数据智能处理-作业数据\智盒数据处理\泗安塘大桥3月份位移数据\320\10_oclock.xlsx"
    data = Read_xlsx(path)
    draw(data, "320_0_clock_original_data", "320_10_clock_original_data.jpg")
    data_cl = Kalman1D(data)
    draw(data_cl, "320_0_clock_Clean_data", "320_10_clock_Clean_data.jpg")