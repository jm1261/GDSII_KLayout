# import pya
import klayout.db as db
import math
import numpy as np
from datetime import date
today = date.today()

dose = 1000

### Variables ###
p = np.linspace(0.300,0.600,num=13)
period = [np.round(pl,3) for pl in p]
print(period)
fillfactor = 0.3

### Layout ###
length = 10
height = 10
y1 = 0
y2 = 20
y3 = 40
offset_from_origin = [0, 20, 40, 60, 
                      80, 100, 120, 140, 
                      160, 180, 200, 220, 240]

ly = db.Layout()
cell_name = f'df{dose}_{length}um_ff{fillfactor}'
top_cell = ly.create_cell(cell_name)
layer = ly.layer(1, dose)
l2 = ly.layer(2, dose)
l3 = ly.layer(3, dose)

for per, off in zip(period[:4], offset_from_origin):
    n1 = math.floor(length / per)
    for i in range(0, n1):
        pt = db.DPoint((i * per)+off, y3)
        box = db.DBox(pt, pt + db.DVector(per * fillfactor, height))

        top_cell.shapes(layer).insert(box)
            
    for per, off in zip(period[4:8], offset_from_origin):
        n2 = math.floor(length / per)
        for i in range(0, n2):
            pt = db.DPoint((i * per)+off, y2)
            box = db.DBox(pt, pt + db.DVector(per * fillfactor, height))

            top_cell.shapes(layer).insert(box)
            
    for per, off in zip(period[8:], offset_from_origin):
        n3 = math.floor(length / per)
        for i in range(0, n3):
            pt = db.DPoint((i * per)+off, y1)
            box = db.DBox(pt, pt + db.DVector(per * fillfactor, height))

            top_cell.shapes(layer).insert(box)
        
x_text = [5, 25, 45, 65, 5, 25, 45, 65, 5, 25, 45, 65, 85]
y_text = [51, 51, 51, 51, 31, 31, 31, 31, 11, 11, 11, 11, 11]

for index, (x, y) in enumerate(zip(x_text,y_text)):
    x = x - 5
    mag = 1
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

ly.write(f'{dose}_10um_Period_Sweep_GMR_P{period[0]}_FF{period[-1]}_FF{fillfactor}um_{today}.gds')
# ly.write(f'test.gds')