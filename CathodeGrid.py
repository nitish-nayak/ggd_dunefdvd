

#!/usr/bin/env python
'''
CathodeGrid builder for DUNE FD-VD
'''

import gegede.builder
from utils import *

class CathodeGridBuilder(gegede.builder.Builder):
    def configure(self, **kwds):
        if not set(kwds).issubset(globals.Cathode): # no unknown keywords
            msg = 'Unknown parameter in: "%s"' % (', '.join(sorted(kwds.keys())), )
            raise ValueError(msg)

        # The builder hierarchy takes care of all the configuration parameters
        globals.Cathode = kwds

    def constructGrid(geom, cblock, cvoid, ny=4, nz=4):
        # recursively step through a 4x4 grid
        py = (2.5-ny)*globals.get("widthCathodeVoid") + (2.0-ny + (ny<2))*globals.get("CathodeBorder")
        pz = (2.5-nz)*globals.get("widthCathodeVoid") + (2.0-nz + (nz<2))*globals.get("CathodeBorder")
        posij = geom.structure.Position('posCathodeSub'+str((5-ny)*(5-nz)),
                                        x = 0,
                                        y = py,
                                        z = pz)
        cij = geom.shapes.Boolean('Cathode'+str((5-ny)*(5-nz)),
                                  type = 'subtraction',
                                  first = cblock,
                                  second = cvoid,
                                  pos = posij.name)
        if ny == 1 and nz == 1:
            cij.name = 'CathodeGrid'
            return cij
        elif nz == 1:
            cij = constructGrid(geom, cij, cvoid, ny-1, 4)
        else:
            cij = constructGrid(geom, cij, cvoid, ny, nz-1)

    def construct(self, geom):
        cathodeblockBox = geom.shapes.Box('CathodeBlock',
                                          dx=globals.get("heightCathode"),
                                          dy=globals.get("widthCathode"),
                                          dz=globals.get("lengthCathode"))
        cathodevoidBox = geom.shapes.Box('CathodeVoid',
                                          dx=globals.get("heightCathode") + Q('1.0cm'),
                                          dy=globals.get("widthCathodeVoid"),
                                          dz=globals.get("lengthCathodeVoid"))

        cathodegridBox = constructGrid(geom, cathodeblockBox, cathodevoidBox)
        cathodegridLV = geom.structure.Volume('vol'+cathodegridBox.name,
                                              material = "G10",
                                              shape = cathodegridBox)
        self.add_volume(cathodegridLV)
        return
