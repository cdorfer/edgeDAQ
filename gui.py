from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QSlider
from PyQt5.Qt import QLabel, QGridLayout, Qt, QDoubleSpinBox,QLCDNumber


class Window(QWidget):
    
    
    def __init__(self, positionControl, scanControl):
        super().__init__()       
        self.initUI()
        self.posContr = positionControl
        self.scanContr = scanControl
        
        
    def initUI(self):
        self.setWindowTitle('edgeDAQ')
        self.setMinimumWidth(500)
        #self.setMinimumHeight(600)
        
        ############################ scan control ##############################
        self.posCtrLayout = QGridLayout()
        self.posCtrLayout.setContentsMargins(4, 4, 4, 4)
        self.posCtrLayout.setSpacing(2)
        self.posCtrLayout.setObjectName("posCtrLayout")  
        
        self.xLabel = QLabel('X: ')
        self.yLabel = QLabel('Y: ')
        self.zLabel = QLabel('Z: ')   
        
        self.xSlider = QSlider()
        self.xSlider.setOrientation(Qt.Horizontal)
        self.xSlider.setMinimumWidth(200)   
        self.ySlider = QSlider()
        self.ySlider.setOrientation(Qt.Horizontal)
        self.ySlider.setMinimumWidth(200)
        self.zSlider = QSlider()
        self.zSlider.setOrientation(Qt.Horizontal)
        self.zSlider.setMinimumWidth(200)
        
        self.xSpinBox = QDoubleSpinBox()
        self.ySpinBox = QDoubleSpinBox()
        self.zSpinBox = QDoubleSpinBox()
        
        self.posCtrLayout.addWidget(self.xLabel, 1,1,1,1, Qt.AlignCenter)
        self.posCtrLayout.addWidget(self.xSlider, 1,2,1,3, Qt.AlignLeft)
        self.posCtrLayout.addWidget(self.xSpinBox, 1,4,1,1, Qt.AlignCenter)
        
        self.posCtrLayout.addWidget(self.yLabel, 2,1,1,1,Qt.AlignCenter)
        self.posCtrLayout.addWidget(self.ySlider, 2,2,1,3,Qt.AlignLeft)
        self.posCtrLayout.addWidget(self.ySpinBox, 2,4,1,1,Qt.AlignCenter)

        self.posCtrLayout.addWidget(self.zLabel, 3,1,1,1,Qt.AlignCenter)
        self.posCtrLayout.addWidget(self.zSlider, 3,2,1,3,Qt.AlignLeft)
        self.posCtrLayout.addWidget(self.zSpinBox, 3,4,1,1,Qt.AlignCenter)
        
        #----------------------------------------------------------------------
        
        self.xLimLowLabel = QLabel('X<sub>LimLow</sub>: ')
        self.xlimlow = QLCDNumber()
        self.xlimlow.setMinimumWidth(100)
        self.xLimHighLabel = QLabel('X<sub>LimHigh</sub>: ')
        self.xlimhigh = QLCDNumber()
        self.xlimhigh.setMinimumWidth(100)
      
        self.yLimLowLabel = QLabel('Y<sub>LimLow</sub>: ')
        self.ylimlow = QLCDNumber()
        self.ylimlow.setMinimumWidth(100)
        self.yLimHighLabel = QLabel('Y<sub>LimHigh</sub>: ')
        self.ylimhigh = QLCDNumber()
        self.ylimhigh.setMinimumWidth(100)
        
        self.zLimLowLabel = QLabel('Z<sub>LimLow</sub>: ')
        self.zlimlow = QLCDNumber()
        self.zlimlow.setMinimumWidth(100)
        self.zLimHighLabel = QLabel('Z<sub>LimHigh</sub>: ')
        self.zlimhigh = QLCDNumber()
        self.zlimhigh.setMinimumWidth(100)
        
        self.posCtrLayout.addWidget(self.xLimLowLabel, 4,1,1,1,Qt.AlignCenter)
        self.posCtrLayout.addWidget(self.xlimlow, 4,2,1,1,Qt.AlignLeft)
        self.posCtrLayout.addWidget(self.xLimHighLabel, 4,3,1,1,Qt.AlignCenter)
        self.posCtrLayout.addWidget(self.xlimhigh, 4,4,1,1,Qt.AlignLeft)
        
        self.posCtrLayout.addWidget(self.yLimLowLabel, 5,1,1,1,Qt.AlignCenter)
        self.posCtrLayout.addWidget(self.ylimlow, 5,2,1,1,Qt.AlignLeft)
        self.posCtrLayout.addWidget(self.yLimHighLabel, 5,3,1,1,Qt.AlignCenter)
        self.posCtrLayout.addWidget(self.ylimhigh, 5,4,1,1,Qt.AlignLeft)

        self.posCtrLayout.addWidget(self.zLimLowLabel, 6,1,1,1,Qt.AlignCenter)
        self.posCtrLayout.addWidget(self.zlimlow, 6,2,1,1,Qt.AlignLeft)
        self.posCtrLayout.addWidget(self.zLimHighLabel, 6,3,1,1,Qt.AlignCenter)
        self.posCtrLayout.addWidget(self.zlimhigh, 6,4,1,1,Qt.AlignLeft)

        #----------------------------------------------------------------------
        
        self.goHome = QPushButton()
        self.goHome.setText('Go Home')
        self.button.clicked.connect()
        #self.goHome.setMinimumWidth(40)
        
        self.defHome = QPushButton()
        self.defHome.setText('Define Home')
        #self.defHome.setMinimumWidth(200)
        
        self.defHWLim = QPushButton()
        self.defHWLim.setText('Find HW Limits')
        #self.defHWLim.setMinimumWidth(60)
        
        self.posCtrLayout.addWidget(self.goHome, 8,1,1,1,Qt.AlignCenter)
        self.posCtrLayout.addWidget(self.defHome, 8,2,1,1,Qt.AlignCenter)
        self.posCtrLayout.addWidget(self.defHWLim, 8,4,1,1,Qt.AlignCenter)
        
        #----------------------------------------------------------------------
        
        self.posWin = QHBoxLayout()
        self.posWin.addLayout(self.posCtrLayout)
        
        
        
        #self.logWin = QHBoxLayout()
        
        
        
        self.mainLayout = QVBoxLayout()
        self.mainLayout.addLayout(self.posWin)
        self.setLayout(self.mainLayout)
        
        
        
        
        
        
        
                
        self.show()