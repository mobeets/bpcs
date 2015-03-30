import os.path
from setuptools import setup

def read(fname):
    """
    Utility function to read the README file.
    Used for the long_description.  It's nice, because now 1) we have a top level
    README file and 2) it's easier to type in the README file than to put a raw
    string in below ...
    """
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "bpcs_steg",
    version = "0.0.1",
    author = "Jay Hennig",
    author_email = "mobeets@gmail.com",
    description = ("BPCS Steganography: embedding a message in a vessel image file"),
    license = "BSD",
    keywords = "bpcs steganography image bitplane complexity segmentation",
    url = "http://packages.python.org/bpcs_steg",
    packages=['bpcs_steg'],
    long_description=read('README')
)
