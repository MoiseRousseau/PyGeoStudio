#!/bin/bash

cd basics
python change_anchors_properties.py > /dev/null
python change_saturated_perm.py

cd ../calibrations
python 1D_unsaturated_column_VG_parameter.py
python rapid_drawdown_basic.py

cd ../geometry
python create_region.py

cd ../parametric
python rapid_drawdown_Ksat.py

cd ../results
python export_results.py
python plot_results.py
