# -*- coding: UTF-8 -*-
"""
PROJECT_NAME ASCII_ART
PRODUCT_NAME PyCharm
NAME test2
AUTHOR Pfolg
TIME 2025/8/19 19:26
"""
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


def convert_frame_to_ascii_fast(pixels, width, height):
    """快速将图像帧转换为ASCII字符"""
    # 简化的ASCII字符集，从暗到亮排列
    ascii_chars = "@#*+=-:."
    # ascii_chars = " .:-=+*#@"

    # 预计算字符映射
    char_map = [ascii_chars[int(i / 255 * (len(ascii_chars) - 1))] for i in range(256)]

    # 使用列表推导式构建ASCII帧，比字符串连接快得多
    ascii_lines = []
    for i in range(height):
        # 使用生成器表达式和join，比字符串连接快
        line = ''.join(char_map[pixel] for pixel in pixels[i * width : (i + 1) * width])
        ascii_lines.append(line)

    return '\n'.join(ascii_lines)


def play_video_in_ascii(video_path, frame_rate=15, max_width=80):
    """将视频转换为ASCII艺术并在终端播放"""
    # 获取终端尺寸
    term_height, term_width = get_terminal_size()
    width = min(term_width, max_width)
    height = term_height  # - 1  # 留一行给状态信息

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
        '-i',
        video_path,  # 输入文件
        '-vf',
        f'fps={frame_rate},scale={width}:{height}:flags=fast_bilinear',  # 使用更快的缩放算法
        '-f',
        'image2pipe',  # 输出到管道
        '-pix_fmt',
        'gray',  # 直接输出灰度图像，减少处理
        '-vcodec',
        'rawvideo',  # 视频编解码器
        '-',
    ]

    try:
        # 启动ffmpeg进程
        process = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=10**8
        )

        frame_size = width * height  # 灰度图像只有一个通道
        frame_count = 0
        start_time = time.time()

        # 预分配缓冲区
        frame_buffer = bytearray(frame_size)

        while True:
            # 读取一帧到预分配的缓冲区
            bytes_read = process.stdout.readinto(frame_buffer)
            if bytes_read != frame_size:
                break

            # 直接使用numpy数组处理灰度值
            pixels = np.frombuffer(frame_buffer, dtype=np.uint8)

            # 转换为ASCII
            ascii_art = convert_frame_to_ascii_fast(pixels, width, height)

            # 清屏并显示ASCII艺术
            sys.stdout.write('\033[H')
            # sys.stdout.write('\033[2J\033[H')
            sys.stdout.write(ascii_art)

            # 显示状态信息
            elapsed = time.time() - start_time
            fps = frame_count / elapsed if elapsed > 0 else 0
            status = f"帧: {frame_count} | 耗时: {elapsed:.1f}s | FPS: {fps:.1f} | 按Ctrl+C退出"
            # sys.stdout.write(status)
            sys.stdout.flush()

            frame_count += 1
            # 控制帧率
            # time.sleep(1 / frame_rate)

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
    video_path = r"F:\videosCopy\Haku-Bad Boy\pro.mp4"
    play_video_in_ascii(video_path, 30, 2000)
