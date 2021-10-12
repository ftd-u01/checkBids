# checkBids
Validate a BIDS directory

## Installation
You will need to install the 'bids' package for python (via sciget) before running
```
[user@sciget ~]$ pip3 install bids
```

## Usage
on an ibash session, first load in python
```
module load python/3.6.1
```
next, run the script and point it to the base directory of a BIDS dataset
```
python3 checkBids.py -p /path/to/bids/data
```
The script requires the 'LSB_JOBID' environment variable so it needs to run on an ibash session or via bsub. Currently the script will write to stdout, so if running via bsub it would be wise to pipe the output to a file
