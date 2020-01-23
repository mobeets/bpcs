## BPCS Steganography

The goal of steganography is to hide a message in plain sight. BPCS is a method to embed a message in an image by replacing all "complex" blocks of pixels in the image with portions of our message. It turns out that portions of the image with high complexity can be entirely removed (or in this case, replaced with our message) without changing the appearance of the image at all. Because most blocks of pixels are complex (i.e., with complexity above some threshold, alpha), you can usually replace around 45% of an image with a hidden message. Below, the 300x300 image on the right contains the text of an entire novel, while still looking virtually identical to the vessel image on the left.

![vessel](https://cloud.githubusercontent.com/assets/1677179/14302935/10adb242-fb74-11e5-9cc7-e5a213760876.png)
![out](https://cloud.githubusercontent.com/assets/1677179/14302974/712fdfc8-fb74-11e5-89fe-a11a2116f055.png)

Note that with BPCS, the hidden message doesn't have to be text. It can be any file type, including another image.

You could upload a profile photo to a website that contains a secret image. Or you could embed an image of a turtle inside an image of a turtle inside an image...turtles all the way down.

This is an implementation of the method discussed in: Kawaguchi, Eiji, and Richard O. Eason. "Principles and applications of BPCS steganography." In Photonics East (ISAM, VVDC, IEMB), pp. 464-473. International Society for Optics and Photonics, 1999. ([pdf](http://web.eece.maine.edu/~eason/steg/SPIE98.pdf))

### Encoding and decoding

First, we want to embed a file in a vessel image. Here, we'll embed the text of an entire novel in a 300x300 image.

`$ python -m bpcs.bpcs encode -i examples/vessel.png -m examples/message.txt -a 0.45 -o examples/encoded.png`

Now, given the encoded image, we want to recover the message hidden inside it.

`$ python -m bpcs.bpcs decode -i examples/encoded.png -a 0.45 -o examples/message_decoded.txt`

The output, message_decoded.txt, should be the same as message.txt, which means we have recovered our original message.

### Checking a vessel image's message capacity

Given a vessel image file and an alpha value, we can assess the maximum size message that we could encode.

`$ python -m bpcs.bpcs capacity -i examples/vessel.png -a 0.45`

The vessel image in the examples folder is 158 KB, and can store a hidden message of up to around 66 KB.

### Customization

The goal of steganography is to hide things in plain sight. For this reason, BPCS doesn't use a secret key or password for encoding and decoding. However, aside from varying the alpha parameter, one way to customize the BPCS procedure is by adding custom encryption and decryption to the message before and after using BPCS.

### Run as a module

```python
import bpcs

alpha = 0.45
vslfile = '../examples/vessel.png'
msgfile = '../examples/message.txt' # can be any type of file
encfile = '../examples/encoded.png'
msgfile_decoded = 'tmp.txt'

bpcs.capacity(vslfile, alpha) # check max size of message you can embed in vslfile
bpcs.encode(vslfile, msgfile, encfile, alpha) # embed msgfile in vslfile, write to encfile
bpcs.decode(encfile, msgfile_decoded, alpha) # recover message from encfile
```

### Running tests

`$ python -m bpcs.bpcs test`
