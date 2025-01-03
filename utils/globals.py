import sys
from gegede import Quantity as Q

class Params:
    def __init__(self):
        # defaults
        self.params = {}
        self.World = None
        self.TPC = None
        self.Cryostat = None
        self.Detenc = None
        self.Fieldcage = None
        self.Cathode = None
        self.Arapuca = None

    @property
    def World(self):
        return self.world

    @World.setter
    def World(self, inputdict):
        self.world = {}
        self.world['FieldCage_switch'] = True
        self.world['Cathode_switch'] = True
        self.world['workspace'] = 0
        self.world['pdsconfig'] = 0
        self.world['wires'] = True
        self.world['tpc'] = True
        if inputdict:
            self.world.update(inputdict)
        self.params.update(self.world)


    @property
    def TPC(self):
        return self.tpc

    @TPC.setter
    def TPC(self, inputdict):
        self.tpc = {}
        self.tpc['nChans'] = {'Ind1': 286, 'Ind1Bot': 96, 'Ind2': 286, 'Col': 292}

        self.tpc['wirePitchU'] = Q('0.765cm')
        self.tpc['wirePitchV'] = Q('0.765cm')
        self.tpc['wirePitchZ'] = Q('0.51cm')

        self.tpc['wireAngleU'] = Q('150.0deg')
        self.tpc['wireAngleV'] = Q('30.0deg')

        self.tpc['widthPCBActive'] = Q('167.7006cm')
        self.tpc['borderCRM'] = Q('0.0cm')
        self.tpc['borderCRP'] = Q('0.5cm')

        self.tpc['nCRM_x'] = 4*2
        self.tpc['nCRM_z'] = 20*2

        self.tpc['driftTPCActive'] = Q('650.0cm')
        self.tpc['padWidth'] = Q('0.02cm')
        if inputdict:
            self.tpc.update(inputdict)
        self.tpc['nViews'] = len(self.tpc['nChans'])
        self.tpc['lengthPCBActive'] = self.tpc['wirePitchZ'] * self.tpc['nChans']['Col']
        self.tpc['widthCRM_active'] = self.tpc['widthPCBActive']
        self.tpc['lengthCRM_active'] = self.tpc['lengthPCBActive']
        self.tpc['widthCRM'] = self.tpc['widthPCBActive'] + 2 * self.tpc['borderCRM']
        self.tpc['lengthCRM'] = self.tpc['lengthPCBActive'] + 2 * self.tpc['borderCRM']

        if self.world['workspace'] == 1:
            self.tpc['nCRM_x'] = 1 * 2
            self.tpc['nCRM_z'] = 1 * 2
        if self.world['workspace'] == 2:
            self.tpc['nCRM_x'] = 2 * 2
            self.tpc['nCRM_z'] = 2 * 2
        if self.world['workspace'] == 3:
            self.tpc['nCRM_x'] = 4 * 2
            self.tpc['nCRM_z'] = 3 * 2
        if self.world['workspace'] == 4:
            self.tpc['nCRM_x'] = 4 * 2
            self.tpc['nCRM_z'] = 7 * 2
        if self.world['workspace'] == 5:
            self.tpc['nCRM_x'] = 4 * 2
            self.tpc['nCRM_z'] = 20 * 2

        self.tpc['widthTPCActive'] = self.tpc['nCRM_x'] * (self.tpc['widthCRM'] + self.tpc['borderCRP'])
        self.tpc['lengthTPCActive'] = self.tpc['nCRM_z'] * (self.tpc['lengthCRM'] + self.tpc['borderCRP'])
        self.tpc['ReadoutPlane'] = self.tpc['nViews'] * self.tpc['padWidth']
        self.tpc['anodePlateWidth'] = self.tpc['padWidth']/2.

        self.params.update(self.tpc)


    @property
    def Cryostat(self):
        return self.cryostat

    @Cryostat.setter
    def Cryostat(self, inputdict):
        self.cryostat = {}
        self.cryostat['Argon_x'] = Q('1510cm')
        self.cryostat['Argon_y'] = Q('1510cm')
        self.cryostat['Argon_z'] = Q('6200cm')
        self.cryostat['HeightGaseousAr'] = Q('100cm')
        self.cryostat['SteelThickness'] = Q('0.12cm') # membrane
        if inputdict:
            self.cryostat.update(inputdict)
        if self.world['workspace'] != 0:
            self.cryostat['Argon_x'] = self.tpc['driftTPCActive'] + self.cryostat['HeightGaseousAr'] + self.tpc['ReadoutPlane'] + Q('100cm')
            self.cryostat['Argon_y'] = self.tpc['widthTPCActive'] + Q('162cm')
            self.cryostat['Argon_z'] = self.tpc['lengthTPCActive'] + Q('214.0cm')
        self.cryostat['xLArBuffer'] = self.cryostat['Argon_x'] - self.tpc['driftTPCActive'] - self.cryostat['HeightGaseousAr'] - self.tpc['ReadoutPlane']
        self.cryostat['yLArBuffer'] = 0.5 * (self.cryostat['Argon_y'] - self.tpc['widthTPCActive'])
        self.cryostat['zLArBuffer'] = 0.5 * (self.cryostat['Argon_z'] - self.tpc['lengthTPCActive'])

        self.cryostat['Cryostat_x'] = self.cryostat['Argon_x'] + 2*self.cryostat['SteelThickness']
        self.cryostat['Cryostat_y'] = self.cryostat['Argon_y'] + 2*self.cryostat['SteelThickness']
        self.cryostat['Cryostat_z'] = self.cryostat['Argon_z'] + 2*self.cryostat['SteelThickness']

        self.params.update(self.cryostat)

    @property
    def Enclosure(self):
        return self.detenc

    @Enclosure.setter
    def Enclosure(self, inputdict):
        self.detenc = {}
        self.detenc['SteelSupport_x'] = Q('100cm')
        self.detenc['SteelSupport_y'] = Q('100cm')
        self.detenc['SteelSupport_z'] = Q('100cm')
        self.detenc['FoamPadding'] = Q('80cm')
        self.detenc['FracMassOfSteel'] = 0.5
        self.detenc['SpaceSteelSupportToWall']    = Q('100cm')
        self.detenc['SpaceSteelSupportToCeiling'] = Q('100cm')
        self.detenc['RockThickness'] = Q('4000cm')
        if inputdict:
            self.detenc.update(inputdict)
        self.detenc['FracMassOfAir'] = 1 - self.detenc['FracMassOfSteel']
        self.detenc['DetEncX']  =    self.cryostat['Cryostat_x'] + 2*(self.detenc['SteelSupport_x'] + self.detenc['FoamPadding']) + self.detenc['SpaceSteelSupportToCeiling']

        self.detenc['DetEncY']  =    self.cryostat['Cryostat_y'] + 2*(self.detenc['SteelSupport_y'] + self.detenc['FoamPadding']) + 2*self.detenc['SpaceSteelSupportToWall']

        self.detenc['DetEncZ']  =    self.cryostat['Cryostat_z'] + 2*(self.detenc['SteelSupport_z'] + self.detenc['FoamPadding']) + 2*self.detenc['SpaceSteelSupportToWall']

        self.detenc['posCryoInDetEnc_x'] = - self.detenc['DetEncX']/2 + self.detenc['SteelSupport_x'] + self.detenc['FoamPadding'] + self.cryostat['Cryostat_x']/2

        self.detenc['OriginXSet'] =  self.detenc['DetEncX']/2.0 - self.detenc['SteelSupport_x'] - self.detenc['FoamPadding'] - self.cryostat['SteelThickness'] - self.cryostat['xLArBuffer'] - self.tpc['driftTPCActive']/2.0

        self.detenc['OriginYSet'] =   self.detenc['DetEncY']/2.0 - self.detenc['SpaceSteelSupportToWall'] - self.detenc['SteelSupport_y'] - self.detenc['FoamPadding'] - self.cryostat['SteelThickness'] - self.cryostat['yLArBuffer'] - self.tpc['widthTPCActive']/2.0

        self.detenc['OriginZSet'] =   self.detenc['DetEncZ']/2.0 - self.detenc['SpaceSteelSupportToWall'] - self.detenc['SteelSupport_z'] - self.detenc['FoamPadding'] - self.cryostat['SteelThickness'] - self.cryostat['zLArBuffer'] - self.tpc['borderCRM']

        self.params.update(self.detenc)

    @property
    def FieldCage(self):
        return self.fieldcage

    @FieldCage.setter
    def FieldCage(self, inputdict):
        self.fieldcage = {}
        self.fieldcage['FieldShapeInnerRadius'] = Q('0.5cm')
        self.fieldcage['FieldShapeOuterRadius'] = Q('2.285cm')
        self.fieldcage['FieldShapeOuterRadiusSlim'] = Q('0.75cm')
        self.fieldcage['FieldShapeTorRad'] = Q('2.3cm')
        self.fieldcage['FieldShapeArapucaWindowLength'] = Q('670cm')
        self.fieldcage['FieldShaperSeparation'] = Q('6.0cm')
        if inputdict:
            self.fieldcage.update(inputdict)
        self.fieldcage['FieldShaperLongTubeLength']  =  self.tpc['lengthTPCActive']
        self.fieldcage['FieldShaperShortTubeLength'] =  self.tpc['widthTPCActive']
        self.fieldcage['FieldShaperLength'] = self.fieldcage['FieldShaperLongTubeLength'] + 2*self.fieldcage['FieldShaperOuterRadius']+ 2*self.fieldcage['FieldShaperTorRad']
        self.fieldcage['FieldShaperWidth'] =  self.fieldcage['FieldShaperShortTubeLength'] + 2*self.fieldcage['FieldShaperOuterRadius']+ 2*self.fieldcage['FieldShaperTorRad']

        self.fieldcage['NFieldShapers'] = (self.tpc['driftTPCActive']/self.fieldcage['FieldShaperSeparation']) - 1

        self.fieldcage['FieldCageSizeX'] = self.fieldcage['FieldShaperSeparation']*self.fieldcage['NFieldShapers']+2
        self.fieldcage['FieldCageSizeY'] = self.fieldcage['FieldShaperWidth']+2
        self.fieldcage['FieldCageSizeZ'] = self.fieldcage['FieldShaperLength']+2

        self.params.update(self.fieldcage)

    @property
    def Cathode(self):
        return self.cathode

    @Cathode.setter
    def Cathode(self, inputdict):
        self.cathode = {}
        self.cathode['heightCathode'] = Q('4.0cm')
        self.cathode['CathodeBorder'] = Q('4.0cm')
        self.cathode['widthCathodeVoid'] = Q('76.35cm')
        self.cathode['lengthCathodeVoid'] = Q('67.0cm')
        if inputdict:
            self.cathode.update(inputdict)
        self.cathode['widthCathode'] =2*self.tpc['widthCRM']
        self.cathode['lengthCathode']=2*self.tpc['lengthCRM']

        self.params.update(self.cathode)

    @property
    def Arapuca(self):
        return self.arapuca

    @Arapuca.setter
    def Arapuca(self, inputdict):
        self.arapuca = {}
        self.arapuca['ArapucaOut_x'] = Q('65.0cm')
        self.arapuca['ArapucaOut_y'] = Q('2.5cm')
        self.arapuca['ArapucaOut_z'] = Q('65.0cm')
        self.arapuca['ArapucaIn_x'] = Q('60.0cm')
        self.arapuca['ArapucaIn_y'] = Q('2.0cm')
        self.arapuca['ArapucaIn_z'] = Q('60.0cm')
        self.arapuca['ArapucaAcceptanceWindow_x'] = Q('60.0cm')
        self.arapuca['ArapucaAcceptanceWindow_y'] = Q('1.0cm')
        self.arapuca['ArapucaAcceptanceWindow_z'] = Q('60.0cm')
        self.arapuca['GapPD'] = Q('0.5cm')
        self.arapuca['FrameToArapucaSpace'] = Q('1.0cm')
        self.arapuca['FrameToArapucaSpaceLat'] = Q('10.0cm')
        self.arapuca['VerticalPDdist'] = Q('75.0cm')
        self.arapuca['FirstFrameVertDist'] = Q('40.0cm')
        if inputdict:
            self.arapuca.update(inputdict)
        self.arapuca['list_posx_bot'] = [0]*4
        self.arapuca['list_posz_bot'] = [0]*4

        self.arapuca['list_posx_bot'][0]=-2*self.cathode['widthCathodeVoid'] - 2.0*self.cathode['CathodeBorder'] + self.arapuca['GapPD'] + 0.5*self.arapuca['ArapucaOut_x']
        self.arapuca['list_posz_bot'][0]= 0.5*self.cathode['lengthCathodeVoid'] + self.cathode['CathodeBorder']
        self.arapuca['list_posx_bot'][1]= - self.cathode['CathodeBorder'] - self.arapuca['GapPD'] - 0.5*self.arapuca['ArapucaOut_x']
        self.arapuca['list_posz_bot'][1]=-1.5*self.cathode['lengthCathodeVoid'] - 2.0*self.cathode['CathodeBorder']
        self.arapuca['list_posx_bot'][2]=-self.arapuca['list_posx_bot'][1]
        self.arapuca['list_posz_bot'][2]=-self.arapuca['list_posz_bot'][1]
        self.arapuca['list_posx_bot'][3]=-self.arapuca['list_posx_bot'][0]
        self.arapuca['list_posz_bot'][3]=-self.arapuca['list_posz_bot'][0]

        self.params.update(self.arapuca)

    def get(self, key):
        if key not in self.params:
            print("Unable to access requested parameter. Exiting")
            sys.exit(1)
        return self.params[key]
