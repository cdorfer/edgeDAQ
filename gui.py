from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QSlider,\
    QCheckBox
from PyQt5.Qt import QLabel, QGridLayout, Qt, QDoubleSpinBox,QLCDNumber
from time import sleep


class Window(QWidget):
    
    
    def __init__(self, posC, scanC):
        super().__init__()   
        
        #defaults position control
        self.xStepSize = 500 #um
        self.yStepSize = 50
        self.zStepSize = 1000
            
        
        self.initUI(posC, scanC)

      
        
    def initUI(self, posC, scanC):
        self.positionControl = posC
        self.scanControl = scanC

        self.setWindowTitle('edgeDAQ')
        self.setMinimumWidth(500)
        #self.setMinimumHeight(600)
        
        ############################ position control ##############################
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
        self.xSlider.setPageStep(self.xStepSize*1000) #1000 to display um not nm
        self.xSlider.setMinimumWidth(220)   
          
        self.ySlider = QSlider()
        self.ySlider.setOrientation(Qt.Horizontal)   
        self.ySlider.setValue(self.positionControl.getYPosition()*(10**6)) #to nm
        self.ySlider.setTickInterval(1)
        self.ySlider.setMaximum(self.positionControl.getYMax()*(10**6)) #to nm
        self.ySlider.setMinimum(self.positionControl.getYMin()*(10**6)) #to nm
        self.ySlider.valueChanged.connect(self.sliderYChange)
        self.ySlider.setPageStep(self.yStepSize*1000) #1000 to display um not nm
        self.ySlider.setMinimumWidth(220)
        
        self.zSlider = QSlider()
        self.zSlider.setOrientation(Qt.Horizontal)
        self.zSlider.setValue(self.positionControl.getZPosition()*(10**6)) #to nm
        self.zSlider.setTickInterval(1)
        self.zSlider.setMaximum(self.positionControl.getZMax()*(10**6)) #to nm
        self.zSlider.setMinimum(self.positionControl.getZMin()*(10**6)) #to nm
        self.zSlider.valueChanged.connect(self.sliderZChange)
        self.zSlider.setPageStep(self.zStepSize*1000) #1000 to display um not nm
        self.zSlider.setMinimumWidth(220)
    
    
        self.xSpinBox = QDoubleSpinBox()
        self.xSpinBox.setMaximum(10000)
        self.xSpinBox.setMinimum(0.0001)
        self.xSpinBox.setAlignment(Qt.AlignRight)
        self.xSpinBox.setValue(self.xStepSize)
        self.xSpinBox.valueChanged.connect(self.xSpinBoxChange)
             
        self.ySpinBox = QDoubleSpinBox()
        self.ySpinBox.setMaximum(10000)
        self.ySpinBox.setMinimum(0.0001)
        self.ySpinBox.setAlignment(Qt.AlignRight)
        self.ySpinBox.setValue(self.yStepSize)
        self.ySpinBox.valueChanged.connect(self.ySpinBoxChange)
          
        self.zSpinBox = QDoubleSpinBox()
        self.zSpinBox.setMaximum(10000)
        self.zSpinBox.setMinimum(0.0001)
        self.zSpinBox.setAlignment(Qt.AlignRight)
        self.zSpinBox.setValue(self.zStepSize)
        self.zSpinBox.valueChanged.connect(self.zSpinBoxChange)
        

        self.posCtrLayout.addWidget(QLabel("<h2>Position Control</h2>"), 1,1,1,4,Qt.AlignCenter)

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
        self.xCurr.setMinimumHeight(25)
        self.xCurr.setDigitCount(7)
        self.showXPos()
 
        self.yCurrLabel = QLabel('Y<sub>Pos</sub>: ')
        self.yCurr = QLCDNumber()
        self.yCurr.setDigitCount(6)
        self.yCurr.setMinimumWidth(100)
        self.yCurr.setMinimumHeight(25)
        self.yCurr.setDigitCount(7)
        self.showYPos()
        
        self.zCurrLabel = QLabel('Z<sub>Pos</sub>: ')
        self.zCurr = QLCDNumber()
        self.zCurr.setDigitCount(7)
        self.zCurr.setMinimumWidth(100)
        self.zCurr.setMinimumHeight(25)
        self.zCurr.setDigitCount(7)
        self.showZPos()

        
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
        self.defHome.clicked.connect(self.defHomeSlot)
        #self.defHome.setMinimumWidth(200)
        
        self.defHWLim = QPushButton()
        self.defHWLim.setText('Find HW Limits')
        self.defHWLim.clicked.connect(self.positionControl.findHardwareLimits)
        #self.defHWLim.setMinimumWidth(60)
        
        self.posCtrLayout.addWidget(self.goHome, 10,1,1,1,Qt.AlignCenter)
        self.posCtrLayout.addWidget(self.defHome, 10,2,1,1,Qt.AlignCenter)
        self.posCtrLayout.addWidget(self.defHWLim, 10,4,1,1,Qt.AlignCenter)
        self.posCtrLayout.addWidget(QLabel(""), 11,1,1,4,Qt.AlignCenter)
        
        #----------------------------------------------------------------------
        
        self.posWin = QHBoxLayout()
        self.posWin.addLayout(self.posCtrLayout)
        
        ############################ end position control ##############################
        
        ############################ start scan control ##############################
        
        self.scanCtrLayout = QGridLayout()
        self.scanCtrLayout.setContentsMargins(4, 4, 4, 4)
        self.scanCtrLayout.setSpacing(2)
        self.scanCtrLayout.setObjectName("scanCtrLayout") 
            
        self.xlimlow = QDoubleSpinBox()
        self.xlimlow.setMaximum(100)
        self.xlimlow.setMinimum(-100)
        self.xlimlow.setAlignment(Qt.AlignRight)
        self.xlimlow.setDecimals(3)
        self.xlimlow.setMinimumWidth(90)
        self.xlimlow.setValue(0)
        self.xlimlow.valueChanged.connect(self.xLimLowChange)
        self.xLimLowChange()
        
        self.xlimhigh = QDoubleSpinBox()
        self.xlimhigh.setMaximum(100)
        self.xlimhigh.setMinimum(-100)
        self.xlimhigh.setAlignment(Qt.AlignRight)
        self.xlimhigh.setDecimals(3)
        self.xlimhigh.setMinimumWidth(90)
        self.xlimhigh.setValue(0)
        self.xlimhigh.valueChanged.connect(self.xLimHighChange) 
        self.xLimHighChange()
        
        self.xstep = QDoubleSpinBox()
        self.xstep.setMaximum(20)
        self.xstep.setMinimum(-20)
        self.xstep.setAlignment(Qt.AlignRight)
        self.xstep.setDecimals(3)
        self.xstep.setMinimumWidth(90)
        self.xstep.setValue(1)
        self.xstep.valueChanged.connect(self.xStepChange)
        self.xStepChange()
        
        self.xactive = QCheckBox('onX')
        self.xactive.setChecked(True)
        self.xactive.stateChanged.connect(lambda:self.btnstate(self.xactive))
          

        self.ylimlow = QDoubleSpinBox()
        self.ylimlow.setMaximum(5)
        self.ylimlow.setMinimum(-5)
        self.ylimlow.setAlignment(Qt.AlignRight)
        self.ylimlow.setDecimals(3)
        self.ylimlow.setMinimumWidth(90)
        self.ylimlow.setValue(0)
        self.ylimlow.valueChanged.connect(self.yLimLowChange)
        self.yLimLowChange()
        
        self.ylimhigh = QDoubleSpinBox()
        self.ylimhigh.setMaximum(5)
        self.ylimhigh.setMinimum(-5)
        self.ylimhigh.setAlignment(Qt.AlignRight)
        self.ylimhigh.setDecimals(3)
        self.ylimhigh.setMinimumWidth(90)
        self.ylimhigh.setValue(0)
        self.ylimhigh.valueChanged.connect(self.yLimHighChange) 
        self.yLimHighChange()
        
        self.ystep = QDoubleSpinBox()
        self.ystep.setMaximum(1)
        self.ystep.setMinimum(-1)
        self.ystep.setAlignment(Qt.AlignRight)
        self.ystep.setDecimals(3)
        self.ystep.setMinimumWidth(90)
        self.ystep.setValue(1)
        self.ystep.valueChanged.connect(self.yStepChange)   
        self.yStepChange()
        
        self.yactive = QCheckBox('onY')
        self.yactive.setChecked(True)
        self.yactive.stateChanged.connect(lambda:self.btnstate(self.yactive))
       
         
        self.zlimlow = QDoubleSpinBox()
        self.zlimlow.setMaximum(150)
        self.zlimlow.setMinimum(-150)
        self.zlimlow.setAlignment(Qt.AlignRight)
        self.zlimlow.setDecimals(3)
        self.zlimlow.setMinimumWidth(90)
        self.zlimlow.setValue(0)
        self.zlimlow.valueChanged.connect(self.zLimLowChange)
        self.zLimLowChange()
        
        self.zlimhigh = QDoubleSpinBox()
        self.zlimhigh.setMaximum(150)
        self.zlimhigh.setMinimum(-150)
        self.zlimhigh.setAlignment(Qt.AlignRight)
        self.zlimhigh.setDecimals(3)
        self.zlimhigh.setMinimumWidth(90)
        self.zlimhigh.setValue(0)
        self.zlimhigh.valueChanged.connect(self.zLimHighChange)
        self.zLimLowChange() 
        
        self.zstep = QDoubleSpinBox()
        self.zstep.setMaximum(20)
        self.zstep.setMinimum(-20)
        self.zstep.setAlignment(Qt.AlignRight)
        self.zstep.setDecimals(3)
        self.zstep.setMinimumWidth(90)
        self.zstep.setValue(1)
        self.zstep.valueChanged.connect(self.zStepChange) 
        self.zStepChange()
        
        self.zactive = QCheckBox('onZ')
        self.zactive.setChecked(True)
        self.zactive.stateChanged.connect(lambda:self.btnstate(self.zactive))
     
     
        
        self.scanCtrLayout.addWidget(QLabel("<h2>Scan Control</h2>"), 1,1,1,7,Qt.AlignCenter)   
        self.scanCtrLayout.addWidget(QLabel(""), 2,1,1,4,Qt.AlignCenter)
               
        self.scanCtrLayout.addWidget(QLabel('X<sub>min</sub>'), 3,1,1,1,Qt.AlignCenter)
        self.scanCtrLayout.addWidget(self.xlimlow, 3,2,1,1,Qt.AlignLeft)
        self.scanCtrLayout.addWidget(QLabel('X<sub>max</sub>'), 3,3,1,1,Qt.AlignCenter)
        self.scanCtrLayout.addWidget(self.xlimhigh, 3,4,1,1,Qt.AlignLeft)
        self.scanCtrLayout.addWidget(QLabel('X<sub>step</sub>'), 3,5,1,1,Qt.AlignCenter)
        self.scanCtrLayout.addWidget(self.xstep, 3,6,1,1,Qt.AlignLeft)
        self.scanCtrLayout.addWidget(self.xactive, 3,7,1,1,Qt.AlignCenter)
        
        self.scanCtrLayout.addWidget(QLabel('Y<sub>min</sub>'), 4,1,1,1,Qt.AlignCenter)
        self.scanCtrLayout.addWidget(self.ylimlow, 4,2,1,1,Qt.AlignLeft)
        self.scanCtrLayout.addWidget(QLabel('Y<sub>max</sub>'), 4,3,1,1,Qt.AlignCenter)
        self.scanCtrLayout.addWidget(self.ylimhigh, 4,4,1,1,Qt.AlignLeft)
        self.scanCtrLayout.addWidget(QLabel('Y<sub>step</sub>'), 4,5,1,1,Qt.AlignCenter)
        self.scanCtrLayout.addWidget(self.ystep, 4,6,1,1,Qt.AlignLeft)
        self.scanCtrLayout.addWidget(self.yactive, 4,7,1,1,Qt.AlignCenter)

        self.scanCtrLayout.addWidget(QLabel('Z<sub>min</sub>'), 5,1,1,1,Qt.AlignCenter)
        self.scanCtrLayout.addWidget(self.zlimlow, 5,2,1,1,Qt.AlignLeft)
        self.scanCtrLayout.addWidget(QLabel('Z<sub>max</sub>'), 5,3,1,1,Qt.AlignCenter)
        self.scanCtrLayout.addWidget(self.zlimhigh, 5,4,1,1,Qt.AlignLeft)
        self.scanCtrLayout.addWidget(QLabel('Z<sub>step</sub>'), 5,5,1,1,Qt.AlignCenter)
        self.scanCtrLayout.addWidget(self.zstep, 5,6,1,1,Qt.AlignLeft)
        self.scanCtrLayout.addWidget(self.zactive, 5,7,1,1,Qt.AlignCenter)
        
        
        self.startScan = QPushButton()
        self.startScan.setText('Start Scan')
        self.startScan.clicked.connect(self.startScanSlot)
        
        self.stopScan = QPushButton()
        self.stopScan.setText('Stop Scan')
        self.stopScan.clicked.connect(self.stopScanSlot)  
        
        self.scanCtrLayout.addWidget(self.startScan, 6,1,1,1,Qt.AlignCenter)
        self.scanCtrLayout.addWidget(self.stopScan, 6,2,1,1,Qt.AlignCenter)     
        
  
 
        self.scanWin = QHBoxLayout()
        self.scanWin.addLayout(self.scanCtrLayout)

   
        self.mainLayout = QVBoxLayout()
        self.mainLayout.addLayout(self.posWin)
        self.mainLayout.addLayout(self.scanWin)
        self.setLayout(self.mainLayout)
        
        self.show()
    
    
    def sliderXChange(self):
        self.positionControl.moveAbsoluteX(1.0*self.xSlider.value()/(10**6))
        self.showXPos()
     
    def sliderYChange(self):
        self.positionControl.moveAbsoluteY(1.0*self.ySlider.value()/(10**6))
        self.showYPos()   
        
    def sliderZChange(self):
        self.positionControl.moveAbsoluteZ(1.0*self.zSlider.value()/(10**6))
        self.showZPos()    
        
        
    def xSpinBoxChange(self):
        self.xStepSize = self.xSpinBox.value() 
        self.xSlider.setPageStep(self.xStepSize*1000)
        
    def ySpinBoxChange(self):
        self.yStepSize = self.ySpinBox.value() 
        self.ySlider.setPageStep(self.yStepSize*1000)    
        
    def zSpinBoxChange(self):
        self.zStepSize = self.zSpinBox.value() 
        self.zSlider.setPageStep(self.zStepSize*1000)
        
    def showXPos(self):
        sleep(0.5)
        self.xCurr.display(self.positionControl.getXPosition())
        
    def showYPos(self):
        sleep(0.5)
        self.yCurr.display(round(self.positionControl.getYPosition(),4))
           
    def showZPos(self):
        sleep(0.5)
        self.zCurr.display(self.positionControl.getZPosition())
        
    def defHomeSlot(self):
        self.positionControl.setHome()
        sleep(1)
        self.showXPos()
        self.showYPos()
        self.showZPos()  
    
            
    def goHomeSlot(self):
        self.positionControl.goHome()
        sleep(2)
        self.showXPos()
        self.showYPos()
        self.showZPos()
        self.xSlider.setValue(self.positionControl.getXPosition())
        self.ySlider.setValue(self.positionControl.getYPosition())
        self.zSlider.setValue(self.positionControl.getZPosition())
        
 
    def xLimLowChange(self):
        self.scanControl.setXmin(self.xlimlow.value())
        
    def xLimHighChange(self):
        self.scanControl.setXmax(self.xlimhigh.value())
        
    def xStepChange(self):
        self.scanControl.setStepX(self.xstep.value())
        
    
    def yLimLowChange(self):
        self.scanControl.setYmin(self.ylimlow.value())
        
    def yLimHighChange(self):
        self.scanControl.setYmax(self.ylimhigh.value())
        
    def yStepChange(self):
        self.scanControl.setStepY(self.ystep.value())
     
        
    def zLimLowChange(self):
        self.scanControl.setZmin(self.zlimlow.value())
        
    def zLimHighChange(self):
        self.scanControl.setZmax(self.zlimhigh.value())
        
    def zStepChange(self):
        self.scanControl.setStepZ(self.zstep.value())
        print('xstep: ', self.zstep.value())
  
    
    def btnstate(self,b):
        if b.text() == 'onX':
            if b.isChecked() == True:
                self.scanControl.setXactive(True)
            else:
                self.scanControl.setXactive(False)

        if b.text() == 'onY':
            if b.isChecked() == True:
                self.scanControl.setYactive(True)
            else:
                self.scanControl.setYactive(False)

        if b.text() == 'onZ':
            if b.isChecked() == True:
                self.scanControl.setZactive(True)
            else:
                self.scanControl.setZactive(False)
    
        
    def startScanSlot(self):
        self.scanControl.startScan()
        
    def stopScanSlot(self):
        self.scanControl.stopScan()
    
    
