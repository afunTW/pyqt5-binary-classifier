# pyqt5-binary-classifier

A simple tool for pre-labeling the image and classification

![demo](https://i.imgur.com/LGp29yO.jpg)

## Requirement

Please to install PyQt5 in you platform.

### Ubuntu

```
sudo apt-get install python3-pyqt5
```

## Usage

```
usage: Binary Classifier building with PyQt5 [-h] --img-dir IMGDIR
                                             [--out OUTFILE]

optional arguments:
  -h, --help        show this help message and exit
  --img-dir IMGDIR
  --history HISTORY
  --out OUTFILE
```

## Instruction

- Press 'A' to label false
- Press 'D' to label true
- Press 'U' to undo
- Press 'PageUp' goto previous unlabeled image
- Press 'PageDown' goto next unlabeled image
- Press 'Confirm' button to export label result as csv file