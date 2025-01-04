#!/usr/bin/env python
'''
Arapuca builder for DUNE FD-VD
      <solidref ref="ArapucaAcceptanceWindow"/>
      <solidref ref="ArapucaAcceptanceWindow"/>
      <solidref ref="ArapucaAcceptanceWindowShortLat"/>
      <solidref ref="ArapucaAcceptanceWindowCathode"/>
    <volume name="Arapuca">
      <materialref ref="G10" />
      <solidref ref="ArapucaWalls" />
    </volume>

    <volume name="volArapuca">
      <materialref ref="LAr"/>
      <solidref ref="ArapucaOut"/>
      <physvol>
        <volumeref ref="Arapuca"/>
        <positionref ref="posCenter"/>
      </physvol>
      <physvol>
        <volumeref ref="volOpDetSensitive"/>
        <position name="opdetshift" unit="cm" x="0" y="@{[$ArapucaAcceptanceWindow_y/2.0]}" z="0"/>
      </physvol>
    </volume>


    <volume name="volArapucaLongLat">
      <materialref ref="LAr"/>
      <solidref ref="ArapucaOut"/>
      <physvol>
        <volumeref ref="Arapuca"/>
        <positionref ref="posCenter"/>
      </physvol>
      <physvol>
        <volumeref ref="volOpDetSensitiveLongLat"/>
        <position name="opdetshift" unit="cm" x="0" y="@{[$ArapucaAcceptanceWindow_y/2.0]}" z="0"/>
      </physvol>
    </volume>

    <volume name="volArapucaShortLat">
      <materialref ref="LAr"/>
      <solidref ref="ArapucaOutShortLat"/>
      <physvol>
        <volumeref ref="Arapuca"/>
        <positionref ref="posCenter"/>
        <rotationref ref="rMinus90AboutX" />
      </physvol>
      <physvol>
        <volumeref ref="volOpDetSensitiveShortLat"/>
        <position name="opdetshift" unit="cm" x="0" y="0" z="@{[$ArapucaAcceptanceWindow_y/2.0]}"/>
      </physvol>
    </volume>

    <volume name="volArapucaCathode">
      <materialref ref="LAr"/>
      <solidref ref="ArapucaOutCathode"/>
      <physvol>
        <volumeref ref="Arapuca"/>
        <positionref ref="posCenter"/>
        <rotationref ref="rPlus90AboutXPlus90AboutZ"/>
      </physvol>
      <physvol>
        <volumeref ref="volOpDetSensitiveCathode"/>
        <position name="opdetshift" unit="cm" x="@{[$ArapucaAcceptanceWindow_y/2.0]}" y="0" z="0"/>
      </physvol>
    </volume>

'''

import gegede.builder
from utils import *

class ArapucaBuilder(gegede.builder.Builder):
    def configure(self, **kwds):
        if not set(kwds).issubset(globals.Arapuca): # no unknown keywords
            msg = 'Unknown parameter in: "%s"' % (', '.join(sorted(kwds.keys())), )
            raise ValueError(msg)

        # The builder hierarchy takes care of all the configuration parameters
        globals.Arapuca = kwds
