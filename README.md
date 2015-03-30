__BPCS Steganography__: encoding/decoding messages hidden in a vessel image
Source: [pdf](http://web.eece.maine.edu/~eason/steg/SPIE98.pdf)

### Usage

```
$ python bpcs/bpcs.py -h
Usage: bpcs.py [options]

Options:
  -h, --help            show this help message and exit
  -i INFILE, --infile=INFILE
                        path to vessel image (.png)
  -o OUTFILE, --outfile=OUTFILE
                        path to write output file
  -m MESSAGEFILE, --messagefile=MESSAGEFILE
                        path to message file
  -a ALPHA, --alpha=ALPHA
                        complexity threshold
  -b BEHAVIOR, --behavior=BEHAVIOR
                        interaction modes: ['encode', 'decode', 'test',
                        'capacity']
```

#### Encoding

* Example: `python bpcs/bpcs.py -i vessel.png -m message.txt -o outfile.png -b encode`

* expects a vessel image file, message file, and alpha value
* hides the contents of a file inside a vessel image

#### Decoding

* Example: `python bpcs/bpcs.py -i vessel.png -a 0.45 -b decode`

* expects a vessel image file, and alpha value
* recovers the message stored inside a vessel image

#### Check image's message capacity

* Example: `python bpcs/bpcs.py -i vessel.png -a 0.45 -b capacity`

* expects a vessel image file and alpha value
* assesses the maximum size of a message that could be encoded within the vessel image

__Run tests__: `python bpcs/bpcs.py -b test`
