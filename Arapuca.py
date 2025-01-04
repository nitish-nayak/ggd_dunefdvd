#!/usr/bin/env python
'''
Arapuca builder for DUNE FD-VD
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

    def construct(self, geom):
        # define all the shapes
        a_out = (globals.get("ArapucaOut_x"), globals.get("ArapucaOut_y"), globals.get("ArapucaOut_z"))
        a_acc = (globals.get("ArapucaAcceptanceWindow_x"),
                 globals.get("ArapucaAcceptanceWindow_y"),
                 globals.get("ArapucaAcceptanceWindow_z"))

        arapucaOutBox = geom.shapes.Box('ArapucaOut',
                                        dx = a_out[0],
                                        dy = a_out[1],
                                        dz = a_out[2])
        arapucaOutShortLatBox = geom.shapes.Box('ArapucaOutShortLat',
                                                dx = a_out[0],
                                                dy = a_out[2],
                                                dz = a_out[1])
        arapucaOutCathodeBox = geom.shapes.Box('ArapucaOutCathode',
                                               dx = a_out[1],
                                               dy = a_out[2],
                                               dz = a_out[0])
        arapucaInBox = geom.shapes.Box('ArapucaIn',
                                       dx = globals.get("ArapucaIn_x"),
                                       dy = a_out[1],
                                       dz = globals.get("ArapucaIn_z"))
        arapucaWallsBox = geom.shapes.Boolean('ArapucaWalls',
                                              type = 'subtraction',
                                              first = arapucaOutBox,
                                              second = arapucaInBox,
                                              pos = geom.structure.Position('posArapucaSub',
                                                                            x = Q('0cm'),
                                                                            y = 0.5*a_out[1],
                                                                            z = Q('0cm'))
                                              )

        arapucaAccBox = geom.shapes.Box('ArapucaAcceptanceWindow',
                                        dx = a_acc[0],
                                        dy = a_acc[1],
                                        dz = a_acc[2])
        arapucaAccShortLatBox = geom.shapes.Box('ArapucaAcceptanceWindowShortLat',
                                                dx = a_acc[0],
                                                dy = a_acc[2],
                                                dz = a_acc[1])
        arapucaAccCathodeBox = geom.shapes.Box('ArapucaAcceptanceWindowCathode',
                                               dx = a_acc[1],
                                               dy = a_acc[2],
                                               dz = a_acc[0])
        arapucaDoubleInBox = geom.shapes.Box('ArapucaDoubleIn',
                                             dx = globals.get("ArapucaIn_x"),
                                             dy = a_out[1] + Q('1.0cm'),
                                             dz = globals.get("ArapucaIn_z"))
        arapucaDoubleWallsBox = geom.shapes.Boolean('ArapucaDoubleWalls',
                                                    type = 'subtraction',
                                                    first = arapucaOutBox,
                                                    second = arapucaDoubleInBox,
                                                    pos = geom.structure.Position('posArapucaDoubleSub',
                                                                                  x = Q('0cm'),
                                                                                  y = Q('0cm'),
                                                                                  z = Q('0cm'))
                                                    )
        arapucaDoubleAccBox = geom.shapes.Box('ArapucaDoubleAcceptanceWindow',
                                              dx = a_out[1] - Q('0.02cm'),
                                              dy = a_acc[0],
                                              dz = a_acc[2])
        arapucaCathodeAccBox = geom.shapes.Box('ArapucaCathodeAcceptanceWindow',
                                               dx = a_acc[1],
                                               dy = a_acc[0],
                                               dz = a_acc[2])

        # define all the sub-volumes
        opdetsens_LV = geom.structure.Volume('volOpDetSensitive',
                                             material = "LAr",
                                             shape = arapucaAccBox)
        opdetsenslonglat_LV = geom.structure.Volume('volOpDetSensitiveLongLat',
                                                    material = "LAr",
                                                    shape = arapucaAccBox)
        opdetsenssholat_LV = geom.structure.Volume('volOpDetSensitiveShortLat',
                                                   material = "LAr",
                                                   shape = arapucaAccShortLatBox)
        opdetsenscathode_LV = geom.structure.Volume('volOpDetSensitiveCathode',
                                                    material = "LAr",
                                                    shape = arapucaAccCathodeBox)
        main_arapuca_LV = geom.structure.Volume('Arapuca',
                                           material = "G10",
                                           shape = arapucaWallsBox)
        # define the larger volumes
        arapucaout_LV = geom.structure.Volume('volArapuca',
                                              material = "LAr",
                                              shape = arapucaOutBox)
        arapucalonglat_LV = geom.structure.Volume('volArapucaLongLat',
                                                  material = "LAr",
                                                  shape = arapucaOutBox)
        arapucasholat_LV = geom.structure.Volume('volArapucaShortLat',
                                                 material = "LAr",
                                                 shape = arapucaOutShortLatBox)
        arapucacathode_LV = geom.structure.Volume('volArapucaCathode',
                                                  material = "LAr",
                                                  shape = arapucaOutCathodeBox)
        # add it to the builder
        self.add_volume(arapucaout_LV, arapucalonglat_LV, arapucasholat_LV, arapucacathode_LV)

        # now do the placements for each
        arapucaout_LV     = self.placeArapuca(arapucaout_LV, main_arapuca_LV, opdetsens_LV,
                                              opdet_pos = geom.structure.Position('opdetshift',
                                                                                  x = Q('0cm'),
                                                                                  y = 0.5*a_acc[1],
                                                                                  z = Q('0cm')))
        arapucalonglat_LV = self.placeArapuca(arapucalonglat_LV, main_arapuca_LV, opdetsenslonglat_LV,
                                              opdet_pos = geom.structure.Position('opdetshift',
                                                                                  x = Q('0cm'),
                                                                                  y = 0.5*a_acc[1],
                                                                                  z = Q('0cm')))
        arapucasholat_LV  = self.placeArapuca(arapucasholat_LV, main_arapuca_LV, opdetsenssholat_LV,
                                              opdet_pos = geom.structure.Position('opdetshift',
                                                                                  x = Q('0cm'),
                                                                                  y = Q('0cm'),
                                                                                  z = 0.5*a_acc[1]),
                                              rotArapuca = "rMinus90AboutX")
        arapucacathode_LV = self.placeArapuca(arapucacathode_LV, main_arapuca_LV, opdetsenscathode_LV,
                                              opdet_pos = geom.structure.Position('opdetshift',
                                                                                  x = 0.5*a_acc[1],
                                                                                  y = Q('0cm'),
                                                                                  z = Q('0cm')),
                                              rotArapuca = "rPlus90AboutXPlus90AboutZ")

    # helper for arapuca placements
    def placeArapuca(self, arapuca_LV, main_arapuca_LV, opdet_LV, opdet_pos, rotArapuca="rIdentity"):
        place1 = geom.structure.Placement('placearapuca_in'+arapuca_LV.name,
                                          volume = main_arapuca_LV,
                                          pos = "posCenter",
                                          rot = rotArapuca
                                          )
        place2 = geom.structure.Placement('placeopdet_in'+arapuca_LV.name,
                                          volume = opdet_LV,
                                          pos = opdet_pos,
                                          )
        arapuca_LV.placements.append(place1.name)
        arapuca_LV.placements.append(place2.name)
        return
