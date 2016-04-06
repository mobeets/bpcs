## BPCS Steganography

Source: [pdf](http://web.eece.maine.edu/~eason/steg/SPIE98.pdf)

The goal of steganography is to hide a message in plain sight. Here, we embed a message in an image by replacing all "complex" blocks of pixels in the image with portions of our message. It turns out that portions of the image with high complexity can be entirely removed (or in this case, replaced with our message) without changing the appearance of the image at all. Because most blocks of pixels are complex (i.e., with complexity above some threshold, "alpha"), we can usually replace around 45% of our image with a hidden message. Below, the 300x300 image on the right contains the text of an entire novel, while still looking nearly identical to the vessel image on the left.

![vessel](https://cloud.githubusercontent.com/assets/1677179/14302935/10adb242-fb74-11e5-9cc7-e5a213760876.png)
![out](https://cloud.githubusercontent.com/assets/1677179/14302974/712fdfc8-fb74-11e5-89fe-a11a2116f055.png)

### Encoding and decoding

First, we want to embed a file in a vessel image. Here, we'll embed the text of an entire novel in a 300x300 image.

`python bpcs.py encode -i examples/vessel.png -m examples/message.txt -o examples/encoded.png`

Now, given the encoded image, we want to recover the message hidden inside it.

`python bpcs.py decode -i examples/encoded.png -a 0.45 -o examples/message_decoded.txt`

The output, message_decoded.txt, should be the same as message.txt, which means we have recovered our original message.

### Checking a vessel image's message capacity

Given a vessel image file and an alpha value, we can assess the maximum size message that we could encode.

`python bpcs.py capacity -i examples/vessel.png -a 0.45`

The vessel image in the examples folder is 158 KB, and can store a hidden message of up to around 66 KB.

### Customization

The goal of steganography is to hide things in plain sight. For this reason, BPCS doesn't use a secret key or password for encoding and decoding. However, aside from varying the alpha parameter, one way to customize the BPCS procedure is by adding custom encryption and decryption to the message before and after using BPCS.

### Running tests

`python bpcs.py test`

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
