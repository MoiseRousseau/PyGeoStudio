#!/bin/bash

cd basics
python change_anchors_properties.py
python change_saturated_perm.py
python change_timestepping.py

cd ../calibrations
python 1D_unsaturated_column_VG_parameter.py
python rapid_drawdown_basic.py

cd ../datasets
python update_dataset.py

cd ../geometry
python create_region.py

cd ../parametric
python rapid_drawdown_Ksat.py

cd ../results
python export_results.py
python plot_results.py
