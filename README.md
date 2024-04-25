## Summary
This repo contains some scripts and utilities that will go from a draw.io diagram to csv and back.  It needs to be refactored a bit, but its functional.

## Going from an excel CSV to Drawio
```sh
xl_to_drawio.sh [inputfile] [outputfile]
```
Note: within this script is a command line call to draw.io to the final step of the conversion.  You will need to update `drawio_path="/Applications/draw.io.app/Contents/MacOS/draw.io"`, within `csv_to_drawio.sh` to reflect the location of draw.io on your system for the pipeline to work.

## Going from Drawio to and excel CSV
```sh
drawio_to_xl.sh [inputfile] [outputfile]
```

## Odds and Ends
There is a little hardcoding of headers, and header ordering.  The code is flexible to take arbitrary headers.  You may want to edit csv_reorder_headers.py if to suit your needs.




