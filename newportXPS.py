from newportxps import NewportXPS
from time import sleep, time
from configobj import ConfigObj


class XPS(object):
    """ Class for controlling a XPS stage """

    def __init__(self, conf):
        self.conf = conf['Newport']
        self.xps = NewportXPS(self.conf['address'], username=self.conf['username'], password=self.conf['password'])
        print(self.xps.status_report())        

    def get_xpos(self):
        return self.xps.get_stage_position('Group2.Pos')

    def get_ypos(self):
        return self.xps.get_stage_position('Group3.Pos')

    def get_zpos(self):
        return self.xps.get_stage_position('Group1.Pos')

    def move_x(self, xpos):
        self.xps.move_stage('Group2.Pos', xpos)

    def move_y(self, ypos):
        self.xps.move_stage('Group3.Pos', ypos)

    def move_z(self, zpos):
        self.xps.move_stage('Group1.Pos', zpos)


if __name__ == "__main__":
    conf = ConfigObj('config.ini')
    xps = XPS(conf=conf)
    print('x: ', xps.get_xpos())
    print('y: ', xps.get_ypos())
    print('z: ', xps.get_zpos())