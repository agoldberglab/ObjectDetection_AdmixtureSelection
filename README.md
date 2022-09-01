# Example scripts for Object Detection-based selection scans using images of ancestry patterns project

## Notes for generalizable SLiM simulations:

A. [admixture.slim](./admixture.slim) - this is a programmable/general SLiM script for admixture simulations. As is, user must specify the following parameters from the command line:

<table>
    <thead>
        <tr>
            <th align="center">variable name</th>
            <th align="center">parameter description</th>
            <th align="center">example</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td rowspan=1 align="center">L</td>
            <td rowspan=1 align="center">chromosome length (bp)</td>
            <td rowspan=1 align="center">-d L=50000000</td>
        </tr>
        <tr>
            <td rowspan=1 align="center">s</td>
            <td rowspan=1 align="center">selection coefficient for fixed fitness effects</td>
            <td rowspan=1 align="center">-d s=0.05</td>
        </tr>
        <tr>
            <td rowspan=1 align="center">mig</td>
            <td rowspan=1 align="center">source population 1 admixture proportion</td>
            <td rowspan=1 align="center">-d mig=0.5</td>
        </tr>
        <tr>
            <td rowspan=1 align="center">N</td>
            <td rowspan=1 align="center">admixed population size</td>
            <td rowspan=1 align="center">-d N=10000</td>
        </tr>
        <tr>
            <td rowspan=1 align="center">t_end</td>
            <td rowspan=1 align="center">number of generations for simulation</td>
            <td rowspan=1 align="center">-d t_end=50</td>
        </tr>
        <tr>
            <td rowspan=1 align="center">out</td>
            <td rowspan=1 align="center">general name for output files. should also include output directory</td>
            <td rowspan=1 align="center">-d out='"/work/ih49/simulations/test_NN/human_L-50_N-10000_single-pulse_m-0.5"'</td>
        </tr>
        <tr>
            <td rowspan=1 align="center">seed</td>
            <td rowspan=1 align="center">seed number to append to output file</td>
            <td rowspan=1 align="center">-d out='"seed-5"'</td>
        </tr>        
    </tbody>
</table>

Simulation script will output two files
1. a `.trees` file with the name `{out}_s-{selectioncoeff}_pos-{physicalposition}_seed-{seednum}.trees`. This file will be used to generate ancestry images.
2. a `variants.txt` file with the name `{out}_seed-{seednum}_variants.txt`. This file contains the physical position and selection strength of each variant in the simulation. The single variant simulations have this information in the filenames, but having this information separate may be helpful for keeping track of the range of selection strengths and physical positions. It is also useful for simulations with two or more selected mutations.

In the simulation script, there are some lines that can be uncommented to include population size changes, three-way admixture, two selected mutations, continuous migration each generation. I haven't tested these completely, so let me know if there are bugs when incorporating those options.

B. [run_admixture.sh](./run_admixture.sh) - example job array script to generate 1000 SLiM simulations with the [admixture.slim](./admixture.slim) file.

C. [localancestry_alltracts.py](./localancestry_alltracts.py) - script to create bed-like file of ancestry tracts for 200 samples (haploid chromosomes, not diploid individuals) from the .trees file. Assumes two-way admixture and 1 ancestor in each source population.

D. [admixture_ancestrytracts_jobarray.sh](./admixture_ancestrytracts_jobarray.sh) - example job array to generate bed-like ancestry tract files for 1000 SLiM simulations with the [localancestry_alltracts.py](./localancestry_alltracts.py) script.

E. [admixture_makeimage.R](./admixture_makeimage.R) - script to generate b&w ancestry images. Assumes two-way admixture. Height is hard-coded to 200 pixels (i.e. assumes 200 sampled individuals). Chromosome length and image width must be specified at command line. e.g. `admixture_makeimage.R filename_alltracts.txt 50000000 400` would create a 200x400 image, assuming a chromosome length of 50 Mb.

F. [admixture_makeimages_jobarray.sh](./admixture_makeimages_jobarray.sh) - example job array to generate images for 1000 simulations with [admixture_makeimage.R](./admixture_makeimage.R) script
