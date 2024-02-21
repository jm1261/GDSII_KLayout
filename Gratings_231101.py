# %%
import os
import math
import numpy as np
import klayout.db as db

from pathlib import Path

root = Path().absolute()
out_path = Path(f'{root}/Data')

# %%
writefield_height = 500
writefield_width = 500
chip_height = 15000
chip_width = 15000

# %%
layout = db.Layout()
layout.dbu = 0.001
sample_identifier = "AM8"
top_cell = layout.create_cell(f'{sample_identifier}')

# %%


def makes_bars_cell(layout: object,
                    layer: object,
                    period: float,
                    fill_factor: float,
                    bar_height: float,
                    bar_identifier: str) -> object:
    """
    Create bar cell with the given dimensions.

    Parameters
    ---------
    layout, layer: object
        Database and layer objects from KLayout.
    period, fill_factor, bar_height: float
        Period, fill factor, and height of the bar.
    bar_identifier: string
        Bar cell name.

    Returns
    -------
    bar_cell: object
        Bar cell.

    See Also
    --------
    None

    Notes
    -----
    None

    Example
    -------
    None

    """
    bar_cell = layout.create_cell(f'{bar_identifier}')
    bar_origin = db.DPoint(0, 0)
    bar = db.DBox(
        bar_origin,
        (bar_origin + db.DVector(period * (1 - fill_factor), bar_height)))
    bar_cell.shapes(layer).insert(bar)
    return bar_cell


def makes_hole_cell(layout: object,
                    layer: object,
                    radius: float,
                    number_of_vertices: int,
                    hole_identifier: str) -> object:
    """
    Create hole cell with given dimensions.

    Parameters
    ----------
    layout, layer: object
        Database and layer objects from KLayout.
    radius: float
        Hole radius in database units.
    number_of_vertices: int
        Number of polygon vertices.
    hole_identifier: string
        Hole cell name.
    
    Returns
    -------
    hole_cell: object
        Hole cell.
    
    See Also
    --------
    makes_bars_cell

    Notes
    -----
    None

    Example
    -------
    None

    """
    hole_cell = layout.create_cell(f'{hole_identifier}')
    hole = db.DPolygon.ellipse(
        db.DBox(0 - radius, 0 - radius, 0 + radius, 0 + radius),
        number_of_vertices)
    hole_cell.shapes(layer).insert(hole)
    return hole_cell


def generates_texts(layout: object,
                    layer_index: int,
                    dose: float,
                    text_identifier: str,
                    text_string: str,
                    text_magnification: int):
    """
    Generate text string cell in KLayout.

    Parameters
    ---------
    layout: object
        Database object from KLayout.
    layer_index, text_magnification: int
        KLayout layer number and text size.
    dose: float
        Text layer dose.
    text_identifier, text_string: string
        Text cell name and text to write.

    Returns
    -------
    text_cell: object
        Text cell.

    See Also
    --------
    makes_bars_cell

    Notes
    -----
    None

    Example
    -------
    None

    """
    text_layer = layout.layer(layer_index, dose)
    text_cell = layout.create_cell(f'{text_identifier}')
    generator = db.TextGenerator.default_generator()
    region = generator.text(
        text_string,
        layout.dbu,
        text_magnification)
    text_cell.shapes(text_layer).insert(region)
    return text_cell


def makes_gratings_cell(layout: object,
                        grating_bar: object,
                        period: float,
                        grating_length: float,
                        grating_identifier: str) -> object:
    """
    Create a grating cell with the given bar cell, period, and grating length.

    Parameters
    ----------
    layout, grating_bar: object
        Database and cell objects from KLayout.
    period, grating_length: float
        Period or the grating and grating length in database units.
    grating_identifier: string
        Grating cell name.
    
    Returns
    -------
    grating_cell: object
        Grating cell.
    
    See Also
    --------
    makes_bars_cell

    Notes
    -----
    This makes a 1D grating with a period in X.

    Example
    -------
    None

    """
    grating_cell = layout.create_cell(f'{grating_identifier}')
    x_vector = db.DVector(period, 0)
    num_x = math.floor(grating_length / period)
    y_vector = db.DVector()
    num_y = 1
    grating_cell.insert(
        db.DCellInstArray(
            grating_bar.cell_index(),
            db.DTrans(),
            x_vector,
            y_vector,
            num_x,
            num_y))
    return grating_cell


def makes_nanohole_cell(layout: object,
                        hole_cell: object,
                        period_x: float,
                        period_y: float,
                        grating_length: float,
                        grating_height: float,
                        grating_identifier: str) -> object:
    """
    Create a nanohole cell with the given hole cell, period, and grating length.

    Parameters
    ----------
    layout, grating_bar: object
        Database and cell objects from KLayout.
    period_x, period_y, grating_length, grating_height: float
        Period of the grating and grating length in database units.
    grating_identifier: string
        Grating cell name.
    
    Returns
    -------
    grating_cell: object
        Grating cell.
    
    See Also
    --------
    makes_hole_cell

    Notes
    -----
    This makes a 2D grating with a period in X and Y.

    Example
    -------
    None

    """
    grating_cell = layout.create_cell(f'{grating_identifier}')
    x_vector = db.DVector(period_x, 0)
    num_x = math.floor(grating_length / period_x)
    y_vector = db.DVector(0, period_y)
    num_y = math.floor(grating_height / period_y)
    grating_cell.insert(
        db.DCellInstArray(
            hole_cell.cell_index(),
            db.DTrans(),
            x_vector,
            y_vector,
            num_x,
            num_y))
    return grating_cell


# %%
chip_cell = layout.create_cell('Chip_Outline')
layer_index = 0
layer = layout.layer(layer_index, 0)
chip_bottom = db.DBox(
    db.DPoint(0, 0),
    (db.DPoint(0, 0) + db.DVector(chip_width, - 100)))
chip_left = db.DBox(
    db.DPoint(0, 0),
    (db.DPoint(0, 0) + db.DVector(-100, chip_height)))
chip_right = db.DBox(
    db.DPoint(chip_width, 0),
    (db.DPoint(chip_width, 0) + db.DVector(100, chip_height)))
chip_top = db.DBox(
    db.DPoint(0, chip_height),
    (db.DPoint(0, chip_height) + db.DVector(chip_width, 100)))

# %%
gratings_dictionary = {}

# %%
dose_factors = np.arange(1, 2.1, 1)
periods = range(420, 481, 20)
fill_factors = np.arange(0.6, 0.81, 0.1)
grating_spacing = 500
text_magnification = 100
text_spacing = 50
layer_index = 1
text_layer = layout.layer(len(dose_factors) + 1, 2000)
flat_cell = layout.create_cell('Flat_Gratings')
for i, dose in enumerate(dose_factors):
    layer = layout.layer(layer_index + i, dose * 1000)
    dose_cell = layout.create_cell(f'Flat_df{dose}')
    dose_text_cell = layout.create_cell(f'FlatText_df{dose}')
    for j, ffs in enumerate(fill_factors):
        ff = round(ffs, 1)
        ff_cell = layout.create_cell(f'Flat_df{dose}_ff{ff}')
        ff_text_cell = layout.create_cell(f'FlatText_df{dose}_ff{ff}')
        for k, period in enumerate(periods):
            grating_period = period / 1000  # scale to database units
            grating_identifier = f'{sample_identifier}.flat.{i}.{j}.{k}'
            gratings_dictionary.update(
                {grating_identifier: f'df{dose}_p{period}_ff{ff}'})
            bar_cell = makes_bars_cell(
                layout=layout,
                layer=layer,
                period=grating_period,
                fill_factor=ff,
                bar_height=writefield_height,
                bar_identifier=f'FlatBar_df{dose}_p{period}_ff{ff}')
            grating_cell = makes_gratings_cell(
                layout=layout,
                grating_bar=bar_cell,
                period=grating_period,
                grating_length=writefield_width,
                grating_identifier=(
                    f'FlatGrating_df{dose}_p{period}_ff{ff}'))
            text_cell = generates_texts(
                layout=layout,
                layer_index=len(dose_factors) + 1,
                dose=2000,
                text_identifier=f'FlatText_df{dose}_p{period}_ff{ff}',
                text_string=grating_identifier,
                text_magnification=text_magnification)
            ff_cell.insert(
                db.DCellInstArray(
                    grating_cell.cell_index(),
                    db.DTrans(
                        db.DVector(
                            k * (writefield_width + grating_spacing),
                            0))))
            ff_text_cell.insert(
                db.DCellInstArray(
                    text_cell.cell_index(),
                    db.DTrans(
                        db.DVector(
                            k * (writefield_width + grating_spacing),
                            writefield_height + text_spacing))))
        dose_cell.insert(
            db.DCellInstArray(
                ff_cell.cell_index(),
                db.DTrans(
                    db.DVector(
                        0,
                        j * (writefield_width + grating_spacing)))))
        dose_text_cell.insert(
            db.DCellInstArray(
                ff_text_cell.cell_index(),
                db.DTrans(
                    db.DVector(
                        0,
                        j * (writefield_width + grating_spacing)))))
    flat_cell.insert(
        db.DCellInstArray(
            dose_cell.cell_index(),
            db.DTrans(
                db.DVector(
                    0,
                    i * (
                        (writefield_height * len(fill_factors)) +
                        (grating_spacing * len(fill_factors)))))))
    flat_cell.insert(
        db.DCellInstArray(
            dose_text_cell.cell_index(),
            db.DTrans(
                db.DVector(
                    0,
                    i * (
                        (writefield_height * len(fill_factors)) +
                        (grating_spacing * len(fill_factors)))))))
