<p align="center">
    <img src="./icon.ico" />
</p>

![X (Formerly Twitter)](https://img.shields.io/twitter/url?url=https%3A%2F%2Fx.com%2F%40westernqoul&label=Follow)
![LICENSE](https://img.shields.io/github/license/westernqoul/kudan)

```sh
python -m venv "./.venv"
source "./venv/Scripts/activate"
pip install -r requirements.txt
```

```sh
pyinstaller "./src/main.py" --noconfirm --clean --onefile --name="Kudan" --icon="./icon.ico" --add-data="./icon.ico:./" --add-data="./Inter-Regular.ttf:./" --add-data="./Inter-Medium.ttf:./" --add-data="./Inter-Bold.ttf:./" --add-data="./JetBrainsMono-Regular.ttf:./" --windowed
```

![](./screenshot.png)
