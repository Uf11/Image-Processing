import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QLabel, QFileDialog, QDialog, QLineEdit
from PyQt5.QtGui import QPixmap
from PyQt5 import uic
import matplotlib.pyplot as plt
import numpy as np
import copy
import cv2

option_counter = 0
negative_win_counter = 0
grey_level_win_counter = 0
histogram_spread_win_counter = 0
histogram_shrink_win_counter = 0
intensity_level_win_counter = 0
piecewise_win_counter = 0
power_law_win_counter = 0
file_name = []
image_copy = None
grey_image_copy = None


class Main(QMainWindow):
    def __init__(self):
        super(Main, self).__init__()
        uic.loadUi(".\\ui\\main.ui", self)
        self.Select_Button = self.findChild(QPushButton, "Select_Button")
        self.label = self.findChild(QLabel, "label")
        self.Map_Button = self.findChild(QPushButton, "Map_Button")
        self.Select_Button.clicked.connect(self.file_selector)
        self.Map_Button.clicked.connect(self.map_options)
        self.show()

    def file_selector(self):
        global file_name
        global image_copy
        global grey_image_copy
        file_name = QFileDialog.getOpenFileName(self, "Open File", "c:",
                                                "All Files (*);;Bmp Files (*.bmp);;Jpg Files (*.jpg)")
        if file_name:
            self.pixmap = QPixmap(file_name[0])
            self.label.setPixmap(self.pixmap)
            img = plt.imread(file_name[0])
            if len(img.shape) == 2:
                image_copy = np.zeros((img.shape[0], img.shape[1], 3), dtype=int)
                for i in range(3):
                    image_copy[:, :, i] = copy.deepcopy(img)
                grey_image_copy = image_copy
            else:
                image_copy = copy.deepcopy(img)
                grey_image_copy = copy.deepcopy(image_copy)
                grey_image_copy[:] = grey_image_copy.mean(axis=-1, keepdims=1)
        else:
            image_copy = None
            grey_image_copy = None

    def map_options(self):
        global option_counter
        if option_counter == 0 and image_copy is not None:
            option_counter += 1
            window = Options()
            window.exec_()
            option_counter -= 1


class Options(QDialog):
    def __init__(self):
        super(Options, self).__init__()
        uic.loadUi(".\\ui\\options.ui", self)
        self.Digital_Negative_Button = self.findChild(QPushButton, "Digital_Negative_Button")
        self.Grey_Level_Button = self.findChild(QPushButton, "Grey_Level_Tran_Button")
        self.Histogram_Spread_Button = self.findChild(QPushButton, "Histogram_Stretch_Button")
        self.Histogram_Shrink_Button = self.findChild(QPushButton, "Histogram_Shrink_Button")
        self.Intensity_Level_Tran_Button = self.findChild(QPushButton, "Intensity_Level_Tran_Button")
        self.PieceWise_Tran_Button = self.findChild(QPushButton, "PieceWise_Tran_Button")
        self.Power_Law_Tran_Button = self.findChild(QPushButton, "Power_Law_Tran_Button")
        self.Digital_Negative_Button.clicked.connect(self.Digital_Negative_Fun)
        self.Grey_Level_Button.clicked.connect(self.Grey_Level_Fun)
        self.Histogram_Spread_Button.clicked.connect(self.Histogram_Spread_Fun)
        self.Histogram_Shrink_Button.clicked.connect(self.Histogram_Shrink_Fun)
        self.Intensity_Level_Tran_Button.clicked.connect(self.Intensity_Level_Fun)
        self.PieceWise_Tran_Button.clicked.connect(self.PieceWise_Fun)
        self.Power_Law_Tran_Button.clicked.connect(self.Power_Law_Fun)
        self.show()

    def Digital_Negative_Fun(self):
        global negative_win_counter
        if negative_win_counter == 0:
            negative_win_counter += 1
            neg_img = np.zeros((image_copy.shape[0], image_copy.shape[1], image_copy.shape[2]), dtype=int)
            for i in range(image_copy.shape[2]):
                neg_img[:, :, i] = negative(image_copy[:, :, i])
            plt.imshow(neg_img)
            plt.title('Negative Image', fontweight='bold')
            plt.show()
            negative_win_counter -= 1

    def Grey_Level_Fun(self):
        global grey_level_win_counter
        if grey_level_win_counter == 0:
            grey_level_win_counter += 1
            window = Grey_Level()
            window.exec_()
            grey_level_win_counter -= 1

    def Histogram_Spread_Fun(self):
        global histogram_spread_win_counter
        if histogram_spread_win_counter == 0:
            histogram_spread_win_counter += 1
            window = Histogram_Spread()
            window.exec_()
            histogram_spread_win_counter -= 1

    def Histogram_Shrink_Fun(self):
        global histogram_shrink_win_counter
        if histogram_shrink_win_counter == 0:
            histogram_shrink_win_counter += 1
            window = Histogram_Shrink()
            window.exec_()
            histogram_shrink_win_counter -= 1

    def Intensity_Level_Fun(self):
        global intensity_level_win_counter
        if intensity_level_win_counter == 0:
            intensity_level_win_counter += 1
            window = Intensity_Level()
            window.exec_()
            intensity_level_win_counter -= 1

    def PieceWise_Fun(self):
        global piecewise_win_counter
        if piecewise_win_counter == 0:
            piecewise_win_counter += 1
            window = PieceWise()
            window.exec_()
            piecewise_win_counter -= 1

    def Power_Law_Fun(self):
        global power_law_win_counter
        if power_law_win_counter == 0:
            power_law_win_counter += 1
            window = Power_Law()
            window.exec_()
            power_law_win_counter -= 1


class Grey_Level(QDialog):
    def __init__(self):
        super(Grey_Level, self).__init__()
        uic.loadUi(".\\ui\\grey_level.ui", self)
        self.Grey_Level_Button = self.findChild(QPushButton, "Grey_Level_Tran_Button")
        self.Grey_Level_Button.clicked.connect(self.Grey_Level_Tran)
        self.Grey_Level_A_val_text = self.findChild(QLineEdit, "A_val")
        self.Grey_Level_B_val_text = self.findChild(QLineEdit, "B_val")
        self.Grey_Level_C_val_text = self.findChild(QLineEdit, "C_val")
        self.Grey_Level_D_val_text = self.findChild(QLineEdit, "D_val")
        self.show()

    def Grey_Level_Tran(self):
        a_val = int(self.Grey_Level_A_val_text.text())
        b_val = int(self.Grey_Level_B_val_text.text())
        c_val = int(self.Grey_Level_C_val_text.text())
        d_val = int(self.Grey_Level_D_val_text.text())
        glt_img = np.zeros((grey_image_copy.shape[0], grey_image_copy.shape[1], grey_image_copy.shape[2]), dtype=int)
        for i in range(3):
            glt_img[:, :, i] = grey_level_transformation(grey_image_copy[:, :, i], a_val, b_val, c_val, d_val)
        plt.imshow(glt_img)
        plt.title('Grey Level Transformed Image', fontweight='bold')
        plt.show()


class Histogram_Spread(QDialog):
    def __init__(self):
        super(Histogram_Spread, self).__init__()
        uic.loadUi(".\\ui\\histogram_stretch.ui", self)
        self.Histogram_Spread_Button = self.findChild(QPushButton, "Histogram_Stretch_button")
        self.Histogram_Spread_Button.clicked.connect(self.Histogram_Spread_Tran)
        self.Histogram_Spread_A_Val_Text = self.findChild(QLineEdit, "A_val")
        self.Histogram_Spread_B_Val_Text = self.findChild(QLineEdit, "B_val")
        self.show()

    def Histogram_Spread_Tran(self):
        a = int(self.Histogram_Spread_A_Val_Text.text())
        b = int(self.Histogram_Spread_B_Val_Text.text())
        hsp_img = np.zeros((image_copy.shape[0], image_copy.shape[1], image_copy.shape[2]), dtype=int)
        for i in range(3):
            hsp_img[:, :, i] = histogram_adjustment(image_copy[:, :, i], a, b)
        plt.imshow(hsp_img)
        plt.title('Histogram Stretched Image', fontweight='bold')
        plt.show()


class Histogram_Shrink(QDialog):
    def __init__(self):
        super(Histogram_Shrink, self).__init__()
        uic.loadUi(".\\ui\\histogram_shrink.ui", self)
        self.Histogram_Shrink_Button = self.findChild(QPushButton, "Histogram_Shrink_button")
        self.Histogram_Shrink_Button.clicked.connect(self.Histogram_Shrink_Tran)
        self.Histogram_Shrink_A_Val_Text = self.findChild(QLineEdit, "A_val")
        self.Histogram_Shrink_B_Val_Text = self.findChild(QLineEdit, "B_val")
        self.show()

    def Histogram_Shrink_Tran(self):
        a = int(self.Histogram_Shrink_A_Val_Text.text())
        b = int(self.Histogram_Shrink_B_Val_Text.text())
        hsh_img = np.zeros((image_copy.shape[0], image_copy.shape[1], image_copy.shape[2]), dtype=int)
        for i in range(3):
            hsh_img[:, :, i] = histogram_adjustment(image_copy[:, :, i], a, b)
        plt.imshow(hsh_img)
        plt.title('Histogram Shrinked Image', fontweight='bold')
        plt.show()


class Intensity_Level(QDialog):
    def __init__(self):
        super(Intensity_Level, self).__init__()
        uic.loadUi(".\\ui\\intensity_level_slicing.ui", self)
        self.Intensity_Level_Tran_Button = self.findChild(QPushButton, "Intensity_level_slicing_button")
        self.Intensity_Level_Tran_Button.clicked.connect(self.Intensity_Level_Tran)
        self.Intensity_Level_A_Val_Text = self.findChild(QLineEdit, "A_val")
        self.Intensity_Level_B_Val_Text = self.findChild(QLineEdit, "B_val")
        self.Intensity_Level_D_Val_Text = self.findChild(QLineEdit, "D_val")
        self.show()

    def Intensity_Level_Tran(self):
        ilt_img = np.zeros((grey_image_copy.shape[0], grey_image_copy.shape[1], grey_image_copy.shape[2]), dtype=int)
        a_val = int(self.Intensity_Level_A_Val_Text.text())
        b_val = int(self.Intensity_Level_B_Val_Text.text())
        d_val = int(self.Intensity_Level_D_Val_Text.text())
        for i in range(3):
            ilt_img[:, :, i] = intensity_level_slicing(grey_image_copy[:, :, i], a_val, b_val, d_val)
        plt.imshow(ilt_img)
        plt.title('Intensity Level Slicied Image', fontweight='bold')
        plt.show()


class PieceWise(QDialog):
    def __init__(self):
        super(PieceWise, self).__init__()
        uic.loadUi(".\\ui\\piecewise.ui", self)
        self.PieceWise_Tran_Button = self.findChild(QPushButton, "PiecewiseTran_Button")
        self.PieceWise_Tran_Button.clicked.connect(self.PieceWise_Tran)
        self.PieceWise_show_Button = self.findChild(QPushButton, "show_result")
        self.PieceWise_show_Button.clicked.connect(self.show_piece_result)
        self.piecewise_A1_Val_Text = self.findChild(QLineEdit, "A1_val")
        self.piecewise_B1_Val_Text = self.findChild(QLineEdit, "B1_val")
        self.piecewise_C1_Val_Text = self.findChild(QLineEdit, "C1_val")
        self.piecewise_D1_Val_Text = self.findChild(QLineEdit, "D1_val")
        self.piecewise_image = np.zeros((grey_image_copy.shape[0], grey_image_copy.shape[1], grey_image_copy.shape[2]),
                                        dtype=int)
        self.pieces = []
        self.show_window = 1
        self.show()

    def PieceWise_Tran(self):
        a1 = int(self.piecewise_A1_Val_Text.text())
        b1 = int(self.piecewise_B1_Val_Text.text())
        c1 = int(self.piecewise_C1_Val_Text.text())
        d1 = int(self.piecewise_D1_Val_Text.text())
        pwt_img1 = np.zeros((grey_image_copy.shape[0], grey_image_copy.shape[1], grey_image_copy.shape[2]), dtype=int)
        for i in range(3):
            pwt_img1[:, :, i] = grey_level_transformation(grey_image_copy[:, :, i], a1, b1, c1, d1, 0)
        self.pieces.append(pwt_img1)
        self.show_window = 0
        plt.imshow(pwt_img1)
        plt.title('Piece Image', fontweight='bold')
        plt.show()

    def show_piece_result(self):
        if self.show_window == 0:
            self.show_window = 1
            self.piecewise_image = self.pieces.pop()
            while self.pieces:
                self.piecewise_image = cv2.bitwise_or(self.piecewise_image, self.pieces.pop())
            self.pieces.append(self.piecewise_image)
            plt.imshow(self.piecewise_image)
            plt.title('Piecewise Image', fontweight='bold')
            plt.show()
            self.show_window = 0


class Power_Law(QDialog):
    def __init__(self):
        super(Power_Law, self).__init__()
        uic.loadUi(".\\ui\\power_law.ui", self)
        self.Power_Law_Tran_Button = self.findChild(QPushButton, "Power_Law_Tran_Button")
        self.Power_Law_Tran_Button.clicked.connect(self.Power_Law_Tran)
        self.gamma_val_text = self.findChild(QLineEdit, "Gamma_val")
        self.show()

    def Power_Law_Tran(self):
        gamma_val = float(self.gamma_val_text.text())
        plt_img = np.zeros((image_copy.shape[0], image_copy.shape[1], image_copy.shape[2]), dtype=int)
        for i in range(3):
            plt_img[:, :, i] = gamma_transformation(image_copy[:, :, i], gamma_val)
        plt.imshow(plt_img)
        plt.title('Gamma Transformed Image', fontweight='bold')
        plt.show()


# change from :a to b to: c to d
def grey_level_transformation(image, a, b, c, d, e=-1):
    temp_image = copy.deepcopy(image)
    slope = (d - c) / (b - a)
    z = d - slope * b
    r, c = image.shape
    for i in range(r):
        for j in range(c):
            if a <= image[i, j] <= b:
                temp_image[i, j] = slope * image[i, j] + z
            else:
                if e != -1:
                    temp_image[i, j] = 0
    return temp_image


# change from :a to b to: c and if required other to d
def intensity_level_slicing(image, a, b, d=-1):
    temp_image = copy.deepcopy(image)
    r, c = image.shape
    for i in range(r):
        for j in range(c):
            if a <= image[i, j] <= b:
                temp_image[i, j] = 255
            elif d != -1:
                temp_image[i, j] = d
    return temp_image


# gamma = c for power law, gamma = 1/c for gamma correction
def gamma_transformation(image, c=1.0):
    temp_image = np.array(255 * (image / 255) ** c, dtype='uint8')
    return temp_image


# m(c,r) = i.max - i(c,r)
def negative(image):
    max_val = image.max()
    temp_image = np.array(max_val - image, dtype='uint8')
    return temp_image


# change range of pixel values from image.min to min_val and image.max max_val
def histogram_adjustment(image, min_val, max_val):
    temp_max = image.max()
    temp_min = image.min()
    temp_image = np.array(((image - temp_min) / (temp_max - temp_min)) * (max_val - min_val) + min_val, dtype='uint8')
    return temp_image


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = Main()
    app.exec_()