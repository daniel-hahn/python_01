'''
this is just a very small test to draw a random plot on a desktop window
'''

import sys
import random
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

# inherit from QMainWindow
class MyProgram(QMainWindow):

    def __init__(self):
        #call super constructor
        super().__init__()
        # position on screen
        self.left = 20
        self.top = 20
        # title bar
        self.title = 'my gui program'
        # dimensions
        self.width = 1000
        self.height = 400
        # start gui
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # create canvas
        canvas = ShowCanvas(self)
        # put canvas in top left corner
        canvas.move(0,0)
        # create btn
        button = QPushButton('button', self)
        button.setToolTip('example button')
        button.move(500,0)
        button.resize(100,400)

        self.show()

# inherit from FigureCanvas
class ShowCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        #create figure
        figure = Figure(figsize=(width, height), dpi=dpi)

        # pass figure to parent class
        FigureCanvas.__init__(self, figure)
        self.setParent(parent)

        # plot canvas
        self.plot()

    def plot(self):
        # create 40 random numbers from 0-1
        data = [random.random() for i in range(40)]
        # print(data)
        # set axis
        ax = self.figure.add_subplot(111)
        ax.plot(data, 'r-')
        ax.set_title('random graph')

        # draw graph
        self.draw()

if __name__ == '__main__':
    # call c++ constructor of QApplication
    app = QApplication(sys.argv)
    # start program
    pr = MyProgram()
    # starts the event-loop and blocks until the application quits
    sys.exit(app.exec_())