#!/bin/bash
cp /home/venkatek/scripts/utilities/charge.py .
python charge.py > bader.out
bader density.cube >> bader.out
cp /home/venkatek/scripts/utilities/bader_data.py .
python bader_data.py >> bader.out

rm charge.py
rm bader_data.py
ls
