# Prometheus series helper


## Setup

1. Creating the virtual env
```
python3 -m venv venv
```
2. Activate it
```
source venv/bin/activate
```
3. Install dependencies
```
pip3 install humanfriendly
```

## Command Usage

### Expanding series:
```
helper expand --series 'SERIES_1' [--series 'SERIES_2' [--series 'SERIES_X']] [--unit_type (storage|time) --unit_name UNIT_NAME] [--raw]
```
Flags:
* `--series` :  The series represented in expanded notation format.  Can specify this flag multiple times when working with multiple seperate series
* `--unit_type` : (Optional) The unit type of the values.  This simplifies the representation of the values into human-readable values.  Possible values are `storage` and `time`.
* `--unit_name` : (Optional) When unit_type is set, this is used to specify the name of the unit, such as `b`, `KB`, `MiB`, etc. for storage and `us`, `ms`, `s`, `h`, etc. for time periods.
* `--raw`:  If included, the resulting series will be outputed directly on a single line instead of a formated table.

### Compressing series
```
helper compress --series 'SERIES_1' [--series 'SERIES_2' [--series 'SERIES_X']] 
```
Flags:
* `--series` :  The series represented in expanded notation format.  Can specify this flag multiple times when working with multiple seperate series


## Examples

Expanding:
```
./helper expand --series '10000000+1000000x6 16000000+0x3 10000000-1000000x4' --unit_type storage --unit_name kb

---------------------------------------------
*******        RESULTING VALUES     *********
---------------------------------------------
T =       0 |           10 GB
T =       1 |           11 GB
T =       2 |           12 GB
T =       3 |           13 GB
T =       4 |           14 GB
T =       5 |           15 GB
T =       6 |           16 GB
T =       7 |           16 GB
T =       8 |           16 GB
T =       9 |           16 GB
T =      10 |           16 GB
T =      11 |           10 GB
T =      12 |            9 GB
T =      13 |            8 GB
T =      14 |            7 GB
T =      15 |            6 GB
---------------------------------------------
```

Compressing:
```
./helper compress --series '1000 1100 1200 1300 1400 1500' --series '1500 1500 1500'

-------------------------------------------------------
*********      RESULTING EXPANDED NOTATION      *******
-------------------------------------------------------
1000+100x5
1500+0x2
```