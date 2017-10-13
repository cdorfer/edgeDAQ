####################################               
# Author: Christian Dorfer
# Email: cdorfer@phys.ethz.ch                                  
####################################

from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QSlider, QCheckBox, QComboBox, QSpinBox, QTextEdit, QProgressBar
from PyQt5.Qt import QLabel, QGridLayout, Qt, QDoubleSpinBox, QLCDNumber
from time import sleep
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import threading

class Window(QWidget):
    
    
    def __init__(self, posC, acqC, dh, mon):
        super().__init__()   
        
        #defaults for position control
        self.xStepSize = posC.xStepSize
        self.yStepSize = posC.yStepSize
        self.zStepSize = posC.zStepSize
        
        #defaults for scan control
        self.xScanMin = acqC.xScanMin
        self.xScanMax = acqC.xScanMax
        self.xScanStep = acqC.xScanStep
        self.yScanMin = acqC.yScanMin
        self.yScanMax = acqC.yScanMax
        self.yScanStep = acqC.yScanStep
        self.zScanMin = acqC.zScanMin
        self.zScanMax = acqC.zScanMax
        self.zScanStep = acqC.zScanStep
        
        self.tekconfigured = False
        self.fileOpen = False

        self.acqControl = acqC
        self.positionControl = posC
        self.datahandler = dh
        self.livemon = mon
        self.livemon.setStepSize([self.xScanStep, self.yScanStep, self.zScanStep])
        self.livemon.setPlotLimits([self.xScanMin, self.xScanMax, self.yScanMin, self.yScanMax, self.zScanMin, self.zScanMax])
        
        #thread for the scan loop
        self.pill2kill = threading.Event()
        self.scanThread = threading.Thread(target=self.acqControl.startScan, args=(self.pill2kill, 'test'))
        
        self.initUI()


    def initUI(self):
        self.setWindowTitle('edgeDAQ')
        #self.setMinimumWidth(600)
        #self.setMaximumHeight(780)
        
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
        self.xSlider.setMinimumWidth(220)  
        self.xSlider.setTickInterval(1)
        self.xSlider.setPageStep(self.xStepSize*1000) #1000 to display um not nm        
        self.xSlider.setMaximum(self.positionControl.getXMax()*(10**6)) #to nm
        self.xSlider.setMinimum(self.positionControl.getXMin()*(10**6)) #to nm
        self.xSlider.setValue(self.positionControl.getXPosition()*(10**6)) #to nm
        self.xSlider.valueChanged.connect(self.sliderXChange)

        self.ySlider = QSlider()
        self.ySlider.setOrientation(Qt.Horizontal)  
        self.ySlider.setMinimumWidth(220)
        self.ySlider.setTickInterval(1)
        self.ySlider.setPageStep(self.yStepSize*1000) #1000 to display um not nm
        self.ySlider.setMaximum(self.positionControl.getYMax()*(10**6)) #to nm
        self.ySlider.setMinimum(self.positionControl.getYMin()*(10**6)) #to nm
        self.ySlider.setValue(self.positionControl.getYPosition()*(10**6)) #to nm
        self.ySlider.valueChanged.connect(self.sliderYChange)

        self.zSlider = QSlider()
        self.zSlider.setOrientation(Qt.Horizontal)
        self.zSlider.setMinimumWidth(220)
        self.zSlider.setTickInterval(1)
        self.zSlider.setPageStep(self.zStepSize*1000) #1000 to display um not nm
        self.zSlider.setMaximum(self.positionControl.getZMax()*(10**6)) #to nm
        self.zSlider.setMinimum(self.positionControl.getZMin()*(10**6)) #to nm
        self.zSlider.setValue(self.positionControl.getZPosition()*(10**6)) #to nm
        self.zSlider.valueChanged.connect(self.sliderZChange)
    
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
        self.defHome.setEnabled(True) #fixme, limits are screwed up after this.
        #self.defHome.setMinimumWidth(200)
        
        self.defHWLim = QPushButton()
        self.defHWLim.setText('Find HW Limits')
        self.defHWLim.setEnabled(False) #fixme
        self.defHWLim.clicked.connect(self.positionControl.findHardwareLimits)
        #self.defHWLim.setMinimumWidth(60)
        
        self.posCtrLayout.addWidget(self.goHome, 7,3,1,1,Qt.AlignLeft)
        self.posCtrLayout.addWidget(self.defHome, 8,3,1,1,Qt.AlignLeft)
        self.posCtrLayout.addWidget(self.defHWLim, 9,3,1,1,Qt.AlignLeft)
        self.posCtrLayout.addWidget(QLabel(""), 10,1,1,4,Qt.AlignCenter)
        
        #----------------------------------------------------------------------
        
        self.posWin = QHBoxLayout()
        self.posWin.addLayout(self.posCtrLayout)
                    
        self.xlimlow = QDoubleSpinBox()
        self.xlimlow.setMaximum(100)
        self.xlimlow.setMinimum(-100)
        self.xlimlow.setAlignment(Qt.AlignRight)
        self.xlimlow.setDecimals(3)
        self.xlimlow.setMinimumWidth(90)
        self.xlimlow.setValue(self.xScanMin)
        self.xlimlow.valueChanged.connect(self.xLimLowChange)
        self.xLimLowChange()

        self.xlimlowset = QPushButton()
        self.xlimlowset.setText(("X\u2098\u1D62\u2099"))
        self.xlimlowset.clicked.connect(self.xLimLowSet)
        self.xlimlowset.setMaximumWidth(45)
        
        self.xlimhigh = QDoubleSpinBox()
        self.xlimhigh.setMaximum(100)
        self.xlimhigh.setMinimum(-100)
        self.xlimhigh.setAlignment(Qt.AlignRight)
        self.xlimhigh.setDecimals(3)
        self.xlimhigh.setMinimumWidth(90)
        self.xlimhigh.setValue(self.xScanMax)
        self.xlimhigh.valueChanged.connect(self.xLimHighChange) 
        self.xLimHighChange()

        self.xlimhighset = QPushButton()
        self.xlimhighset.setText(("X\u2098\u2090\u2093"))
        self.xlimhighset.clicked.connect(self.xLimHighSet)
        self.xlimhighset.setMaximumWidth(45)
        
        self.xstep = QDoubleSpinBox()
        self.xstep.setMaximum(20)
        self.xstep.setMinimum(-20)
        self.xstep.setAlignment(Qt.AlignRight)
        self.xstep.setDecimals(3)
        self.xstep.setMinimumWidth(90)
        self.xstep.setValue(self.xScanStep)
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
        self.ylimlow.setValue(self.yScanMin)
        self.ylimlow.valueChanged.connect(self.yLimLowChange)
        self.yLimLowChange()

        self.ylimlowset = QPushButton()
        self.ylimlowset.setText(("Y\u2098\u1D62\u2099"))
        self.ylimlowset.clicked.connect(self.yLimLowSet)
        self.ylimlowset.setMaximumWidth(45)
        
        self.ylimhigh = QDoubleSpinBox()
        self.ylimhigh.setMaximum(5)
        self.ylimhigh.setMinimum(-5)
        self.ylimhigh.setAlignment(Qt.AlignRight)
        self.ylimhigh.setDecimals(3)
        self.ylimhigh.setMinimumWidth(90)
        self.ylimhigh.setValue(self.yScanMax)
        self.ylimhigh.valueChanged.connect(self.yLimHighChange) 
        self.yLimHighChange()

        self.ylimhighset = QPushButton()
        self.ylimhighset.setText(("Y\u2098\u2090\u2093"))
        self.ylimhighset.clicked.connect(self.yLimHighSet)
        self.ylimhighset.setMaximumWidth(45)
        
        self.ystep = QDoubleSpinBox()
        self.ystep.setMaximum(1)
        self.ystep.setMinimum(-1)
        self.ystep.setAlignment(Qt.AlignRight)
        self.ystep.setDecimals(3)
        self.ystep.setMinimumWidth(90)
        self.ystep.setValue(self.yScanStep)
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
        self.zlimlow.setValue(self.zScanMin)
        self.zlimlow.valueChanged.connect(self.zLimLowChange)
        self.zLimLowChange()

        self.zlimlowset = QPushButton()
        self.zlimlowset.setText(("Z\u2098\u1D62\u2099"))
        self.zlimlowset.clicked.connect(self.zLimLowSet)
        self.zlimlowset.setMaximumWidth(45)
        
        self.zlimhigh = QDoubleSpinBox()
        self.zlimhigh.setMaximum(150)
        self.zlimhigh.setMinimum(-150)
        self.zlimhigh.setAlignment(Qt.AlignRight)
        self.zlimhigh.setDecimals(3)
        self.zlimhigh.setMinimumWidth(90)
        self.zlimhigh.setValue(self.zScanMax)
        self.zlimhigh.valueChanged.connect(self.zLimHighChange)
        self.zLimLowChange() 

        self.zlimhighset = QPushButton()
        self.zlimhighset.setText(("Z\u2098\u2090\u2093"))
        self.zlimhighset.clicked.connect(self.zLimHighSet)
        self.zlimhighset.setMaximumWidth(45)
        
        self.zstep = QDoubleSpinBox()
        self.zstep.setMaximum(20)
        self.zstep.setMinimum(-20)
        self.zstep.setAlignment(Qt.AlignRight)
        self.zstep.setDecimals(3)
        self.zstep.setMinimumWidth(90)
        self.zstep.setValue(self.zScanStep)
        self.zstep.valueChanged.connect(self.zStepChange) 
        self.zStepChange()
        
        self.zactive = QCheckBox('onZ')
        self.zactive.setChecked(True)
        self.zactive.stateChanged.connect(lambda:self.btnstate(self.zactive))

        #self.progress = QProgressBar(self)
        #self.progress.resetProgressBar()

        self.scanCtrLayout = QGridLayout()
        self.scanCtrLayout.setContentsMargins(4, 4, 4, 4)
        self.scanCtrLayout.setSpacing(2)
        self.scanCtrLayout.setObjectName("scanCtrLayout") 
   
        self.scanCtrLayout.addWidget(QLabel('Limits for Automatic Scan<br>'), 10,1,1,7,Qt.AlignCenter)
        #scan limits and steps     

        self.scanCtrLayout.addWidget(self.xlimlowset, 13,1,1,1,Qt.AlignCenter)
        self.scanCtrLayout.addWidget(self.xlimlow, 13,2,1,1,Qt.AlignLeft)
        self.scanCtrLayout.addWidget(self.xlimhighset, 13,3,1,1,Qt.AlignCenter)
        self.scanCtrLayout.addWidget(self.xlimhigh, 13,4,1,1,Qt.AlignLeft)
        self.scanCtrLayout.addWidget(QLabel('X<sub>step</sub>'), 13,5,1,1,Qt.AlignCenter)
        self.scanCtrLayout.addWidget(self.xstep, 13,6,1,1,Qt.AlignLeft)
        self.scanCtrLayout.addWidget(self.xactive, 13,7,1,1,Qt.AlignCenter)
        
        self.scanCtrLayout.addWidget(self.ylimlowset, 14,1,1,1,Qt.AlignCenter)
        self.scanCtrLayout.addWidget(self.ylimlow, 14,2,1,1,Qt.AlignLeft)
        self.scanCtrLayout.addWidget(self.ylimhighset, 14,3,1,1,Qt.AlignCenter)
        self.scanCtrLayout.addWidget(self.ylimhigh, 14,4,1,1,Qt.AlignLeft)
        self.scanCtrLayout.addWidget(QLabel('Y<sub>step</sub>'), 14,5,1,1,Qt.AlignCenter)
        self.scanCtrLayout.addWidget(self.ystep, 14,6,1,1,Qt.AlignLeft)
        self.scanCtrLayout.addWidget(self.yactive, 14,7,1,1,Qt.AlignCenter)

        self.scanCtrLayout.addWidget(self.zlimlowset, 15,1,1,1,Qt.AlignCenter)
        self.scanCtrLayout.addWidget(self.zlimlow, 15,2,1,1,Qt.AlignLeft)
        self.scanCtrLayout.addWidget(self.zlimhighset, 15,3,1,1,Qt.AlignCenter)
        self.scanCtrLayout.addWidget(self.zlimhigh, 15,4,1,1,Qt.AlignLeft)
        self.scanCtrLayout.addWidget(QLabel('Z<sub>step</sub>'), 15,5,1,1,Qt.AlignCenter)
        self.scanCtrLayout.addWidget(self.zstep, 15,6,1,1,Qt.AlignLeft)
        self.scanCtrLayout.addWidget(self.zactive, 15,7,1,1,Qt.AlignCenter)
        #self.scanCtrLayout.addWidget(QLabel('    Progress: '), 16,1,1,1,Qt.AlignCenter)
        #self.scanCtrLayout.addWidget(self.progress, 16,2,1,6, Qt.AlignLeft)
        self.scanCtrLayout.addWidget(QLabel('<br>'), 17,1,1,1,Qt.AlignCenter)

        
        self.scanWin = QHBoxLayout()
        self.scanWin.addLayout(self.scanCtrLayout)
        
        
        ############################ end position control ##############################
        
        ############################ start acquisiton control ##############################
        
        #start Acquisition control
        self.acqCtrLayout = QGridLayout()
        self.acqCtrLayout.setContentsMargins(4, 4, 4, 4)
        self.acqCtrLayout.setSpacing(2)
        self.acqCtrLayout.setObjectName("acqCtrLayout") 
        
        
        self.acqCtrLayout.addWidget(QLabel("<h2>Acquisition Control</h2>"), 1,1,1,8,Qt.AlignCenter)   
        self.acqCtrLayout.addWidget(QLabel(""), 2,1,1,4,Qt.AlignCenter)
        self.acqCtrLayout.addWidget(QLabel('    Run Number:'), 3,1,1,1,Qt.AlignLeft)
        self.run_number = QLabel(str(self.datahandler.runnumber))
        
        self.acqCtrLayout.addWidget(self.run_number, 3,2,1,1, Qt.AlignCenter)
        
        self.acqCtrLayout.addWidget(QLabel('    Diamond Name:'), 4,1,1,1,Qt.AlignLeft)
        self.diamond_name = QComboBox()
        self.diamond_name.addItems(['S116', 'S118', 'Heisenberg', 'Dirac', 'Einstein', 'Higgs', 'Other'])
        self.diamond_name.setMinimumWidth(104)
        self.diamond_name.setCurrentText(self.datahandler.diamond_name)
        self.diamond_name.currentIndexChanged.connect(self.diamNameSlot)
        self.acqCtrLayout.addWidget(self.diamond_name, 4,2,1,1, Qt.AlignLeft)
        
        self.acqCtrLayout.addWidget(QLabel('    Bias Voltage [V]:'), 5,1,1,1,Qt.AlignLeft)
        self.bias_voltage = QDoubleSpinBox()
        self.bias_voltage.setMinimum(-1500)
        self.bias_voltage.setMaximum(1500)
        self.bias_voltage.setAlignment(Qt.AlignLeft)
        self.bias_voltage.setMinimumWidth(104)
        self.bias_voltage.setValue(self.datahandler.bias_voltage)
        self.bias_voltage.valueChanged.connect(self.biasVoltageSlot) 
        self.acqCtrLayout.addWidget(self.bias_voltage, 5,2,1,1, Qt.AlignLeft)
        
        self.acqCtrLayout.addWidget(QLabel('    Number of WF:'), 6,1,1,1,Qt.AlignLeft)
        self.nwf = QSpinBox()
        self.nwf.setMinimum(0)
        self.nwf.setMaximum(1000)
        self.nwf.setAlignment(Qt.AlignLeft)
        self.nwf.setMinimumWidth(104)
        self.nwf.setValue(self.datahandler.nwf)
        self.nwf.valueChanged.connect(self.nwfSlot) 
        self.acqCtrLayout.addWidget(self.nwf, 6,2,1,1, Qt.AlignLeft)
                
        self.acqCtrLayout.addWidget(QLabel('        Pulse Energy [pJ]:   '), 3,3,1,1,Qt.AlignLeft)
        self.pulse_energy = QDoubleSpinBox()
        self.pulse_energy.setMinimum(0)
        self.pulse_energy.setMaximum(10000)
        self.pulse_energy.setAlignment(Qt.AlignLeft)
        self.pulse_energy.setMinimumWidth(104)
        self.pulse_energy.setValue(self.datahandler.laser_pulse_energy)
        self.pulse_energy.valueChanged.connect(self.pulseEnergySlot) 
        self.acqCtrLayout.addWidget(self.pulse_energy, 3,4,1,1, Qt.AlignLeft)
        
        self.acqCtrLayout.addWidget(QLabel('        Side:'), 4,3,1,1,Qt.AlignLeft)
        self.diamond_side = QComboBox()
        self.diamond_side.addItems(['0', '1'])
        self.diamond_side.setMinimumWidth(104)
        self.diamond_side.setCurrentText(str(self.datahandler.side))
        self.diamond_side.currentIndexChanged.connect(self.diamSideSlot)
        self.acqCtrLayout.addWidget(self.diamond_side, 4,4,1,1, Qt.AlignLeft)
        
        self.acqCtrLayout.addWidget(QLabel('        Scan Type:'), 5,3,1,1,Qt.AlignLeft)
        self.scan_type = QComboBox()
        self.scan_type.addItems(['regular', 'knive_edge'])
        self.scan_type.setMinimumWidth(104)
        self.scan_type.setCurrentText(self.datahandler.scan_type)
        self.scan_type.currentIndexChanged.connect(self.ScanTypeSlot)
        self.acqCtrLayout.addWidget(self.scan_type, 5,4,1,1, Qt.AlignLeft)
          
        self.acqCtrLayout.addWidget(QLabel('        PCB Version:'), 6,3,1,1,Qt.AlignLeft) 
        self.pcb = QComboBox()
        self.pcb.addItems(['simple', 'car'])
        self.pcb.setMinimumWidth(104)
        self.pcb.setCurrentText(self.datahandler.pcb)
        self.pcb.currentIndexChanged.connect(self.PCBSlot)
        self.acqCtrLayout.addWidget(self.pcb, 6,4,1,1, Qt.AlignLeft)
        
        self.acqCtrLayout.addWidget(QLabel('    Comments:'), 11,1,1,1,Qt.AlignLeft) 
        self.comments = QTextEdit()
        self.comments.setMinimumWidth(370)
        self.comments.setMaximumHeight(50)
        self.acqCtrLayout.addWidget(self.comments, 11,2,1,8, Qt.AlignLeft)
        
        self.acqWin = QHBoxLayout()
        self.acqWin.addLayout(self.acqCtrLayout)
    
    
        #start Acquisition control
        self.acqCtr2Layout = QGridLayout()
        self.acqCtr2Layout.setContentsMargins(4, 4, 4, 4)
        self.acqCtr2Layout.setSpacing(2)
        self.acqCtr2Layout.setObjectName("acqCtr2Layout") 

        self.opMode = QPushButton()
        self.opMode.setText('Manual')
        self.opMode.setStyleSheet("background-color: red")
        self.opMode.clicked.connect(self.operatingMode)

        self.newFile = QPushButton()
        self.newFile.setText('New File')
        self.newFile.clicked.connect(self.newFileSlot)
        self.newFile.setEnabled(False)

        self.collectWf = QPushButton()
        self.collectWf.setText('Collect WF')
        self.collectWf.clicked.connect(self.collectWfSlot)
        self.collectWf.setEnabled(False)
    
        self.startScan = QPushButton()
        self.startScan.setText('Start Scan')
        self.startScan.clicked.connect(self.startScanSlot)
        self.startScan.setEnabled(False)
        
        self.stopScan = QPushButton()
        self.stopScan.setText('Stop Scan')
        self.stopScan.clicked.connect(self.stopScanSlot)
        self.stopScan.setEnabled(False)
        
        self.closeFile = QPushButton()
        self.closeFile.setText('Close File')
        self.closeFile.clicked.connect(self.closeFileSlot)
        self.closeFile.setEnabled(False)  
        
        self.acqCtr2Layout.addWidget(QLabel('Tektronix Mode'), 1,1,1,1,Qt.AlignCenter) 
        self.acqCtr2Layout.addWidget(self.opMode, 2,1,1,1,Qt.AlignCenter)
        self.acqCtr2Layout.addWidget(self.newFile, 2,2,1,1,Qt.AlignCenter)
        self.acqCtr2Layout.addWidget(self.collectWf, 2,3,1,1,Qt.AlignCenter)     
        self.acqCtr2Layout.addWidget(self.startScan, 2,4,1,1,Qt.AlignCenter)
        self.acqCtr2Layout.addWidget(self.stopScan, 2,5,1,1,Qt.AlignCenter)
        self.acqCtr2Layout.addWidget(self.closeFile, 2,6,1,1,Qt.AlignCenter)     
        
        self.acq2Win = QHBoxLayout()
        self.acq2Win.addLayout(self.acqCtr2Layout)
    

        ############################ end acquisiton control ##############################
        
        ############################    start plotting      ##############################
        
        # generate layout
        plotLayout = QVBoxLayout()
        plotLayout.addWidget(self.livemon.canvas)
        self.toolbar = NavigationToolbar(self.livemon.canvas, self) #navigation widget
        plotLayout.addWidget(self.toolbar)
        
        
        ############################     end plotting       ##############################
        

        #master layout
        self.mainLayout = QHBoxLayout()
        
        #the control layout, add it to master layout
        self.controlLayout = QVBoxLayout()
        self.controlLayout.addLayout(self.posWin)
        self.controlLayout.addLayout(self.scanWin)
        self.controlLayout.addLayout(self.acqWin)
        self.controlLayout.addLayout(self.acq2Win)
        self.mainLayout.addLayout(self.controlLayout)
        
        #add plot layout to master layout
        self.mainLayout.addLayout(plotLayout)
        
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
        self.acqControl.setXmin(self.xlimlow.value())
        self.livemon.setPlotLimits([self.acqControl.xScanMin, self.acqControl.xScanMax, self.acqControl.yScanMin, self.acqControl.yScanMax, self.acqControl.zScanMin, self.acqControl.zScanMax])
    
    def xLimLowSet(self):
        val = self.positionControl.getXPosition()
        self.xlimlow.setValue(val)

    def xLimHighChange(self):
        self.acqControl.setXmax(self.xlimhigh.value())
        self.livemon.setPlotLimits([self.acqControl.xScanMin, self.acqControl.xScanMax, self.acqControl.yScanMin, self.acqControl.yScanMax, self.acqControl.zScanMin, self.acqControl.zScanMax])
        
    def xLimHighSet(self):
        val = self.positionControl.getXPosition()
        self.xlimhigh.setValue(val)

    def xStepChange(self):
        self.acqControl.setStepX(self.xstep.value())
        self.livemon.setStepSize([self.acqControl.xScanStep, self.acqControl.yScanStep, self.acqControl.zScanStep])
        
        
    def yLimLowChange(self):
        self.acqControl.setYmin(self.ylimlow.value())
        self.livemon.setPlotLimits([self.acqControl.xScanMin, self.acqControl.xScanMax, self.acqControl.yScanMin, self.acqControl.yScanMax, self.acqControl.zScanMin, self.acqControl.zScanMax])

    def yLimLowSet(self):
        val = self.positionControl.getYPosition()
        self.ylimlow.setValue(val)

    def yLimHighChange(self):
        self.acqControl.setYmax(self.ylimhigh.value())
        self.livemon.setPlotLimits([self.acqControl.xScanMin, self.acqControl.xScanMax, self.acqControl.yScanMin, self.acqControl.yScanMax, self.acqControl.zScanMin, self.acqControl.zScanMax])
 
    def yLimHighSet(self):
        val = self.positionControl.getYPosition()
        self.ylimhigh.setValue(val)
       
    def yStepChange(self):
        self.acqControl.setStepY(self.ystep.value())
        self.livemon.setStepSize([self.acqControl.xScanStep, self.acqControl.yScanStep, self.acqControl.zScanStep])
     
        
    def zLimLowChange(self):
        self.acqControl.setZmin(self.zlimlow.value())
        self.livemon.setPlotLimits([self.acqControl.xScanMin, self.acqControl.xScanMax, self.acqControl.yScanMin, self.acqControl.yScanMax, self.acqControl.zScanMin, self.acqControl.zScanMax])

    def zLimLowSet(self):
        val = self.positionControl.getZPosition()
        self.zlimlow.setValue(val)

    def zLimHighChange(self):
        self.acqControl.setZmax(self.zlimhigh.value())
        self.livemon.setPlotLimits([self.acqControl.xScanMin, self.acqControl.xScanMax, self.acqControl.yScanMin, self.acqControl.yScanMax, self.acqControl.zScanMin, self.acqControl.zScanMax])

    def zLimHighSet(self):
        val = self.positionControl.getZPosition()
        self.zlimhigh.setValue(val)

    def zStepChange(self):
        self.acqControl.setStepZ(self.zstep.value())
        self.livemon.setStepSize([self.acqControl.xScanStep, self.acqControl.yScanStep, self.acqControl.zScanStep])
  
    
    def btnstate(self,b):
        if b.text() == 'onX':
            if b.isChecked() == True:
                self.acqControl.setXactive(True)
            else:
                self.acqControl.setXactive(False)

        if b.text() == 'onY':
            if b.isChecked() == True:
                self.acqControl.setYactive(True)
            else:
                self.acqControl.setYactive(False)

        if b.text() == 'onZ':
            if b.isChecked() == True:
                self.acqControl.setZactive(True)
            else:
                self.acqControl.setZactive(False)
    
        
    def startScanSlot(self):
        self.scanThread.start()
        self.stopScan.setEnabled(True)
        self.collectWf.setEnabled(False)
        self.startScan.setEnabled(False)
        self.closeFile.setEnabled(False)
        
        
    def stopScanSlot(self):
        self.pill2kill.set()
        self.scanThread.join(2)
        self.stopScan.setEnabled(False)
        self.collectWf.setEnabled(True)
        self.startScan.setEnabled(True)
        self.closeFile.setEnabled(True)
        self.pill2kill = threading.Event()
        self.scanThread = threading.Thread(target=self.acqControl.startScan, args=(self.pill2kill, 'test'))
             
    def diamNameSlot(self):
        self.datahandler.setDiamondName(self.diamond_name.currentText())
        self.newFile.setEnabled(False)
        
    def diamSideSlot(self):
        self.datahandler.setSide(self.diamond_side.currentText())
        self.newFile.setEnabled(False)   
 
    def ScanTypeSlot(self):
        self.datahandler.setScanType(self.scan_type.currentText())
        self.acqControl.tek.setScanType(self.scan_type.currentText())
        self.newFile.setEnabled(False)
       
    def PCBSlot(self):
        self.datahandler.setPCB(self.pcb.currentText())
        self.newFile.setEnabled(False)
        
    def nwfSlot(self):
        self.datahandler.setNWf(self.nwf.value())
        self.newFile.setEnabled(False)
        
    def pulseEnergySlot(self):
        self.datahandler.setLaserPulseEnergy(self.pulse_energy.value())
        self.newFile.setEnabled(False)

    def biasVoltageSlot(self):
        self.datahandler.setBiasVoltage(self.bias_voltage.value())
        self.newFile.setEnabled(False)

    def newFileSlot(self):
        comment = str(self.comments.toPlainText())
        self.datahandler.createFile(comment)
        self.run_number.setText(str(self.datahandler.runnumber))
        self.newFile.setEnabled(False)
        self.collectWf.setEnabled(True)
        self.closeFile.setEnabled(True)
        self.startScan.setEnabled(True)
        self.fileOpen = True
        
        #disable other input options
        self.diamond_name.setEnabled(False)
        self.bias_voltage.setEnabled(False)
        self.nwf.setEnabled(False)
        self.pulse_energy.setEnabled(False)
        self.diamond_side.setEnabled(False)
        self.scan_type.setEnabled(False)
        self.pcb.setEnabled(False)
        self.comments.setEnabled(False)
        
        
    def closeFileSlot(self):
        self.datahandler.closeFile()
        self.collectWf.setEnabled(False)
        self.closeFile.setEnabled(False)
        self.startScan.setEnabled(False)
        self.newFile.setEnabled(True)
        self.fileOpen = False
        
        #enable other input options
        self.diamond_name.setEnabled(True)
        self.bias_voltage.setEnabled(True)
        self.nwf.setEnabled(True)
        self.pulse_energy.setEnabled(True)
        self.diamond_side.setEnabled(True)
        self.scan_type.setEnabled(True)
        self.pcb.setEnabled(True)
        self.comments.setEnabled(True)
        self.livemon.resetPlots()
        
        
    def collectWfSlot(self):
        if (not self.tekconfigured):
            self.acqControl.configureTek()
            self.tekconfigured = True
        self.acqControl.collectNWfs()
        
    def operatingMode(self):
        if(self.opMode.text() == 'Manual'):
            self.opMode.setText('Software')
            self.opMode.setStyleSheet("background-color: green")
            self.acqControl.openTek()
            self.acqControl.configureTek()
            self.tekconfigured = True
            if(self.fileOpen):
                self.newFile.setEnabled(False)
                self.collectWf.setEnabled(True)
                self.startScan.setEnabled(True)
                self.closeFile.setEnabled(True)
            else:
                self.newFile.setEnabled(True)
                self.collectWf.setEnabled(False)
                self.startScan.setEnabled(False)
                self.closeFile.setEnabled(False)
            
        else:
            self.opMode.setText('Manual')
            self.opMode.setStyleSheet("background-color: red")
            self.acqControl.closeTek()
            if(self.fileOpen):
                self.newFile.setEnabled(False)
                self.collectWf.setEnabled(False)
                self.startScan.setEnabled(False)
                self.closeFile.setEnabled(True)
            else:
                self.newFile.setEnabled(True)
                self.collectWf.setEnabled(False)
                self.startScan.setEnabled(False)
                self.closeFile.setEnabled(False)
        
        self.newFile.setEnabled(True)

    #def setProgressBarStep(self, val):
    #    self.progress.setValue(val)

    #def resetProgressBar(self):
    #    self.progress.reset()
    #    self.progress.setRange(0, self.acqControl.estimateScanSteps())
