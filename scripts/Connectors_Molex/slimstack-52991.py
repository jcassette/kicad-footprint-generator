#!/usr/bin/env python

# KicadModTree is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# KicadModTree is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with kicad-footprint-generator. If not, see < http://www.gnu.org/licenses/ >.
#
# (C) 2016 by Thomas Pointhuber, <thomas.pointhuber@gmx.at>

import sys
import os
import argparse

sys.path.append(os.path.join(sys.path[0], "../.."))  # enable package import from parent directory

from KicadModTree import *  # NOQA


def round_to(n, precision):
    correction = 0.5 if n >= 0 else -0.5
    return int( n/precision+correction ) * precision


if __name__ == '__main__':

    # handle arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('pincount', help='number of pins of the connector', type=int, nargs=1)
    parser.add_argument('partnumber', help='suffix to 52991 series number (e.g. 0200)', type=str, nargs=1)
    parser.add_argument('-v', '--verbose', help='show extra information while generating the footprint', action='store_true')
    args = parser.parse_args()
    pincount = int(args.pincount[0])
    partnumber = str(args.partnumber[0])
    footprint_name = 'Molex_SlimStack_Receptacle_2x{pc:02g}_Pitch0.5mm_52991-{pn:s}'.format(pc=pincount/2, pn=partnumber)
    print('Building {:s} '.format(footprint_name))

    # calculate working values
    pad_x_spacing = 0.5
    pad_y_spacing = 2.2 + 1.8
    pad_width = 0.3
    pad_height = 1.8
    pad_x_span = (pad_x_spacing * ((pincount / 2) - 1))

    h_body_width = 4.3 / 2.0
    h_body_length = (pad_x_span / 2.0) + 2.15 + 0.35

    tab_width = 1.3
    tab_height = 0.5

    fab_width = 0.1

    outline_x = h_body_length - (pad_x_span / 2.0) - 0.3
    marker_y = 0.8
    silk_width = 0.12
    nudge = 0.15

    courtyard_width = 0.05
    courtyard_precision = 0.01
    courtyard_clearance = 0.5
    courtyard_x = round_to(h_body_length + courtyard_clearance, courtyard_precision)
    courtyard_y = round_to((pad_y_spacing + pad_height) / 2.0 + courtyard_clearance, courtyard_precision)

    label_x_offset = 0
    label_y_offset = courtyard_y + 0.7

    # initialise footprint
    kicad_mod = Footprint(footprint_name)
    kicad_mod.setDescription('Molex SlimStack receptacle, 02x{pc:02g} contacts 0.5mm pitch 4mm height, http://www.molex.com/pdm_docs/sd/529910408_sd.pdf'.format(pc=pincount/2))
    kicad_mod.setTags('connector molex slimstack 52991-{:s}'.format(partnumber))
    kicad_mod.setAttribute('smd')

    # set general values
    kicad_mod.append(Text(type='reference', text='REF**', size=[1,1], at=[label_x_offset, -label_y_offset], layer='F.SilkS'))
    kicad_mod.append(Text(type='user', text='%R', size=[1,1], at=[0, 0], layer='F.Fab'))
    kicad_mod.append(Text(type='value', text=footprint_name, at=[label_x_offset, label_y_offset], layer='F.Fab'))

    # create pads
    kicad_mod.append(PadArray(pincount=pincount//2, x_spacing=pad_x_spacing, y_spacing=0,\
        center=[0,-pad_y_spacing/2.0], initial=1, increment=2, type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT, size=[pad_width, pad_height],\
        layers=Pad.LAYERS_SMT))
    kicad_mod.append(PadArray(pincount=pincount//2, x_spacing=pad_x_spacing, y_spacing=0,\
        center=[0,pad_y_spacing/2.0], initial=2, increment=2, type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT, size=[pad_width, pad_height],\
        layers=Pad.LAYERS_SMT))

    # create fab outline and pin 1 marker
    kicad_mod.append(RectLine(start=[-h_body_length, -h_body_width], end=[h_body_length, h_body_width], layer='F.Fab', width=fab_width))
    kicad_mod.append(Line(start=[-h_body_length+outline_x, -h_body_width-nudge], end=[-h_body_length+outline_x, -h_body_width-marker_y], layer='F.Fab', width=fab_width))

    # create silkscreen outline and pin 1 marker
    left_outline = [[-h_body_length+outline_x, h_body_width+nudge], [-h_body_length-nudge, h_body_width+nudge], [-h_body_length-nudge, -h_body_width-nudge],\
                    [-h_body_length+outline_x, -h_body_width-nudge], [-h_body_length+outline_x, -h_body_width-marker_y]]
    right_outline = [[h_body_length-outline_x, h_body_width+nudge], [h_body_length+nudge, h_body_width+nudge], [h_body_length+nudge, -h_body_width-nudge],\
                     [h_body_length-outline_x, -h_body_width-nudge]]
    top_left_tab = [[-h_body_length-nudge, -h_body_width-nudge], [-h_body_length-nudge, -h_body_width-nudge-tab_height],\
                    [-h_body_length-nudge+tab_width, -h_body_width-nudge-tab_height], [-h_body_length-nudge+tab_width, -h_body_width-nudge]]
    bottom_left_tab = [[-h_body_length-nudge, h_body_width+nudge], [-h_body_length-nudge+tab_width/3, h_body_width+nudge+tab_height],\
                       [-h_body_length-nudge+tab_width, h_body_width+nudge+tab_height], [-h_body_length-nudge+tab_width, h_body_width+nudge]]
    top_right_tab = [[h_body_length+nudge, -h_body_width-nudge], [h_body_length+nudge, -h_body_width-nudge-tab_height],\
                     [h_body_length+nudge-tab_width, -h_body_width-nudge-tab_height], [h_body_length+nudge-tab_width, -h_body_width-nudge]]
    bottom_right_tab = [[h_body_length+nudge, h_body_width+nudge], [h_body_length+nudge, h_body_width+nudge+tab_height],\
                       [h_body_length+nudge-tab_width, h_body_width+nudge+tab_height], [h_body_length+nudge-tab_width, h_body_width+nudge]]
    kicad_mod.append(PolygoneLine(polygone=left_outline, layer='F.SilkS', width=silk_width))
    kicad_mod.append(PolygoneLine(polygone=right_outline, layer='F.SilkS', width=silk_width))
    kicad_mod.append(PolygoneLine(polygone=top_left_tab, layer='F.SilkS', width=silk_width))
    kicad_mod.append(PolygoneLine(polygone=bottom_left_tab, layer='F.SilkS', width=silk_width))
    kicad_mod.append(PolygoneLine(polygone=top_right_tab, layer='F.SilkS', width=silk_width))
    kicad_mod.append(PolygoneLine(polygone=bottom_right_tab, layer='F.SilkS', width=silk_width))

    # create courtyard
    kicad_mod.append(RectLine(start=[-courtyard_x, -courtyard_y], end=[courtyard_x, courtyard_y], layer='F.CrtYd', width=courtyard_width))

    # add model
    kicad_mod.append(Model(filename="${{KISYS3DMOD}}/Connectors_Molex.3dshapes/{:s}.wrl".format(footprint_name), at=[0, 0, 0], scale=[1, 1, 1], rotate=[0, 0, 0]))

    # print render tree
    if args.verbose:
        print(kicad_mod.getRenderTree())

    # write file
    file_handler = KicadFileHandler(kicad_mod)
    file_handler.writeFile('{:s}.kicad_mod'.format(footprint_name))

