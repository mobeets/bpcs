### Notes

#### A.

* read image as n-bit plane
* show n-bit plane as image

#### B.

* get n-bit image as n bit planes
    - e.g. n-by-m 8-bit image has pixels each as 0-255 => 8 n-by-m images with pixels as 0-1
* combine n bit planes as one n-bit plane

#### C.

* PBC (pure binary code) to CGC (gray code)
    - see: http://www.datahide.com/BPCSe/pbc-vs-cgc-e.html
    1. 1st most significant bit plane in CGC is just the PBC one
    2. given ith most significant bit plane in PBC, bit plane i in CGC becomes bit plane i in PBC XOR bit plane i-1 in PBC

* CGC to PBC

#### D. 

* file to list of bytes
* list of bytes to list of 8-bytes each

#### E. conjugate block (see source)

#### F. calculate image complexity of block

* k = sum of bit flips along each row and column of block
* max_k = maximum number of k given an n-by-m block
* returns k/max_k

#### Encoding

1. read file as n bit planes
2. PBC to CGC
3. segment each bit plane into blocks
4. mark each block as either simple or complex using threshold
5. conjugate each secret block if its complexity is below threshold
    - store this act in conjugation map
6. insert secret blocks using ordering defined
    - extra secret blocks are header (defining orderings?, and conjugation map)
7. CGC to PBC
8. write image

__Notes__:

* set info-threshold alpha (suggested alpha = 0.3)
* define function for sorting an image's blocks given its n bit planes
* define function for ordering a secret file's blocks
* define subset indices of complex blocks of image to be replaced with secret blocks

#### Misc

complexified: flip all grids with complexity < thresh

* cgc = rainbow
* pbc = silver

simplified: flip all grids with complexity > thresh

* cgc = normal, best_thresh ~ 0.35, ~12500 grids
* pbc = normal, best_thresh ~ 0.45, ~10500 grids
