# Terminal System Monitor

A colourful terminal-based system monitor built with Python and [Rich](https://github.com/Textualize/rich).  
Displays live CPU, GPU, and memory usage along with disk partition details and temperature monitoring.

## Requirements

- Python 3.7+
- `rich`, `psutil`, `GPUtil`, and `setuptools` Python libraries
- NVIDIA GPU drivers (for GPU monitoring)

## Installation

```bash
pip install rich psutil GPUtil setuptools
```

## Usage

```bash
python system_monitor.py
```

Press `Ctrl+C` to exit the program.

## Features

- **CPU Monitor**: Shows CPU usage percentage and temperature
- **GPU Monitor**: Shows GPU usage percentage and temperature (NVIDIA GPUs)
- **Memory Monitor**: Shows memory usage percentage and used/total memory
- **Disk Partitions**: Displays detailed disk usage information
