# ASCII Video Player

This is a Python program that plays videos in ASCII character form in the terminal. It uses FFmpeg to extract video frames, converts them to grayscale images, and then maps each pixel to ASCII characters, creating an effect similar to character art.

[简体中文](docs/README_zh.md)

## Features

- 🎬 Real-time playback of videos as ASCII art in the terminal
- ⚡ Fast frame processing with optimized algorithms
- 🖥️ Automatic adaptation to terminal size
- 📊 Displays playback status information (frame count, elapsed time, FPS)
- 🔧 Supports custom frame rates and resolutions

## System Requirements

- Python 3.6+
- FFmpeg (required)

### Installing Dependencies

```bash
# Install Python dependencies
pip install -r requirements.txt

# Install FFmpeg (based on your operating system)

# Ubuntu/Debian
sudo apt install ffmpeg

# macOS
brew install ffmpeg

# Windows
# Download from https://ffmpeg.org/download.html and add to system PATH
```

## Installation Steps

1. Clone or download the project files
2. Install Python dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Ensure FFmpeg is installed and accessible from the command line

## Usage

### Method 1: Using Command Line Arguments

Change the code at the end of the main.py file to:

```python
if __name__ == "__main__":
    main()
```

```bash
# Basic usage
python main.py <video_file_path>

# Specify frame rate and width
python main.py <video_file_path> --fps 30 --width 100

# Example
python main.py "my_video.mp4" --fps 24 --width 120
```

### Method 2: Direct Code Modification

Modify the following parameters at the bottom of the `main.py` file:

```python
if __name__ == "__main__":
    video_path = r"your_video_file_path"
    play_video_in_ascii(video_path, 30, 2000)  # 30 FPS, max width 2000
```

Then run `python main.py` to play the video in the terminal.

## Command Line Arguments

| Argument     | Description                  | Default |
| ------------ | ---------------------------- | ------- |
| `video_path` | Video file path (required)   | -       |
| `--fps`      | Playback frame rate          | 15      |
| `--width`    | Maximum width of ASCII image | 80      |

## How It Works

1. **Video Processing**: Uses FFmpeg to extract video frames, converts to grayscale, and resizes
2. **ASCII Conversion**: Maps grayscale pixel values to a set of ASCII characters (dark to bright: @#\*+=-:.)
3. **Terminal Rendering**: Clears the terminal and displays the ASCII representation of the current frame
4. **Frame Rate Control**: Controls playback speed by adjusting read and processing speed

## Performance Optimizations

- Uses precomputed character mapping table for faster conversion
- Uses faster image scaling algorithm (fast_bilinear)
- Directly processes grayscale images to avoid color conversion overhead
- Pre-allocates buffers to reduce memory allocation

## Troubleshooting

### Common Issues

1. **"Error: FFmpeg not found"**

   - Ensure FFmpeg is correctly installed and added to the system PATH

2. **ASCII image distorted or incorrect size**

   - Adjust the `--width` parameter or terminal size
   - Ensure the terminal supports ANSI escape codes

3. **Playback too slow**
   - Lower the `--fps` parameter value
   - Reduce the `--width` parameter value

### Exiting the Program

- Press `Ctrl+C` to stop playback

## Custom ASCII Character Set

In the `convert_frame_to_ascii_fast` function in `main.py`, you can modify the `ascii_chars` variable to customize the character set:

```python
# Default character set (dark to bright)
ascii_chars = "@#*+=-:."

# Inverted character set (bright to dark)
# ascii_chars = " .:-=+*#@"

# More detailed character set
# ascii_chars = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "
```

## Notes

- Playback effect depends on terminal size and font size
- High-resolution videos may require more processing time
- Some terminals may not support ANSI escape codes, causing display issues
- Ensure the terminal has sufficient height to display the complete ASCII frame

## License

[CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/)

This project is open source and intended for learning and research purposes only.

---

**Pro tip**: For best results, use a modern terminal that supports ANSI escape codes and adjust the terminal window size to match the video aspect ratio.
