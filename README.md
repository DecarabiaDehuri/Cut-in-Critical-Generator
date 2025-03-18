# Cut-in-Critical-Generator
Simple program that puts portrait PNGs into a Cut-in Critical animation, for use mainly on Lex Talionis engine.


## Features
- Real-time preview
- Offset adjustments
- Batch processing

## Installation

### From Source
1. Install [Python 3.8+](https://www.python.org/downloads/)
2. Clone repo:
   ```bash
   git clone https://github.com/yourusername/PortraitApplier.git
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Build Executable
```bash
pyinstaller --onefile --windowed --add-data "Template;Template" src/main.py
```

## Usage
1. Place frame images in `Template/` folder (1.png to 20.png)
2. Run `Cut-in Critical Generator.exe`
3. Select portrait and adjust offsets

## Contributing
Pull requests welcome! For major changes, please open an issue first.

## License
[MIT](LICENSE)
