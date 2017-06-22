#!/usr/bin/env python

import argparse
import os
from openpyxl import Workbook, load_workbook
from translate_survey import load_translations

parser = argparse.ArgumentParser(description = "Merges two spreadsheets of translation strings with the second file provided overriding the values of the first.")

parser.add_argument(
    'FIRST_FILE',
    type=argparse.FileType('rb'),
    help="The location of the file that will have it's translations overridden on a key clash"
)

parser.add_argument(
    'SECOND_FILE',
    type=argparse.FileType('rb'),
    help="The location of the file who's translations should be kept on a key clash"
)

parser.add_argument(
    'OUT',
    type=argparse.FileType('wb'),
    help="The path of the new file of merged translations"
)

def output_translations(translations, aFile):
    wb = Workbook()
    ws = wb.active
    ws.append(['Context', 'English Text', 'Welsh Text'])
    for line in translations:
        ws.append(line)

    wb.save(aFile)

if __name__ == '__main__':
    args = parser.parse_args()

    alpha_translations = load_translations(args.FIRST_FILE)
    beta_translations = load_translations(args.SECOND_FILE)

    alpha_keys = set(alpha_translations.keys())
    beta_keys = set(beta_translations.keys())

    for aKey in alpha_keys.difference(alpha_keys):
        print(aKey)

    alpha_translations.update(beta_translations)

    translations_list = []
    for k,v in alpha_translations.items():
        translations_list.append((k[0], k[1], v))

    output_translations(translations_list, args.OUT)
