import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
from tkinter import Tk, filedialog
from matplotlib import rcParams

# 设置支持中文的字体为宋体
rcParams['font.sans-serif'] = ['SimSun']  # 设置字体为宋体
rcParams['axes.unicode_minus'] = False   # 解决负号显示为方框的问题

# 初始化牛顿环的计算函数
def generate_newton_rings(radius_curvature, wavelength, size=500):
    x = np.linspace(-1, 1, size)  # 生成 x 坐标
    y = np.linspace(-1, 1, size)  # 生成 y 坐标
    X, Y = np.meshgrid(x, y)  # 创建网格
    R = np.sqrt(X ** 2 + Y ** 2)  # 计算每个点到中心的距离
    pattern = np.cos((2 * np.pi / wavelength) * (R ** 2 / (2 * radius_curvature)))  # 计算干涉图案
    return pattern

# 主程序设计
def main():
    # 初始化参数
    default_radius = 50  # 默认曲率半径
    default_wavelength = 0.5  # 默认波长
    size = 500  # 图像分辨率

    # 生成图像
    fig, ax = plt.subplots()  # 创建画布
    plt.subplots_adjust(bottom=0.35)  # 调整布局，预留按钮空间
    pattern = generate_newton_rings(default_radius, default_wavelength, size)  # 生成牛顿环图案
    im = ax.imshow(pattern, cmap='Reds', extent=[-1, 1, -1, 1])  # 使用红色调显示图像

    # 添加滑块
    ax_radius = plt.axes([0.25, 0.2, 0.65, 0.03])  # 曲率半径滑块的位置
    ax_wavelength = plt.axes([0.25, 0.15, 0.65, 0.03])  # 波长滑块的位置
    slider_radius = Slider(ax_radius, '曲率半径', 10, 100, valinit=default_radius)  # 曲率半径滑块
    slider_wavelength = Slider(ax_wavelength, '波长', 0.1, 1.0, valinit=default_wavelength)  # 波长滑块

    # 滑块事件
    def update(val):
        radius = slider_radius.val  # 获取曲率半径滑块的值
        wavelength = slider_wavelength.val  # 获取波长滑块的值
        pattern = generate_newton_rings(radius, wavelength, size)  # 更新牛顿环图案
        im.set_data(pattern)  # 更新显示的图像
        fig.canvas.draw_idle()  # 刷新画布

    slider_radius.on_changed(update)  # 绑定曲率半径滑块的事件
    slider_wavelength.on_changed(update)  # 绑定波长滑块的事件

    # 添加重置按钮
    reset_ax = plt.axes([0.8, 0.025, 0.1, 0.04])  # 重置按钮的位置
    reset_button = Button(reset_ax, '重置')

    def reset(event):
        slider_radius.reset()  # 重置曲率半径滑块
        slider_wavelength.reset()  # 重置波长滑块

    reset_button.on_clicked(reset)  # 绑定重置按钮的事件

    # 添加保存按钮
    save_ax = plt.axes([0.65, 0.025, 0.1, 0.04])  # 保存按钮的位置
    save_button = Button(save_ax, '保存图像')

    def save_image(event):
        root = Tk()
        root.withdraw()  # 隐藏主窗口
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG 文件", "*.png"), ("所有文件", "*.*")],
            title="保存图像"
        )
        if file_path:
            plt.savefig(file_path)  # 保存当前图像为文件
            print(f"图像已保存为 {file_path}")

    save_button.on_clicked(save_image)  # 绑定保存按钮的事件

    plt.show()  # 显示图形界面

if __name__ == '__main__':
    main()
