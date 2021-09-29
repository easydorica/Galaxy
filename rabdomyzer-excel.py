# -*- coding: utf-8 -*-
#!/usr/bin/env python

import argparse
import pandas as pd


def read_csv(csv_file, sep='\t', index_col=False, encoding='utf-8'):
    #def read_csv(csv_file):
    '''
    '''
    csv_read = pd.read_csv(csv_file, sep=sep, index_col=index_col, encoding=encoding)
    #csv_read = pd.read_csv(csv_file,sep='\t', index_col=False, encoding='utf-8')
    return csv_read

def format_worksheet(workbook, worksheet):
    '''
    add conditional formatting to a worksheet
    '''
    
    format_red = workbook.add_format({'bg_color' : '#FF3333'})
    format_green = workbook.add_format({'bg_color' : '#66FF66'})
    #format_orange = workbook.add_format({'bg_color' : '#FFA500'})

    #worksheet.conditional_format('AU2:AU1000000', {'type':     'text',
    #                                       'criteria': 'containing',
     #                                      'value':    'tolerated',
      #                                     'format':   format_green})
    
    #worksheet.conditional_format('AU2:AU1000000', {'type':     'text',
     #                                      'criteria': 'containing',
      #                                     'value':    'deleterious',
       #                                    'format':   format_red})
    
    
    worksheet.conditional_format('AF2:AF1000000', {'type':     'text',                                    ##Sift
                                           'criteria': 'begins with',
                                           'value':    'D',
                                           'format':   format_red})
    
    worksheet.conditional_format('AF2:AF1000000', {'type':     'text',
                                           'criteria': 'begins with',
                                           'value':    'T',
                                           'format':   format_green})
    
    worksheet.conditional_format('AE2:AE1000000', {'type':     'text',                                      ##polyphen
                                           'criteria': 'begins with',
                                           'value':    'D',
                                           'format':   format_red})
                                           
    worksheet.conditional_format('AE2:AE1000000', {'type':     'text',
                                           'criteria': 'begins with',
                                           'value':    'B',
                                           'format':   format_green})
                                          
    worksheet.conditional_format('AD2:AD1000000', {'type':     'cell',
                                           'criteria': 'greater than or equal to',
                                           'value':    '15',
                                           'format':   format_red})
    #worksheet.conditional_format('AY2:AY1000000', {'type':     'cell',
     #                                      'criteria': 'greater than or equal to',
      #                                     'value':    '0.5',
       #                                    'format':   format_red})
                                           
    #worksheet.conditional_format('AZ2:AZ1000000', {'type':     'cell',
     #                                      'criteria': 'greater than or equal to',
      #                                     'value':    '3',
       #                                    'format':   format_red})                                                                              
    
    #worksheet.conditional_format('BA2:BA1000000', {'type':     'cell',
     #                                      'criteria': 'greater than or equal to',
      #                                     'value':    '0.5',
       #                                    'format':   format_red}) 
                                           
    #worksheet.conditional_format('BB2:BB1000000', {'type':     'cell',
     #                                      'criteria': 'greater than or equal to',
      #                                     'value':    '0.5',
       #                                    'format':   format_red})

    #worksheet.conditional_format('BC2:BC1000000', {'type':     'text',
     #                                      'criteria': 'containing',
      #                                     'value':    'PASS',
       #                                    'format':   format_red})

    #worksheet.conditional_format('BC2:BC1000000', {'type':     'text',
     #                                      'criteria': 'containing',
      #                                     'value':    'FAIL',
       #                                    'format':   format_green})
    
    return worksheet
     

   

def main():
    '''
    '''

    parser = argparse.ArgumentParser(description='Create an excel worksheet with rabdomyzer results')
    parser.add_argument('--het', help="het file created with rabdomyzer (required)", type=argparse.FileType('r'), required=True)
    parser.add_argument('--hom', help="hom file created with rabdomyzer (required)", type=argparse.FileType('r'), required=True)
    parser.add_argument('--comhet', help="comhet file created with rabdomyzer", type=argparse.FileType('r'))
    parser.add_argument('--output', help="excel output file (required) ", type=str, required=True)
    
    arguments = parser.parse_args()
    
    writer= pd.ExcelWriter(arguments.output, engine='xlsxwriter')
    workbook  = writer.book
    
    # het
    file_het= read_csv(arguments.het, sep='\t', index_col=False, encoding='utf-8')
    #file_het= read_csv(arguments.het)
    file_het.to_excel(writer, sheet_name='het_calls', encoding='utf8')
    worksheet_het = writer.sheets['het_calls']
    worksheet_het = format_worksheet(workbook, worksheet_het)
    
    #hom
    file_hom= read_csv(arguments.hom, sep='\t', index_col=False, encoding='utf-8')
    #file_hom= read_csv(arguments.hom)
    file_hom.to_excel(writer, sheet_name='hom_calls', encoding='utf8')
    worksheet_hom = writer.sheets['hom_calls']
    worksheet_hom = format_worksheet(workbook, worksheet_hom)
    
    if arguments.comhet:
       file_comhet=pd.read_csv(arguments.comhet, sep='\t', index_col=False, encoding='utf-8')
       #file_comhet=pd.read_csv(arguments.comhet)
       file_comhet.to_excel(writer, sheet_name='comhet_calls', encoding='utf8')
       worksheet_comhet = writer.sheets['comhet_calls']
       worksheet_comhet = format_worksheet(workbook, worksheet_comhet)
        
    writer.save()
    
if __name__ == '__main__':
    main()
     
    

