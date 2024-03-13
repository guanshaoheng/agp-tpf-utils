
- [1. Utilities for Tree of Life AGP and TPF Assembly Files](#1-utilities-for-tree-of-life-agp-and-tpf-assembly-files)
  - [1.1. Scripts](#11-scripts)
    - [1.1.1. `asm-format`](#111-asm-format)
    - [1.1.2. `pretext-to-tpf`](#112-pretext-to-tpf)
  - [1.2. File Formats](#12-file-formats)
    - [1.2.1. AGP](#121-agp)
      - [1.2.1.1. Tags](#1211-tags)
    - [1.2.2. TPF](#122-tpf)
  - [1.3. Development Setup](#13-development-setup)
    - [1.3.1. Reinstalling Development Environment](#131-reinstalling-development-environment)
  - [1.4. Running Tests](#14-running-tests)


# 1. Utilities for Tree of Life AGP and TPF Assembly Files

Code for working with AGP and TPF files as used within the Tree of Life
project, where the combination of long read sequencing and HiC data is used
to produce whole genome assemblies. It is not therefore intended to cover the
full range of AGP and TPF syntax.

## 1.1. Scripts

Added to your `PATH` if the suggested development venv is set up. Run with
`--help` for usage.

### 1.1.1. [`asm-format`](src/tola/assembly/scripts/asm_format.py)

Parses and reformats AGP and TPF files, converting into either format.

### 1.1.2. [`pretext-to-tpf`](src/tola/assembly/scripts/pretext_to_tpf.py)

Takes the AGP file output by
[PretextView](https://github.com/wtsi-hpag/PretextView)
and creates TPF files containing precise coordinates of the curated assembly.

## 1.2. File Formats

Both TPF and AGP file formats described here contain the same information. AGP
is the more appropriate format to use, since it was designed for sequence
assembly coordinates, whereas TPF was for listing (cosmid, fosmid, YAC or
BAC) clones and their accessions in the order that they were tiled to build a
chromosome.

### 1.2.1. AGP

Each line in the
[AGP v2.1 specification](https://www.ncbi.nlm.nih.gov/assembly/agp/AGP_Specification/)
contains 9 tab delimited columns. Of these columns:

- **column 1** the name of the object being assembled (i,e. scaffold_#),
- **column 2** starting position of the components/contigs on the object/assembly,
- **column 3** ending position of the components/contigs on the object/assembly,
- **column 4** line count for the compenents/contigs described in column 1.  
- **DNA Sequence**
    - **column 5** the "component_type" contains `W` in our assemblies,
        meaning a contig from Whole Genome Shotgun (WGS) sequencing.
    - **column 6** name of the component contributing to the object described in column 1,
    - **column 7** begining of the component that contributes to the object in column 1 (in component coordinates),
    - **column 8** ending of the component that contributes to the object in column 1 (in component coordinates),
    - **column 9** orientation, `+` foward, `-` reverse, `?` unknown, `0` unknow, `na` irrelevant. By default, components with (`?`, `0`, or `na`) are treated as `+`,
    - **columns 10 and greater** are extra tag metadata columns not included
        in the AGP v2.1 specification. (See below for their possible
        values.)
- **Gaps**
    - **column 5** the "component_type" contains `U` in our assemblies, for a
        gap of unknown length. (The other gap type `N` is for gaps of known
        length.)
    - **column 6** The default length in the specification for `U` gaps is 100
        base pairs, but we use 200 bp gaps, as produced by
        [yahs](https://github.com/sanger-tol/yahs)
    - **column 7** "gap_type" has `scaffold`, signifying a gap between two contigs in a
        scaffold.
    - **column 8** has `yes`, signifying that there is evidence of linkage
        between the sequence data on either side of the gap,
    - **column 9** type of evidence used to assert linkage, `na` if column 8 is `no`, if there is a linkage, this column can be `paired-ends`, `align_genus`, ..., if multiple lines of evidence to support linkage, all can be listed sing a ';' delimiter.


#### 1.2.1.1. Tags

Single words appended in tab-delimted columns beyond column 9, they can
contain:

- `Contaminant`
- `Haplotig` for haplotype-specific contigs.
- Haplotypes:
  - `Hap1`, `Hap2`…
- `Painted` where fragment has HiC contacts.
- `Unloc` are fragments attached to chromosomes but unlocalised within them.
- Sex Chromosomes:
  - `U`
  - `V`
  - `W` or `W1`, `W2`…
  - `X` or `X1`, `X2`…
  - `Y` or `Y1`, `Y2`…
  - `Z` or `Z1`, `Z2`…
- [B Chromosomes](https://en.wikipedia.org/wiki/B_chromosome):
  - `B1`, `B2`, `B3`…

### 1.2.2. TPF

Our TPF files are highly diverged from the
[original specification](https://www.ncbi.nlm.nih.gov/projects/genome/assembly/TPF_Specification_v1.4_20110215.pdf).

- We incorporate assembly coordinates, which was not the purpose of TPF files.
- We do not necessarily include any `##` header lines, which were mandatory in
  the original specification.
- **DNA Sequence**
    - **column 1** the "accession" is always `?` since the components of our
        assemblies are not accessioned.
    - **column 2** the "clone name" does not contain a clone name, but
        contains the name of scaffold fragment or whole scaffold, with the
        format: `<name>:<start>-<end>` *i.e.* assembly coordinates.
    - **column 3** the "local contig identifier" now contains the name of the
        scaffold each sequence fragment belongs to. Each TPF file used to
        contain a single chromosome, but we put a whole genome into a single
        file, and this column groups the fragments into chromosomes /
        scaffolds.
    - **column 4** which in the original specification was used for
        indicating `CONTAINED` or `CONTAINED_TURNOUT` clones now holds
        assembly strand information, either `PLUS` or `MINUS`.
- **Gaps**
    - **column 2** is `TYPE-2`, which meant a gap between two clones
    - **column 3** length, using our default of 200 bp.

## 1.3. Development Setup

In your cloned copy of the git repository:

```sh
python -m venv --prompt asm-utils venv
source venv/bin/activate
pip install --upgrade pip
pip install --editable .
```

An alias such as this:

```sh
alias atu="cd $HOME/git/agp-tpf-utils && source ./venv/bin/activate"
```

in your shell's `.*rc` file (*e.g.* `~/.bashrc` for `bash` or `~/.zshrc` for
`zsh`) can be convenient.

conda:
```sh
conda create -n asm-utils python=3.11 && conda activate asm-utils
pip install --upgrade pip
pip install --editable .
```  
while using,
```sh
conda evn list
conda activate asm-utils
``` 

### 1.3.1. Reinstalling Development Environment

Some changes, such as adding a new command line script to
[`pyproject.toml`](pyproject.toml), require the development environment to be
reinstalled:

```sh
pip uninstall tola-agp-tpf-utils
pip install --editable .
hash -r
```

## 1.4. Running Tests

Tests, located in the [`tests/`](tests) directory, are run with the `pytest`
command from the project root.
