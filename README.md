<div align="left">
  <a href="https://github.com/SantosVilanculos/kudan/actions">
    <img
      src="https://img.shields.io/github/actions/workflow/status/SantosVilanculos/kudan/release.yml"
      alt="build"
    />
  </a>
  <a href="https://github.com/SantosVilanculos/kudan/releases">
    <img alt="release" src="https://img.shields.io/github/v/release/SantosVilanculos/kudan"/>
  </a>
  <a href="https://github.com/SantosVilanculos/kudan/blob/main/LICENSE">
    <img
      src="https://img.shields.io/github/license/SantosVilanculos/kudan"
      alt="license"
    />
  </a>
  <a href="https://github.com/SantosVilanculos/kudan/commits/main">
    <img
      src="https://img.shields.io/github/last-commit/SantosVilanculos/kudan"
      alt="last commit"
    />
  </a>
</div>

![](./screenshot.png)

<p align="justify">
A sleek desktop OS monitor providing real-time insights into CPU, memory, disk, network, sensor data, and system uptime. Utilizing the <a href="https://github.com/giampaolo/psutil">psutil</a> library, it also showcases detailed I/O device information for optimal system performance analysis.
<p/>

---

## Features

### System Information

- Retrieve detailed memory usage statistics;
- Display disk partitions and usage;
- Monitor input/output counters for disk activity.

### Network Monitoring

- View network interface statistics (e.g., sent and received data);
- Display network connections and active states.

### Hardware Information

- Detect and display camera devices (ID, description, position, etc.);
- Show audio and input devices connected;
- Display battery and screen statistics (if supported).

### Process Management

- List all running processes.
- Access Windows service iterators for advanced process details (if on Windows).

### Cross-Platform

- Built to run on multiple operating systems where psutil is supported.

## Installation

```sh
pip install -r requirements.txt
```

## Development

```sh
pymon -p "*.css" -p "*.png" src/main.py
```

## Building a release

```sh
pyinstaller \
  --noconfirm \
  --clean \
  --onefile \
  --name="test" \
  --icon="icon.png" \
  --add-data="icon.png:." \
  --add-data="font:font" \
  --windowed \
  src/main.py
```
