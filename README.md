# tm-distribute

Distribute XML trigger menus for synthesis (HLS, phase 2).

Use ```tm-distribute``` executable to generate a menu distribution/implementation.

    $ source ./setup.sh
    $ tm-distribute L1Menu_sample.xml -d 1

Generated directory structure:

    L1Menu_sample-d1
    ├── hls
    │   └── module_0
    │       └── src
    │           └── impl
    │               ├── menu.hxx
    │               ├── conditions.hxx
    │               ├── cuts.hxx
    │               └── seeds.hxx
    ├── testvectors
    ├── vhdl
    │   └── module_0
    │       └── src
    │           └── constants_pkg.vhd
    │   
    └── xml
        └── L1Menu_sample-d1.xml
