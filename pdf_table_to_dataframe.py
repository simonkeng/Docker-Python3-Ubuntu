'''
Extract tables from PDFs and convert to pandas DataFrames 
'''

import os, sys, re
import subprocess as sp
import argparse
from PyPDF2 import PdfFileWriter, PdfFileReader
import pandas as pd
import tabula

### Arg Parser ###

parser = argparse.ArgumentParser()

parser.add_argument('--pdf', 
                    help='non-OCR input PDF file.')
parser.add_argument('--gs', 
                    help='Run GhostScript on each PDF to convert to TIFF.',
                    action="store_true")
parser.add_argument('--tess',
                    help='Run tesseract to OCR each TIFF image.',
                    action="store_true")
parser.add_argument('--csv',
                    help='Use tabula to generate DataFrame, write CSV with pandas.',
                    action="store_true")

### Funcs ###

def fname_ends_with_number(fname):
    '''
    Detect files with endings that 
    look like "-#-tmp.pdf"
    '''
    return bool(re.search(r'\w-\d+-tmp.pdf', fname))

def chop(pdf):
    '''
    Chop up PDF by page
    '''
    input_pdf = PdfFileReader(open(pdf, 'rb'))
    outfile = pdf.split('.')[0]

    for i in range(input_pdf.numPages):
        output = PdfFileWriter()
        output.addPage(input_pdf.getPage(i))
        with open(f'{outfile}-{i}-tmp.pdf', 'wb') as output_stream:
            output.write(output_stream)

def run_gs(pdf):
    '''
    Run simple, single arg shell script to convert PDF to TIFF
    '''
    shell_script = os.path.dirname(__file__) + '/pdf_to_tiff.sh'

    if fname_ends_with_number(pdf):
        sp.call([shell_script, pdf])

def run_tesseract(tiff):
    '''
    Run tesseract 
    '''
    outfile = tiff.split('.')[0] + '-ocr'
    sp.call(['tesseract', tiff, outfile, 'pdf'])

def pdf_to_csv():
    '''
    Run tabula to generate dataframes, saved as CSVs
    '''

    for file in os.listdir(os.getcwd()):

        if file.endswith('-tmp-ocr.pdf'):

            print(f'On file: {file}')
            df = tabula.read_pdf(file, multiple_tables=True)

            outfile = file.split('-tmp-')[0]

            try:
                df.to_csv(f'{outfile}.csv', index=False)
            except AttributeError as err:
                for i, single_df in enumerate(df):
                    single_df.to_csv(f'{outfile}-{i}.csv', index=False)



#### Main ####

if __name__ == "__main__":
    
    args = parser.parse_args()

    # Chop up input PDF if "--pdf input.pdf"
    try:
        if args.pdf:
            os.chdir('working/')
            print(f'Chopping up {args.pdf} by page..')
            chop(args.pdf)
    except PyPDF2.utils.PdfReadError as err:
        print('Error occurred while processing PDF, the PDF might be corrupt..')
        print('Error Message: ', err)
        sys.exit()


    # Convert each PDF to TIFF if "--gs"
    if args.gs:
        print('Running GhostScript to generate TIFF images of each PDF file..')
        for pdf_file in os.listdir(os.getcwd()):
            if pdf_file != args.pdf:
                run_gs(pdf_file)

    # OCR each TIFF image if "--tess"
    if args.tess:
        print('Running tesseract OCR on each TIFF image..')
        for file in os.listdir(os.getcwd()):

            if file.endswith('.tif'):
                run_tesseract(file)
    
    # Run tabula to generate CSVs if "--csv"
    if args.csv:
        print('Running tabula..')
        pdf_to_csv()
    
