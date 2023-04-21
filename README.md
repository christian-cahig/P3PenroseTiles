# `P3PenroseTiles`

This repository contains Python code for generating P3 Penrose tilings.
The core functionalities are implemented as a custom package in [`src/core/`](./src/core/).
Scripts for producing example tilings are provided in [`src/`](./src/).
Generated tilings are saved as SVG files in [`outputs/`](./outputs/).

## Reproducibility

For reproducibility, use [`env.yml`](./env.yml) to set up a conda environment with Python 3.10.10.

## Acknowledgement

This work is inspired by Christian Hill's blog posts at
[https://scipython.com/blog/penrose-tiling-1/](https://scipython.com/blog/penrose-tiling-1/)
and
[https://scipython.com/blog/penrose-tiling-2/](https://scipython.com/blog/penrose-tiling-2/).
The implementation used here largely follows his code at
[https://github.com/xnx/penrose](https://github.com/xnx/penrose),
but differs in code style and feature coverage.

## Citing

Should you wish to cite this work, please use the following BibLaTeX entry
(also available in [`CITATION.bib`](./CITATION.bib)):

```bibtex
@Online{P3PenroseTiles,
  author       = {Christian {Cahig}},
  date         = {2023-04-21},
  title        = {P3PenroseTiles},
  url          = {https://github.com/christian-cahig/P3PenroseTiles},
}
```

## License

This repository is licensed under the
[Creative Commons Attribution 4.0 International Public License](https://creativecommons.org/licenses/by/4.0/).
Please see [`LICENSE`](./LICENSE) for the details.
