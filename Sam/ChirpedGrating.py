import klayout.db as db
import numpy as np
from datetime import date
today = date.today()

ly = db.Layout()

dose = 1000

heights = [-250, 0, 250]
periods = [0.450, 0.350, 0.450]
ffs = [0.7, 0.7, 0.7, 0.7, 0.7]

# sets the database unit to 1 um, base units seem to be millimeters.
ly.dbu = 0.001
cell_name = f'df{dose}_chirped_ff{ffs[2]}'
top = ly.create_cell(cell_name)
layer0 = ly.layer(0, dose)
layer1 = ly.layer(1, dose)

grating_width = 500



grating_x = 0
grating_y = 0

rotate90 = True

num_of_periods = round(grating_width / max(periods))

x_cen = []
xs = []
ys = []
n = 1

for p, f, h in zip(periods, ffs, heights):
    temp = np.arange(-num_of_periods/2 * p, (num_of_periods/2 * p) + p, p)
    x_cen.append(list(temp))

x_cen = list(np.asarray(x_cen).reshape(len(periods), -1).transpose())

for x_c in x_cen:
    x_c = list(x_c)
    temp_x = []
    temp_y = []
    for p, f, h, xc in zip(periods, ffs, heights, x_c):
        temp_x.append(xc - p/2)
        temp_y.append(h)

    for p, f, h, xc in zip(reversed(periods), reversed(ffs), reversed(heights), reversed(x_c)):
        temp_x.append(xc - p/2 + (p * (1-f)))
        temp_y.append(h)
    xs.append(temp_x)
    ys.append(temp_y)

for x, y in zip(xs, ys):
    pts = []
    for pt in zip(x, y):
        pts.append(db.DPoint(*pt))
    t1 = db.DTrans.R90
    if rotate90:
        top.shapes(layer0).insert(db.DPolygon(pts) * t1)
    else:
        top.shapes(layer0).insert(db.DPolygon(pts))

ly.write(f'{dose}_ChirpedGrating_{today}_PChirp{periods[2]}_{periods[0]}_FFChirp{ffs[2]}_{ffs[0]}.gds')     # 2 Chirps
# ly.write(f'ChirpedGrating_{today}_PChirp{periods[1]}_{periods[0]}_FFChrip{ffs[1]}_{ffs[0]}.gds')   # 3 Chirps