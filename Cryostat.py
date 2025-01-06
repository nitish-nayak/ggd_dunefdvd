#!/usr/bin/env python
'''
Cryostat builder for DUNE FD-VD
'''

import gegede.builder
from utils import *
import re

class CryostatBuilder(gegede.builder.Builder):
    def configure(self, **kwds):
        if not set(kwds).issubset(globals.Cryostat): # no unknown keywords
            msg = 'Unknown parameter in: "%s"' % (', '.join(sorted(kwds.keys())), )
            raise ValueError(msg)

        # The builder hierarchy takes care of all the configuration parameters
        globals.Cryostat = kwds

    # a number of placement helpers for cryostat and other constituent volumes
    def placeCathodeAndAnode(self, geom, c_LV, a_LV, tpcenc_LV):
        if not globals.get("Cathode_switch"):
            return

        cathode_x = 0.5*globals.get("TPCEnclosure_x") - globals.get("TPC_x") -                                      \
                    globals.get("anodePlateWidth") - 0.5*globals.get("heightCathode")
        cathode_y = -0.5*globals.get("TPCEnclosure_y") + 0.5*globals.get("widthCathode")
        cathode_z = -0.5*globals.get("TPCEnclosure_z") + 0.5*globals.get("lengthCathode")
        anode_toppos = 0.5*globals.get("TPCEnclosure_x") - 0.5*globals.get("anodePlateWidth")
        anode_botpos = -0.5*globals.get("TPCEnclosure_x") + 0.5*globals.get("anodePlateWidth")

        idx = 0
        for ii in range(globals.get("nCRM_z")//2):
            for jj in range(globals.get("nCRM_y")//2):
                name_c = re.sub(r'vol', '', c_LV.name)
                name_a = re.sub(r'vol', '', a_LV.name)
                place_c = geom.structure.Placement('place%s%d_inTPCEnc'%(c_LV.name, idx),
                                                   volume = c_LV,
                                                   pos = geom.structure.Position('pos%s-%d'%(name_c, idx),
                                                                                 x = cathode_x,
                                                                                 y = cathode_y,
                                                                                 z = cathode_z))
                place_a = geom.structure.Placement('place%s%d_inTPCEnc'%(a_LV.name, idx),
                                                   volume = a_LV,
                                                   pos = geom.structure.Position('pos%s-%d'%(name_a, idx),
                                                                                 x = anode_toppos,
                                                                                 y = cathode_y,
                                                                                 z = cathode_z),
                                                   rot = "rIdentity")
                tpcenc_LV.placements.append(place_c.name)
                tpcenc_LV.placements.append(place_a.name)

                if globals.get("nCRM_x") == 2:
                    place_ab = geom.structure.Placement('place%s%d_inTPCEncBottom'%(name_a, idx),
                                                        volume = a_LV,
                                                        pos = geom.structure.Position('pos%sBottom-%d' %            \
                                                                                            (name_a, idx),
                                                                                      x = anode_botpos,
                                                                                      y = cathode_y,
                                                                                      z = cathode_z),
                                                        rot = "rIdentity")
                    tpcenc_LV.placements.append(place_ab.name)

                idx += 1
                cathode_y += globals.get("widthCathode")
            cathode_z += globals.get("lengthCathode")
            cathode_y = -0.5*globals.get("TPCEnclosure_y") + 0.5*globals.get("widthCathode")
        return

    # upstream logic needed for arapuca vs arapurca double passed as argument
    def placeOpDetsCathode(self, geom, arapuca_LV, tpcenc_LV):
        if globals.get("pdsconfig"):
            return
        frCenter_x = 0.5*globals.get("TPCEnclosure_x") - globals.get("TPC_x") -                                     \
                     globals.get("anodePlateWidth") - 0.5*globals.get("heightCathode")
        frCenter_y = -0.5*globals.get("TPCEnclosure_y") + 0.5*globals.get("widthCathode")
        frCenter_z = -0.5*globals.get("TPCEnclosure_z") + 0.5*globals.get("lengthCathode")

        idx = 0
        for ii in range(globals.get("nCRM_y")//2):
            for jj in range(globals.get("nCRM_z")//2):
                for ara in range(4):
                    ara_x = frCenter_x
                    ara_y = frCenter_y + globals.get("list_posy_bot")[ara]
                    ara_z = frCenter_z + globals.get("list_posz_bot")[ara]

                    if jj == 0 and ara == 1:
                        ara_z = frCenter_z + globals.get("list_posz_bot")[0]
                    if jj == globals.get("nCRM_z")//2 - 1 and ara == 2:
                        ara_z = frCenter_z + globals.get("list_posz_bot")[3]
                    if ii == 0 and ara == 0:
                        ara_y = frCenter_y + globals.get("list_posy_bot")[2]
                    if ii == globals.get("nCRM_y")//2 - 1 and ara == 3:
                        ara_y = frCenter_y + globals.get("list_posy_bot")[1]

                    name = re.sub(r'vol', '', arapuca_LV.name)
                    place = geom.structure.Placement('place%sAra%d-%d_inTPCEnc'%(name, ara, idx),
                                                     volume = arapuca_LV,
                                                     pos = geom.structure.Position('pos%s%d-Frame-%d-%d' %          \
                                                                                    (name, ara, ii, jj),
                                                                                    x = ara_x,
                                                                                    y = ara_y,
                                                                                    z = ara_z),
                                                     rot = "rPlus90AboutXPlus90AboutZ")
                    tpcenc_LV.placements.append(place.name)
                idx += 1
                frCenter_z += globals.get("lengthCathode")
            frCenter_y += globals.get("widthCathode")
            frCenter_z = -0.5*globals.get("TPCEnclosure_z") + 0.5*globals.get("lengthCathode")
        return

    def placeFieldShaper(self, geom, fs_LV, fsslim_LV, cryo_LV):
        if not globals.get("FieldCage_switch"):
            return
        reversed = 0 if globals.get("nCRM_x") != 2 else 1
        pos_y = -0.5*globals.get("FieldShaperShortTubeLength") - globals.get("FieldShaperTorRad")
        pos_z = Q('0cm')

        for i in range(globals.get("NFieldShapers")):
            dist = i*globals.get("FieldShaperSeparation")
            pos_x = 0.5*globals.get("Argon_x") - globals.get("HeightGaseousAr") -                                   \
                    (globals.get("driftTPCActive") + globals.get("ReadoutPlane")) +                                 \
                    (i + 0.5)*globals.get("FieldShaperSeparation")
            if reversed:
                pos_x = 0.5*globals.get("Argon_x") - globals.get("HeightGaseousAr") -                               \
                        (globals.get("driftTPCActive") + globals.get("ReadoutPlane")) -                             \
                        globals.get("heightCathode") -                                                              \
                        (i + 0.5)*globals.get("FieldShaperSeparation")

            name = re.sub(r'vol', '', fs_LV.name)
            if (globals.get("pdsconfig") == 0 and dist <= Q('250cm')):
                place = geom.structure.Placement('place%s%d_inCryo' % (fs_LV.name, i),
                                                 volume = fs_LV,
                                                 pos = geom.structure.Position('pos%s_%d%d' %                       \
                                                                                 (name, int(reversed), i),
                                                                               x = pos_x,
                                                                               y = pos_y,
                                                                               z = pos_z),
                                                 rot = "rPlus90AboutZ")
                cryo_LV.placements.append(place.name)
            else:
                place_slim = geom.structure.Placement('place%s%d_inCryo' % (fsslim_LV.name, i),
                                                      volume = fsslim_LV,
                                                      pos = geom.structure.Position('pos%s_%d%d' %                  \
                                                                                      (name, int(reversed), i),
                                                                                    x = pos_x,
                                                                                    y = pos_y,
                                                                                    z = pos_z),
                                                      rot = "rPlus90AboutZ")
                cryo_LV.placements.append(place_slim.name)
        return

    def placeOpDetsLateral(self, geom, arapuca_LV, cryo_LV):
        if (globals.get("pdsconfig") != 0 or globals.get("nCRM_y") != 8):
            return
        frCenter_x = 0.5*globals.get("Argon_x") - globals.get("HeightGaseousAr") -                                  \
                     0.5*globals.get("padWidth")
        frCenter_z = -19*0.5*globals.get("lengthCathode") +                                                         \
                     (40 - globals.get("nCRM_z")*0.25*globals.get("lengthCathode"))

        name = re.sub(r'vol', '', arapuca_LV.name)
        for j in range(globals.get("nCRM_z")//2):
            for ara in range(8*globals.get("nCRM_x")):

                ara_z = frCenter_z
                ara_x = frCenter_x - globals.get("FirstFrameVertDist")
                if ara >= 8:
                    ara_x = -ara_x - globals.get("HeightGaseousAr") + globals.get("xLArBuffer")
                if ara % 4 != 0:
                    ara_x -= globals.get("VerticalPDdist") if ara < 8 else -globals.get("VerticalPDdist")

                ara_y = 0.5*globals.get("Argon_y") - globals.get("FrameToArapucaSpaceLat")
                delta_sens = -0.5*globals.get("ArapucaOut_y") +                                                     \
                             0.5*globals.get("ArapucaAcceptanceWindow_y") + Q('0.01cm')
                ara_ysens = ara_y + delta_sens
                rotation = "rPlus180AboutX"

                if ara % 8 < 4:
                    ara_y = -ara_y
                    ara_ysens = ara_y - delta_sens
                    rotation = "rIdentity"

                place_lat = geom.structure.Placement('place%s%d-Lat%d' % (name, ara, j),
                                                     volume = arapuca_LV,
                                                     pos = geom.structure.Position('pos%s%d-Lat%d' %                \
                                                                                        (name, ara, j),
                                                                                   x = ara_x,
                                                                                   y = ara_y,
                                                                                   z = ara_z),
                                                     rot = rotation)
                cryo_LV.placements.append(place_lat.name)
            frCenter_z += globals.get("lengthCathode")
        return

    def placeOpDetsShortLateral(self, geom, arapuca_LV, cryo_LV):
        if (globals.get("pdsconfig") != 0 or globals.get("nCRM_y") != 8):
            return
        frCenter_x = 0.5*globals.get("Argon_x") - globals.get("HeightGaseousAr") -                                  \
                     0.5*globals.get("padWidth")
        frCenter_z = -19*0.5*globals.get("lengthCathode") +                                                         \
                     (40 - globals.get("nCRM_z")*0.25*globals.get("lengthCathode"))

        name = re.sub(r'vol', '', arapuca_LV.name)
        for j in range(2):
            frCenter_y = Q('220cm') if j else Q('-220cm')
            for ara in range(8*globals.get("nCRM_x")):

                ara_x = frCenter_x - globals.get("FirstFrameVertDist")
                if ara >= 8:
                    ara_x = -ara_x - globals.get("HeightGaseousAr") + globals.get("xLArBuffer")
                if ara % 4 != 0:
                    ara_x -= globals.get("VerticalPDdist") if ara < 8 else -globals.get("VerticalPDdist")
                ara_y = frCenter_y

                ara_z = 0.5*globals.get("Argon_z") - globals.get("FrameToArapucaSpaceLat")
                delta_sens = -0.5*globals.get("ArapucaOut_z") +                                                     \
                             0.5*globals.get("ArapucaAcceptanceWindow_z") + Q('0.01cm')
                ara_zsens = ara_z + delta_sens
                rotation = "rPlus90AboutX"

                if ara % 8 < 4:
                    ara_z = -ara_z
                    ara_zsens = ara_z - delta_sens
                    rotation = "rMinus90AboutX"

                place_lat = geom.structure.Placement('place%s%d-ShortLat%d' % (name, ara, j),
                                                     volume = arapuca_LV,
                                                     pos = geom.structure.Position('pos%s%d-ShortLat%d' %           \
                                                                                        (name, ara, j),
                                                                                   x = ara_x,
                                                                                   y = ara_y,
                                                                                   z = ara_z),
                                                     rot = rotation)
                cryo_LV.placements.append(place_lat.name)
        return

    def placeOpDetsMembOnly(self, geom, arapuca_LV, cryo_LV):
        if (globals.get("pdsconfig") != 1 or globals.get("nCRM_y") != 8):
            return

        frCenter_x = 0.5*globals.get("TPC_x") - 0.5*globals.get("padWidth")
        frCenter_z = -19*0.5*globals.get("lengthCathode") +                                                         \
                     (40 - globals.get("nCRM_z")*0.25*globals.get("lengthCathode"))

        name = re.sub(r'vol', '', arapuca_LV.name)
        for j in range(globals.get("nCRM_z")//2):
            for ara in range(18):

                ara_z = frCenter_z
                ara_x = frCenter_x - 0.5*globals.get("ArapucaOut_x")
                if ara != 0 and ara != 9:
                    ara_x -= globals.get("ArapucaOut_x") - globals.get("FrameToArapucaSpace")

                ara_y = 0.5*globals.get("Argon_y") - globals.get("FrameToArapucaSpaceLat")
                delta_sens = -0.5*globals.get("ArapucaOut_y") +                                                     \
                             0.5*globals.get("ArapucaAcceptanceWindow_y") + Q('0.01cm')
                ara_ysens = ara_y + delta_sens
                rotation = "rPlus180AboutX"

                if ara < 9:
                    ara_y = -ara_y
                    ara_ysens = ara_y - delta_sens
                    rotation = "rIdentity"

                place_lat = geom.structure.Placement('place%s%d-Lat%d' % (name, ara, j),
                                                     volume = arapuca_LV,
                                                     pos = geom.structure.Position('pos%s%d-Lat%d' %                \
                                                                                        (name, ara, j),
                                                                                   x = ara_x,
                                                                                   y = ara_y,
                                                                                   z = ara_z),
                                                     rot = rotation)
                cryo_LV.placements.append(place_lat.name)
            frCenter_z += globals.get("lengthCathode")
        return

