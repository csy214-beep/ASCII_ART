# -*- coding: UTF-8 -*-
"""
PROJECT_NAME ASCII_ART
PRODUCT_NAME PyCharm
NAME main
AUTHOR Pfolg
TIME 2025/8/19 19:04
"""
video_path = r"D:\download\【4K 60FPS】(全站最清晰画质 音频修复)Bad apple！！！坏苹果！！！.mp4"

import subprocess
import numpy as np
import sys
import os
import time
import argparse
from PIL import Image


def get_terminal_size():
    """获取终端大小"""
    try:
        cols, rows = os.get_terminal_size()
        return rows, cols
    except OSError:
        return 40, 80  # 默认终端大小


def convert_frame_to_ascii(image, width, height):
    """将图像帧转换为ASCII字符"""
    # 调整图像大小以匹配终端尺寸
    img = image.resize((width, height))

    # 转换为灰度图
    img = img.convert('L')

    # 将像素数据转换为numpy数组
    pixels = np.array(img)

    # ASCII字符集，从暗到亮排列
    ascii_chars = "@%#*+=-:. "  #

    # 将像素值映射到ASCII字符
    ascii_frame = ""
    for row in pixels:
        for pixel in row:
            # 将0-255的像素值映射到0-len(ascii_chars)-1的索引
            index = int(pixel / 255 * (len(ascii_chars) - 1))
            ascii_frame += ascii_chars[index]
        ascii_frame += "\n"

    return ascii_frame


def play_video_in_ascii(video_path, frame_rate=15, max_width=80):
    """将视频转换为ASCII艺术并在终端播放"""
    # 获取终端尺寸
    term_height, term_width = get_terminal_size()
    width = min(term_width, max_width)
    height = term_height - 1  # 留一行给状态信息

    # 检查ffmpeg是否可用
    try:
        subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("错误: 未找到ffmpeg，请先安装ffmpeg")
        print("在Ubuntu/Debian上: sudo apt install ffmpeg")
        print("在macOS上: brew install ffmpeg")
        print("在Windows上: 从https://ffmpeg.org/download.html下载")
        sys.exit(1)

    # 构建ffmpeg命令提取视频帧
    cmd = [
        'ffmpeg',
        '-i', video_path,  # 输入文件
        '-vf', f'fps={frame_rate},scale={width}:{height}:flags=neighbor',  # 设置帧率和缩放
        '-f', 'image2pipe',  # 输出到管道
        '-pix_fmt', 'rgb24',  # 像素格式
        '-vcodec', 'rawvideo',  # 视频编解码器
        '-'
    ]

    try:
        # 启动ffmpeg进程
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=10 ** 8)

        frame_size = width * height * 3  # RGB三个通道
        frame_count = 0
        start_time = time.time()

        while True:
            # 读取一帧
            raw_frame = process.stdout.read(frame_size)
            if not raw_frame:
                break

            # 将原始数据转换为图像
            frame = Image.frombytes('RGB', (width, height), raw_frame)

            # 转换为ASCII
            ascii_art = convert_frame_to_ascii(frame, width, height)

            # 清屏并显示ASCII艺术
            os.system("cls")
            # sys.stdout.write('\033[2J\033[H')  # ANSI转义序列清屏
            # sys.stdout.write(ascii_art)
            print('\033[2J\033[H')  # ANSI转义序列清屏
            print(ascii_art)

            # 显示状态信息
            elapsed = time.time() - start_time
            fps = frame_count / elapsed if elapsed > 0 else 0
            status = f"帧: {frame_count} | 耗时: {elapsed:.1f}s | FPS: {fps:.1f} | 按Ctrl+C退出"
            # sys.stdout.write(status)
            # sys.stdout.flush()
            print(status)
            frame_count += 1

            # 控制帧率
            time.sleep(1 / frame_rate)

    except KeyboardInterrupt:
        print("\n已停止播放")
    finally:
        process.terminate()


def main():
    parser = argparse.ArgumentParser(description='在终端中以ASCII艺术形式播放视频')
    parser.add_argument('video_path', help='视频文件路径')
    parser.add_argument('--fps', type=int, default=15, help='帧率 (默认: 15)')
    parser.add_argument('--width', type=int, default=80, help='最大宽度 (默认: 80)')

    args = parser.parse_args()

    if not os.path.isfile(args.video_path):
        print(f"错误: 文件 '{args.video_path}' 不存在")
        sys.exit(1)

    play_video_in_ascii(args.video_path, args.fps, args.width)


if __name__ == "__main__":
    # main()
    play_video_in_ascii(video_path, 60, 100)
