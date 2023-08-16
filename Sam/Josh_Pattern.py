# import pya
import klayout.db as db
import math
import numpy as np
from datetime import date
import os
today = date.today()

root = os.getcwd()
print(root)

dose = 1000

### Variables ###
p = np.linspace(0.300,0.600,num=13)
period = [np.round(pl,3) for pl in p]
print(period)
fillfactor = 0.3

### Layout ###
length = 500
height = 500
y = 0
offset_from_origin = [0, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000, 11000, 12000]

ly = db.Layout()
cell_name = f'df{dose}_{length}um_ff{fillfactor}'
top_cell = ly.create_cell(cell_name)
layer = ly.layer(1, dose)
l2 = ly.layer(2, dose)
l3 = ly.layer(3, dose)


for per, off in zip(period, offset_from_origin):
    n = math.floor(length / per)
    for i in range(0, n):
        pt = db.DPoint((i * per)+off, y)
        box = db.DBox(pt, pt + db.DVector(per * fillfactor, height))

        top_cell.shapes(layer).insert(box)
            
    # for per, off in zip(period[5:], offset_from_origin):
    #     for i in range(0, n):
    #         pt = db.DPoint((i * per)+off, 500)
    #         box = db.DBox(pt, pt + db.DVector(per * fillfactor, height))

    #         top_cell.shapes(layer).insert(box)
        
x_text = [0, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000, 11000, 12000]
y_text = [600, 600, 600, 600, 600, 600, 600, 600, 600, 600, 600, 600, 600]

for index, (x, y) in enumerate(zip(x_text,y_text)):
    mag = 50
    gen = db.TextGenerator.default_generator()
    region = gen.text(f'P{np.round(period[index],4)}um, FF{fillfactor}', ly.dbu, mag)
    top_cell.shapes(l2).insert(region, db.DTrans(db.DVector(x, y)))

# ### Alignment Markers ###
# x0 = 0
# y0 = 0
# x1 = 50
# y1= 50
# offsety = 2200
# offsetx = 5500

# top_cell.shapes(l3).insert(db.DBox(x0, y0, x1, y1))                                  # BL
# top_cell.shapes(l3).insert(db.DBox(x0, y0+offsety, x1, y1+offsety))                  # TL 
# top_cell.shapes(l3).insert(db.DBox(x0+100, y0+offsety, x1+100, y1+offsety))          # TL
# top_cell.shapes(l3).insert(db.DBox(x0+offsetx, y0+offsety, x1+offsetx, y1+offsety))  # TR
# top_cell.shapes(l3).insert(db.DBox(x0+offsetx, y0, x1+offsetx, y1))                  # BR

ly.write(f'{dose}_Period_Sweep_GMR_P{period[0]}_FF{period[-1]}_FF{fillfactor}um_{today}.gds')
# ly.write(f'test.gds')