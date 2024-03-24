#создай тут фоторедактор Easy Editor!
from PyQt5.QtWidgets import QApplication, QWidget,QFileDialog, QLabel, QPushButton, QListWidget, QHBoxLayout, QVBoxLayout
import os
from PIL import Image, ImageFilter
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

app = QApplication([])
win = QWidget()

win.resize(700, 500)

win.setWindowTitle('Photoshop')

lb_image = QLabel('Лево')
btn_dir = QPushButton('Папка')
lw_files = QListWidget()

btn_left = QPushButton('Лево')
btn_right = QPushButton('Право')
btn_flip = QPushButton('Зеркало')
btn_sharp = QPushButton('Резкость')
btn_bw = QPushButton('Б/Ч')

row = QHBoxLayout()
row_tools = QHBoxLayout()
col1 = QVBoxLayout()
col2 = QVBoxLayout()
col1.addWidget(btn_dir)
col1.addWidget(lw_files)
col2.addWidget(lb_image, 95)

row_tools.addWidget(btn_left)
row_tools.addWidget(btn_right)
row_tools.addWidget(btn_flip)
row_tools.addWidget(btn_sharp)
row_tools.addWidget(btn_bw)
col2.addLayout(row_tools)
row.addLayout(col1, 20)
row.addLayout(col2, 80)
win.setLayout(row)

workdir = ''
def filter(files, extensions):
    result = []
    for filename in files:
        for ext in extensions:
            if filename.endswith(ext):
                result.append(filename)
    return result

def chooseWorkdir():
    global workdir
    workdir = QFileDialog.getExistingDirectory()

def showFilenamesList():
    extensions = ['.jpg', '.jpeg', '.png','.gif','.bmp']
    chooseWorkdir()
    filenames = filter(os.listdir(workdir), extensions)
    lw_files.clear()
    for filename in filenames:
        lw_files.addItem(filename)
btn_dir.clicked.connect(showFilenamesList)

class ImageProcessor():
    def __init__(self):
        self.image = None
        self.dir = None
        self.filename = None
        self.save_dir = "Modified/"
    def loadImage(self, dir, filename):
        self.dir = dir
        self.filename = filename
        image_path = os.path.join(dir, filename)
        self.image = Image.open(image_path)
    def showImage(self, path):
        lb_image.hide()
        pixmapimage = QPixmap(path)
        w, h = lb_image.width(), lb_image.height()
        pixmapimage = pixmapimage.scaled(w, h, Qt.KeepAspectRatio)
        lb_image.setPixmap(pixmapimage)
        lb_image.show()
    def saveImage(self):
        path = os.path.join(workdir, self.save_dir)
        if not(os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)
        fullname = os.path.join(path, self.filename)
        self.image.save(fullname)
    def do_flip(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.saveImage()
        image_path = os.path.join(
            workdir, self.save_dir, self.filename
        )
        self.showImage(image_path)
    def do_rotate_right(self):
        self.image = self.image.transpose(Image.ROTATE_270)
        self.saveImage()
        image_path = os.path.join(
            workdir, self.save_dir, self.filename
        )
        self.showImage(image_path)
    def do_rotate_left(self):
        self.image = self.image.transpose(Image.ROTATE_90)
        self.saveImage()
        image_path = os.path.join(
            workdir, self.save_dir, self.filename
        )
        self.showImage(image_path)
    def do_L(self):
        self.image = self.image.convert('L')
        self.saveImage()
        image_path = os.path.join(
            workdir, self.save_dir, self.filename
        )
        self.showImage(image_path)
    def do_bl(self):
        self.image = self.image.filter(ImageFilter.BLUR)
        self.saveImage()
        image_path = os.path.join(
            workdir, self.save_dir, self.filename
        )
        self.showImage(image_path)




workimage = ImageProcessor()
def showChosenImage():
    if lw_files.currentRow() >= 0:
        filename = lw_files.currentItem().text()
        workimage.loadImage(workdir, filename)
        image_path = os.path.join(workimage.dir, workimage.filename)
        workimage.showImage(image_path)
lw_files.currentRowChanged.connect(showChosenImage)




btn_flip.clicked.connect(workimage.do_flip)
btn_right.clicked.connect(workimage.do_rotate_right)
btn_left.clicked.connect(workimage.do_rotate_left)
btn_bw.clicked.connect(workimage.do_L)
btn_sharp.clicked.connect(workimage.do_bl)
win.show()
app.exec_()