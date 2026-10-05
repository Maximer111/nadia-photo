#!/usr/bin/env python3
"""Cuts Nadia's originals into web sizes for the slots on the site.

Run: python3 photos.py /path/to/originals
Output: img/p/<id>-<width>.jpg. build.py expands [[<id>]] tokens from SPEC.
"""
import pathlib
import sys

RATIOS = {"r23": 2 / 3, "r34": 3 / 4, "r43": 4 / 3, "r32": 3 / 2, "r169": 16 / 9}

# id: (ratio class, vertical focus 0..1 where the crop is centred, widths)
SPEC = {
    "9957": ("r34", .55, (800, 1600)),
    "2858": ("r23", .5, (600, 1200)),
    "9487": ("r23", .5, (600, 1200)),
    "9203": ("r32", .5, (800, 1600)),
    "4461": ("r34", .5, (600, 1200)),
    "9086": ("r169", .62, (1200, 2400)),
    "9318": ("r169", .5, (1200, 2400)),
    "9096": ("r34", .5, (800, 1600)),
    "8734": ("r23", .5, (600, 1200)),
    "9973": ("r43", .75, (800, 1600)),
    "8406": ("r34", .5, (600, 1200)),
    "4321": ("r43", .45, (800, 1600)),
    "9565": ("r169", .42, (1200, 2400)),
}


def cut(src_dir, out_dir):
    from PIL import Image, ImageOps
    out_dir.mkdir(parents=True, exist_ok=True)
    for pid, (cls, fy, widths) in SPEC.items():
        im = ImageOps.exif_transpose(Image.open(src_dir / f"_MG_{pid}.jpg"))
        icc = im.info.get("icc_profile")
        r, (W, H) = RATIOS[cls], im.size
        if W / H > r:
            w = round(H * r); x = (W - w) // 2
            im = im.crop((x, 0, x + w, H))
        else:
            h = round(W / r); y = round(min(max(fy * H - h / 2, 0), H - h))
            im = im.crop((0, y, W, y + h))
        im = im.convert("RGB")
        for w in widths:
            # no exif= passed: camera metadata and any GPS are dropped
            im.resize((w, round(w / r)), Image.LANCZOS).save(
                out_dir / f"{pid}-{w}.jpg", quality=80, optimize=True,
                progressive=True, icc_profile=icc)
        print(pid, cls, widths)


if __name__ == "__main__":
    cut(pathlib.Path(sys.argv[1]), pathlib.Path(__file__).parent / "img" / "p")
