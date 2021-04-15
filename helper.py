#!/usr/bin/env python

import argparse
import sys
import re

from humanfriendly import format_size
from humanfriendly import format_timespan
from humanfriendly import parse_size
from humanfriendly import parse_timespan


DEBUG = False

def compress(input_series, show_input_series=False):
    print('\n-------------------------------------------------------')
    print('*********      RESULTING EXPANDED NOTATION      *******')
    print('-------------------------------------------------------')
    
    series_points = []
    for s in input_series:
        series_in = re.sub(r'(,|\s+)', ' ', s[0])
        series_points.append(list(map(float, series_in.split(' '))))

    list_diffs = []

    for series in series_points:
      size = len(series)

      value_prev = None
      value_diff = None
      list_diff = []

      for i in range(size):
        if value_prev == None:
          value_prev = series[size-(i+1)]
          continue

        value_diff = value_prev - series[size-(i+1)]
        value_prev = series[size-(i+1)]

        list_diff.append(value_diff)

        if len(list_diff) <= 1:
          continue

        if value_diff != list_diff[i-2]:
          print("The series {} can't be represented in expanded notation format!".format(series))
          exit(1)

      list_diffs.append(list_diff)

    exp_notation_parts = []
    for i in range(len(list_diffs)):

        if list_diffs[i][i] >= 0:
            symbol = "+"
        else:
            symbol = ""

        exp_notation = "{}{}{}x{}".format( series_points[i][0], symbol, list_diffs[i][i], len(series_points[i])-1) 
        if show_input_series:
            exp_notation_parts.append(f"{exp_notation} = {' '.join(input_series[i])}")
        else:
            exp_notation_parts.append(exp_notation)
        

    print('\n'.join(exp_notation_parts))
    print('\n---------------------------------------------')



def expand(input_series, output_raw, unit_type=None, unit_name=None):

    print('---------------------------------------------')
    print('*********      RESULTING VALUES     *********')
    print('---------------------------------------------')

    if DEBUG == True:
        print("[DEBUG] Input series: {}".format(input_series))

    for block in input_series:

        if DEBUG == True:
            print("[DEBUG] Current series block: {}".format(block))

        series = []

        for s in block[0].split():
            matches = re.search(r'((?P<base>\d+(\.\d+)?)(?P<operator>[-+])(?P<increment>\d+(\.\d+)?)(x|X)(?P<count>\d+))', s.strip())

            if DEBUG == True:
                print("[DEBUG] Match: {}".format(displaymatch(matches)))

            base =  float(matches.group('base'))
            if unit_type == 'storage':
                series.append(get_human_readable_size(base, unit_name))
            elif unit_type == 'time':
                series.append(get_human_readable_timespan(base, unit_name))
            else:
                series.append(base)

            for n in range(0, int(matches.group('count'))):
                if matches.group('operator') == '+':
                    val = base + int(matches.group('increment'))
                    if unit_type == 'storage':
                        series.append(get_human_readable_size(val, unit_name))
                    elif unit_type == 'time':
                        series.append(get_human_readable_timespan(val, unit_name))
                    else:
                        series.append(val)
                    base += int(matches.group('increment'))
                else:
                    val = base - int(matches.group('increment'))
                    if unit_type == 'storage':
                        series.append(get_human_readable_size(val, unit_name))
                    elif unit_type == 'time':
                        series.append(get_human_readable_timespan(val, unit_name))
                    else:
                        series.append(val)
                    base -= int(matches.group('increment'))

        if output_raw == False:
            for i in range(0, len(series)):
                val = f'{series[i]:g}'
                print("T = {:7} | {:>15}".format(i, val))
            
            print('---------------------------------------------')
        else:
            print(','.join(map(str, series)))
            print('\n')
            print('---------------------------------------------')


def displaymatch(match):
    if match is None:
        return None
    return '<Match: %r, groups=%r>' % (match.group(), match.groups())


def get_human_readable_size(value, unit):
    return format_size(parse_size(f"{value} {unit}"))

def get_human_readable_timespan(value, unit):
    seconds = parse_timespan(f"{value}{unit}")
    return format_timespan(seconds)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='subparser')

    parser.add_argument('--option', help="Expand or compress series")
    parser_expand = subparsers.add_parser('expand')
    parser_expand.add_argument('--series', help="Comma separated list of data points (series)", action='append', nargs='+')
    parser_expand.add_argument('--unit_type', help="Optional type of unit (supported: storage, time)", default=None)
    parser_expand.add_argument('--unit_name', help="Optional name of the unit (example storage: KB, GB, KiB, example time: ms, s, h)", default=None)
    parser_expand.add_argument('--raw', help="If set and option is expand, then displays the series values on a single line, comma separated.", action='store_true')
    
    parser_compress = subparsers.add_parser('compress')
    parser_compress.add_argument('--series', help="Comma separated list of data points (series)", action='append', nargs='+')
    parser_compress.add_argument('--show_input', help="If set, show the input series also", action='store_true')
    
    args = parser.parse_args()

    if args.subparser == 'expand':
        expand(args.series, args.raw, args.unit_type, args.unit_name)
    else:
        compress(args.series, args.show_input)
