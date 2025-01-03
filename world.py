#!/usr/bin/env python
'''
World builder for DUNE FD-VD
'''

import gegede.builder
from utils import *

class WorldBuilder(gegede.builder.Builder):
    def __init__(self, name):
        super(WorldBuilder, self).__init__(name)
        self.params = Params()

    def configure(self, **kwds):
        if not set(kwds).issubset(self.params.World): # no unknown keywords
            msg = 'Unknown parameter in: "%s"' % (', '.join(sorted(kwds.keys())), )
            raise ValueError(msg)

        self.params.World = kwds

    def construct(self, geom):
        # get all the relevant stuff here
        construct_materials(geom)
        construct_definitions(geom)

        # create the world box
        worldBox = geom.shapes.Box(self.name,
                                dx=self.params.get("DetEncX")+2*self.params.get("RockThickness"),
                                dy=self.params.get("DetEncY")+2*self.params.get("RockThickness"),
                                dz=self.params.get("DetEncZ")+2*self.params.get("RockThickness"))

        # put it in the world volume
        worldLV = geom.structure.Volume('vol'+self.name, material=m_dusel_rock, shape=worldBox)
        self.add_volume(worldLV)

        # get the detector enclosure sub-builder
        detenc = self.get_builder("DetEnclosure")
        detencLV = detenc.get_volume()

        # define where it goes inside the world volume
        detenc_pos = geom.structure.Position('pos'+detenc.name,
                                             x = self.params.get("OriginXSet"),
                                             y = self.params.get("OriginYSet"),
                                             z = self.params.get("OriginZSet"))
        detenc_place = geom.structure.Placement('place'+detenc.name,
                                                volume = detencLV,
                                                pos = detenc_pos)

        # place it inside the world volume
        worldLV.placements.append(detenc_place.name)
        return
