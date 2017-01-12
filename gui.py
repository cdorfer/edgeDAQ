from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QSlider
from PyQt5.Qt import QLabel, QGridLayout, Qt, QDoubleSpinBox,QLCDNumber
from time import sleep


class Window(QWidget):
    
    
    def __init__(self, posC, scanC):
        super().__init__()   
        
        self.xStepSize = 10 #um
        self.yStepSize = 1000
        self.zStepSize = 1000
        
        self.initUI(posC, scanC)

      
        
    def initUI(self, posC, scanC):
        self.positionControl = posC
        self.scanControl = scanC

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
        self.xSlider.setValue(self.positionControl.getXPosition()*(10**6)) #to nm
        self.xSlider.setTickInterval(1)
        self.xSlider.setMaximum(self.positionControl.getXMax()*(10**6)) #to nm
        self.xSlider.setMinimum(self.positionControl.getXMin()*(10**6)) #to nm
        self.xSlider.valueChanged.connect(self.sliderXChange)
        print('min: ', self.positionControl.getXMin()*(10**6), ' max: ', self.positionControl.getXMax()*(10**6), ' current: ', self.positionControl.getXPosition()*(10**6))
        
        self.xSlider.setMinimumWidth(200)   
        self.ySlider = QSlider()
        self.ySlider.setOrientation(Qt.Horizontal)
        self.ySlider.setMinimumWidth(200)
        self.zSlider = QSlider()
        self.zSlider.setOrientation(Qt.Horizontal)
        self.zSlider.setMinimumWidth(200)
        
        self.xSpinBox = QDoubleSpinBox()
        self.xSpinBox.setMaximum(10000)
        self.xSpinBox.setMinimum(0.01)
        self.xSpinBox.setValue(self.xStepSize)
        self.xSpinBox.valueChanged.connect(self.xSpinBoxChange)
        
        
        self.ySpinBox = QDoubleSpinBox()
        self.zSpinBox = QDoubleSpinBox()
        
        self.posCtrLabel = QLabel("Position Control")
        self.posCtrLayout.addWidget(self.posCtrLabel, 1,1,1,4,Qt.AlignCenter)

        self.posCtrLabel = QLabel("Step Size [um]")
        self.posCtrLayout.addWidget(self.posCtrLabel, 3,4,1,1,Qt.AlignCenter)       
        
        self.posCtrLayout.addWidget(self.xLabel, 4,1,1,1, Qt.AlignCenter)
        self.posCtrLayout.addWidget(self.xSlider, 4,2,1,3, Qt.AlignLeft)
        self.posCtrLayout.addWidget(self.xSpinBox, 4,4,1,1, Qt.AlignCenter)
        
        self.posCtrLayout.addWidget(self.yLabel, 5,1,1,1,Qt.AlignCenter)
        self.posCtrLayout.addWidget(self.ySlider, 5,2,1,3,Qt.AlignLeft)
        self.posCtrLayout.addWidget(self.ySpinBox, 5,4,1,1,Qt.AlignCenter)

        self.posCtrLayout.addWidget(self.zLabel, 6,1,1,1,Qt.AlignCenter)
        self.posCtrLayout.addWidget(self.zSlider, 6,2,1,3,Qt.AlignLeft)
        self.posCtrLayout.addWidget(self.zSpinBox, 6,4,1,1,Qt.AlignCenter)
        
        #----------------------------------------------------------------------
        
        self.xCurrLabel = QLabel('X<sub>Pos</sub>: ')
        self.xCurr = QLCDNumber()
        self.xCurr.setDigitCount(7)
        self.xCurr.setMinimumWidth(100)
        self.showXPos()
 
        self.yCurrLabel = QLabel('Y<sub>Pos</sub>: ')
        self.yCurr = QLCDNumber()
        self.yCurr.setMinimumWidth(100)
        
        self.zCurrLabel = QLabel('Z<sub>Pos</sub>: ')
        self.zCurr = QLCDNumber()
        self.zCurr.setMinimumWidth(100)

        
        self.posCtrLayout.addWidget(self.xCurrLabel, 7,1,1,1,Qt.AlignCenter)
        self.posCtrLayout.addWidget(self.xCurr, 7,2,1,1,Qt.AlignLeft)
        
        self.posCtrLayout.addWidget(self.yCurrLabel, 8,1,1,1,Qt.AlignCenter)
        self.posCtrLayout.addWidget(self.yCurr, 8,2,1,1,Qt.AlignLeft)

        self.posCtrLayout.addWidget(self.zCurrLabel, 9,1,1,1,Qt.AlignCenter)
        self.posCtrLayout.addWidget(self.zCurr, 9,2,1,1,Qt.AlignLeft)


        #----------------------------------------------------------------------
        
        self.goHome = QPushButton()
        self.goHome.setText('Go Home')
        self.goHome.clicked.connect(self.goHomeSlot)
        #self.goHome.setMinimumWidth(40)
        
        self.defHome = QPushButton()
        self.defHome.setText('Define Home')
        self.defHome.clicked.connect(self.positionControl.setHome)
        #self.defHome.setMinimumWidth(200)
        
        self.defHWLim = QPushButton()
        self.defHWLim.setText('Find HW Limits')
        self.defHWLim.clicked.connect(self.positionControl.findHardwareLimits)
        #self.defHWLim.setMinimumWidth(60)
        
        self.posCtrLayout.addWidget(self.goHome, 10,1,1,1,Qt.AlignCenter)
        self.posCtrLayout.addWidget(self.defHome, 10,2,1,1,Qt.AlignCenter)
        self.posCtrLayout.addWidget(self.defHWLim, 10,4,1,1,Qt.AlignCenter)
        
        #----------------------------------------------------------------------
        
        self.posWin = QHBoxLayout()
        self.posWin.addLayout(self.posCtrLayout)
        
        
        
        #self.logWin = QHBoxLayout()
        
        
        
        self.mainLayout = QVBoxLayout()
        self.mainLayout.addLayout(self.posWin)
        self.setLayout(self.mainLayout)
        
        
        
        
        
        
        
                
        self.show()
    
    
    def sliderXChange(self):
        print('current table position:', self.positionControl.getXPosition(), 'current slider position: ', self.xSlider.value())
        self.positionControl.moveAbsoluteX((self.xSlider.value()*self.xStepSize))
        self.showXPos()
        
    def xSpinBoxChange(self):
        self.xStepSize = self.xSpinBox.value() #1000 for um to nm
        #currSliderPos = 
        #self.xSlider.blockSignals(True)
        #self.xSlider.setValue(self.xSlider.value()/self.xStepSize)
        #print('set slider value to: ', self.xSlider.value()/self.xStepSize)
        #self.xSlider.blockSignals(False)
        
    def goHomeSlot(self):
        self.positionControl.goHome()
        sleep(2)
        self.showXPos()
        self.xSlider.setValue(self.positionControl.getXPosition())
        
        #self.showYPos()
        #self.showZPos()
        
        
    def showXPos(self):
        sleep(0.5)
        self.xCurr.display(self.positionControl.getXPosition())
        
        
    def priint(self):
        print('testttttt')
