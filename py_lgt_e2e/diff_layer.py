import sys,os

def diff_layer(offset : int):
    l_gap = 32
    l_size = (1605696, 401472, 401472, 401472, 1605696, 1605696, 401472, 401472, 1605696, 401472, 401472, 1605696, 802880, 200768, 802880, 802880, 200768, 200768, 802880, 200768, 200768, 802880, 200768, 200768, 802880, 401472, 100416, 401472, 401472, 100416, 100416, 401472, 100416, 100416, 401472, 100416, 100416, 401472, 100416, 100416, 401472, 100416, 100416, 401472, 200768, 50240, 200768, 200768, 50240, 50240, 200768, 50240, 50240, 200768, 4160, 2112)
    for i in range(0, len(l_size)):
        size = l_size[i]
        if offset < l_gap:
            print("offset in 1st gap: layer", i)
            sys.exit(1)
        offset -= l_gap
        if offset < size:
            print("diff at layer %d + %d(0x%x)" % (i, offset, offset))
            sys.exit(0)
        offset -= size
        if offset < l_gap:
            print("offset in 2nd gap: layer", i)
            sys.exit(1)
        offset -= l_gap
    assert False, "offset out of range"

if __name__ == "__main__":
    diff_layer(eval(sys.argv[1]))