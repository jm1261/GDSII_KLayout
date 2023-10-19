import math
import klayout.db as db

ly = db.Layout()
layer = ly.layer(1, 0)

top_cell = ly.create_cell("TOP")

width = 1.0
height = 10.0
length = 100.0

bar = ly.create_cell("BAR")
bar.shapes(layer).insert(db.DBox(0, 0, width, height))


def make_grating_cell(ly, bar, pitch, length):
    """
    This function creates a grating cell  with the given 
    bar cell and with the given pitch and length.
    """

    # Note: KLayout will create a unique name itself:
    grating = ly.create_cell("GRATING")

    a = db.DVector(pitch, 0)
    na = math.floor(length / pitch)

    b = db.DVector()  # not used
    nb = 1

    grating.insert(db.DCellInstArray(
        bar.cell_index(),
        db.DTrans(),
        a, b, na, nb))

    return grating


y = 0.0
pitch = 2.0

#for pitch in [2.0, 2.5, 3.0]
grating = make_grating_cell(ly, bar, pitch, length)
top_cell.insert(db.DCellInstArray(grating.cell_index(), db.DTrans(db.DVector(0, y))))

#    y += height * 1.5

ly.write("gratings_hierarchical.gds")
