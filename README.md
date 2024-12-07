<div align="left">
  <a href="https://github.com/SantosVilanculos/configuration/blob/main/LICENSE">
    <img
      src="https://img.shields.io/github/license/SantosVilanculos/configuration"
      alt="license"
    />
  </a>
  <a href="https://github.com/SantosVilanculos/configuration/commits/main">
    <img
      src="https://img.shields.io/github/last-commit/SantosVilanculos/configuration"
      alt="last commit"
    />
  </a>
  <a href="https://github.com/SantosVilanculos/kudan/releases">
  <img alt="release" src="https://img.shields.io/github/v/release/SantosVilanculos/kudan">
  </a>
</div>

![](./screenshot.png)

<p align="justify">
 <strong>Kudan</strong> is a desktop operating system monitoring application that provides real-time insights into system performance, resource management and key metrics, offering a reliable and efficient way to monitor your computer.
 <p/>
 <p align="justify">
    This application makes use of the <a href="https://github.com/giampaolo/psutil">psutil</a> library, a cross-platform library for retrieving information on running processes and system utilization (CPU, memory, disks, network, sensors) and system uptime.
</p>

---

```sh
pip install -r requirements.txt
```

```sh
pyinstaller "./src/main.py" --noconfirm --clean --onefile --name="Kudan" --icon="./favicon.ico" --add-data="./favicon.ico:./" --add-data="./inter:./" --windowed
```
