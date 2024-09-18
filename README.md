<p align="center">
    <img src="./icon.ico" />
</p>

![X (Formerly Twitter)](https://img.shields.io/twitter/follow/quollouq)
![LICENSE](https://img.shields.io/github/license/westernqoul/kudan)

<p align="justify">
 <strong>Kudan</strong> is a desktop operating system monitoring application that provides real-time insights into system performance, resource management and key metrics, offering a reliable and efficient way to monitor your computer.
 <p/>
 <p align="justify">
    This application makes use of the <a href="https://github.com/giampaolo/psutil">psutil</a> library, a cross-platform library for retrieving information on running processes and system utilization (CPU, memory, disks, network, sensors) and system uptime.
</p>

---

```sh
python -m venv "./.venv"
source "./venv/Scripts/activate"
pip install -r requirements.txt
```

```sh
pyinstaller "./src/main.py" --noconfirm --clean --onefile --name="Kudan" --icon="./icon.ico" --add-data="./icon.ico:./" --add-data="./res:./" --windowed
```

![](./screenshot.png)
