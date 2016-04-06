__BPCS Steganography__: encoding/decoding messages hidden in a vessel image (source: [pdf](http://web.eece.maine.edu/~eason/steg/SPIE98.pdf))

### Usage

```
$ python bpcs/bpcs.py -h
usage: bpcs.py [-h] [-i INFILE] [-o OUTFILE] [-m MESSAGEFILE] [-a ALPHA]
               behavior

positional arguments:
  behavior              interaction modes: ['encode', 'decode', 'test',
                        'capacity']

optional arguments:
  -h, --help            show this help message and exit
  -i INFILE, --infile INFILE
                        path to vessel image (.png)
  -o OUTFILE, --outfile OUTFILE
                        path to write output file
  -m MESSAGEFILE, --messagefile MESSAGEFILE
                        path to message file
  -a ALPHA, --alpha ALPHA
                        complexity threshold
```

#### Encoding/Decoding

First, we want to embed the file `examples/message.txt` in the image at `examples/vessel.png`. The output is `encoded.png`.

`python bpcs.py encode -i vessel.png -m message.txt -o encoded.png`

Now, given `encoded.png`, we want to recover the message.

`python bpcs.py decode -i encoded.png -a 0.45 -o message_decoded.txt`

Now, `message_decoded.txt` is the same as `message.txt`, so we have recovered our original message.

#### Checking a vessel image's message capacity

Given a vessel image file and an alpha value, we can assess the maximum size message that we could encode.

`python bpcs.py -i vessel.png -a 0.45 -b capacity`

__Run tests__: `python bpcs.py test`
