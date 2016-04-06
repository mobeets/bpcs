__BPCS Steganography__: encoding/decoding messages hidden in a vessel image (source: [pdf](http://web.eece.maine.edu/~eason/steg/SPIE98.pdf))

#### Encoding/Decoding

First, we want to embed a file in a vessel image. Here, we'll embed the text of an entire novel in a 300x300 image.

`python bpcs.py encode -i examples/vessel.png -m examples/message.txt -o examples/encoded.png`

Now, given the encoded image, we want to recover the message hidden inside it.

`python bpcs.py decode -i examples/encoded.png -a 0.45 -o examples/message_decoded.txt`

The output, message_decoded.txt, should be the same as message.txt, which means we have recovered our original message.

#### Checking a vessel image's message capacity

Given a vessel image file and an alpha value, we can assess the maximum size message that we could encode.

`python bpcs.py capacity -i examples/vessel.png -a 0.45`

__Run tests__: `python bpcs.py test`

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
