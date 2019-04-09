#!/usr/bin/env bash

python /tmp/pdf_table_to_dataframe.py --pdf $1
cd /tmp/working/
python /tmp/pdf_table_to_dataframe.py --gs
python /tmp/pdf_table_to_dataframe.py --tess
python /tmp/pdf_table_to_dataframe.py --csv
