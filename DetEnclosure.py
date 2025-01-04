
#!/usr/bin/env python
'''
DetEnclosure builder for DUNE FD-VD
'''

import gegede.builder
from utils import *

class DetEnclosureBuilder(gegede.builder.Builder):
    def configure(self, **kwds):
        if not set(kwds).issubset(globals.Enclosure): # no unknown keywords
            msg = 'Unknown parameter in: "%s"' % (', '.join(sorted(kwds.keys())), )
            raise ValueError(msg)

        # The builder hierarchy takes care of all the configuration parameters
        globals.Enclosure = kwds

    def construct(self, geom):
        detencBox = geom.shapes.Box(self.name,
                                    dx=globals.get("DetEncX"),
                                    dy=globals.get("DetEncY"),
                                    dz=globals.get("DetEncZ"))
        detencLV = geom.structure.Volume('vol'+self.name, material="Air", shape=detencBox)
        self.add_volume(detencLV)

        # get the cryostat volume from the subbuilder and place it
        cryostat = self.get_builder("Cryostat")
        cryostatLV = cryostat.get_volume()
        cryostat_place = geom.structure.Placement('place'+cryostat.name,
                                                  volume = cryostatLV,
                                                  pos = "posCryoInDetEnc")
        detencLV.placements.append(cryostat_place.name)

        # get the outer structure volumes
        foampadblockBox = geom.shapes.Box('FoamPadBlock',
                                          dx=globals.get("Cryostat_x") + 2*globals.get("FoamPadding"),
                                          dy=globals.get("Cryostat_y") + 2*globals.get("FoamPadding"),
                                          dz=globals.get("Cryostat_z") + 2*globals.get("FoamPadding"))
        foampaddingBox = geom.shapes.Boolean('FoamPadding',
                                             type = 'subtraction',
                                             first = foampadblockBox,
                                             second = geom.get_shape(cryostatLV),
                                             pos = "posCenter")
        steelsupportblockBox = geom.shapes.Box('SteelSupportBlock',
                                               dx=globals.get("Cryostat_x")    +    \
                                                  2*globals.get("FoamPadding") +    \
                                                  2*globals.get("SteelSupport_x"),
                                               dy=globals.get("Cryostat_y")    +    \
                                                  2*globals.get("FoamPadding") +    \
                                                  2*globals.get("SteelSupport_y"),
                                               dz=globals.get("Cryostat_z")    +    \
                                                  2*globals.get("FoamPadding") +    \
                                                  2*globals.get("SteelSupport_z"))
        steelsupportBox = geom.shapes.Boolean('SteelSupport',
                                              type = 'subtraction',
                                              first = steelsupportblockBox,
                                              second = foampadblockBox,
                                              pos = "posCenter")

        foampaddingLV = geom.structure.Volume('vol'+foampaddingBox.name,
                                              material = "foam_protoDUNE_RPUF_assayedSample",
                                              shape = foampaddingBox)
        steelsupportLV = geom.structure.Volume('vol'+steelsupportBox.name,
                                              material = "AirSteelMixture",
                                              shape = steelsupportBox)

        # define the placements and put it inside the detector enclosure
        foampadding_place = geom.structure.Placement('place'+foampaddingBox.name,
                                                     volume = foampaddingLV,
                                                     pos = "posCryoInDetEnc")
        steelsupport_place = geom.structure.Placement('place'+steelsupportBox.name,
                                                     volume = steelsupportLV,
                                                     pos = "posCryoInDetEnc")
        detencLV.placements.append(foampadding_place.name)
        detencLV.placements.append(steelsupport_place.name)
        return
