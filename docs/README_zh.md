# ASCII 视频播放器

这是一个在终端中以 ASCII 字符形式播放视频的 Python 程序。它使用 FFmpeg 提取视频帧，将其转换为灰度图像，然后将每个像素映射到 ASCII 字符，创建出类似字符画的效果。

## 功能特点

- 🎬 在终端中实时播放视频的 ASCII 艺术版本
- ⚡ 使用优化的算法实现快速帧处理
- 🖥️ 自动适配终端尺寸
- 📊 显示播放状态信息（帧数、耗时、FPS）
- 🔧 支持自定义帧率和分辨率

## 系统要求

- Python 3.6+
- FFmpeg（必须安装）

### 依赖安装

```bash
# 安装 Python 依赖
pip install -r requirements.txt

# 安装 FFmpeg（根据您的操作系统）

# Ubuntu/Debian
sudo apt install ffmpeg

# macOS
brew install ffmpeg

# Windows
# 从 https://ffmpeg.org/download.html 下载并添加到系统 PATH
```

## 安装步骤

1. 克隆或下载项目文件
2. 安装 Python 依赖：

   ```bash
   pip install -r requirements.txt
   ```

3. 确保 FFmpeg 已安装并可在命令行中访问

## 使用方法

进入`src`目录：

```bash
cd src
```

### 方式一：使用命令行参数

将 main.py 文件末尾的代码改为：

```python
if __name__ == "__main__":
    main()
```

```bash
# 基本用法
python main.py <视频文件路径>

# 指定帧率和宽度
python main.py <视频文件路径> --fps 30 --width 100

# 示例
python main.py "my_video.mp4" --fps 24 --width 120
```

### 方式二：直接修改代码

在 `main.py` 文件底部修改以下参数：

```python
if __name__ == "__main__":
    video_path = r"你的视频文件路径"
    play_video_in_ascii(video_path, 30, 2000)  # 帧率30，最大宽度2000
```

然后运行 `python main.py` 即可在终端中播放视频。

## 命令行参数

| 参数         | 描述                 | 默认值 |
| ------------ | -------------------- | ------ |
| `video_path` | 视频文件路径（必需） | -      |
| `--fps`      | 播放帧率             | 15     |
| `--width`    | ASCII 图像的最大宽度 | 80     |

## 工作原理

1. **视频处理**：使用 FFmpeg 提取视频帧，转换为灰度图像，并调整大小
2. **ASCII 转换**：将灰度像素值映射到一组 ASCII 字符（从暗到亮：@#\*+=-:.）
3. **终端渲染**：清除终端并显示当前帧的 ASCII 表示
4. **帧率控制**：通过调整读取和处理速度来控制播放速度

## 性能优化

- 使用预计算的字符映射表加速转换
- 使用更快的图像缩放算法（fast_bilinear）
- 直接处理灰度图像，避免颜色转换开销
- 预分配缓冲区减少内存分配

## 故障排除

### 常见问题

1. **"错误: 未找到 ffmpeg"**

   - 确保 FFmpeg 已正确安装并添加到系统 PATH

2. **ASCII 图像扭曲或尺寸不正确**

   - 调整 `--width` 参数或终端尺寸
   - 确保终端支持 ANSI 转义码

3. **播放速度太慢**
   - 降低 `--fps` 参数值
   - 减小 `--width` 参数值

### 退出程序

- 按 `Ctrl+C` 停止播放

## 自定义 ASCII 字符集

在 `main.py` 的 `convert_frame_to_ascii_fast` 函数中，可以修改 `ascii_chars` 变量来自定义字符集：

```python
# 默认字符集（从暗到亮）
ascii_chars = "@#*+=-:."

# 反转的字符集（从亮到暗）
# ascii_chars = " .:-=+*#@"

# 更详细的字符集
# ascii_chars = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "
```

## 注意事项

- 播放效果取决于终端尺寸和字体大小
- 高分辨率视频可能需要更多处理时间
- 部分终端可能不支持 ANSI 转义码，导致显示异常
- 确保终端有足够的高度显示完整的 ASCII 帧

## 许可证

[CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/)

此项目为开源项目，仅供学习和研究使用。

---

**提示**：为获得最佳效果，请使用支持 ANSI 转义码的现代终端，并调整终端窗口大小以适应视频比例。
