#!/usr/bin/env python
'''
World builder for DUNE FD-VD
'''

import gegede.builder
from utils import *

class WorldBuilder(gegede.builder.Builder):
    def __init__(self, name):
        super(WorldBuilder, self).__init__(name)

    def configure(self, **kwds):
        if not set(kwds).issubset(globals.World): # no unknown keywords
            msg = 'Unknown parameter in: "%s"' % (', '.join(sorted(kwds.keys())), )
            raise ValueError(msg)

        globals.World = kwds

    def construct(self, geom):
        # get all the relevant stuff here
        construct_materials(geom)
        construct_definitions(geom)

        # create the world box
        worldBox = geom.shapes.Box(self.name,
                                dx=globals.get("DetEncX")+2*globals.get("RockThickness"),
                                dy=globals.get("DetEncY")+2*globals.get("RockThickness"),
                                dz=globals.get("DetEncZ")+2*globals.get("RockThickness"))

        # put it in the world volume
        worldLV = geom.structure.Volume('vol'+self.name, material=m_dusel_rock, shape=worldBox)
        self.add_volume(worldLV)

        # get the detector enclosure sub-builder
        detenc = self.get_builder("DetEnclosure")
        detencLV = detenc.get_volume()

        # define where it goes inside the world volume
        detenc_pos = geom.structure.Position('pos'+detenc.name,
                                             x = globals.get("OriginXSet"),
                                             y = globals.get("OriginYSet"),
                                             z = globals.get("OriginZSet"))
        detenc_place = geom.structure.Placement('place'+detenc.name,
                                                volume = detencLV,
                                                pos = detenc_pos)

        # place it inside the world volume
        worldLV.placements.append(detenc_place.name)
        return
