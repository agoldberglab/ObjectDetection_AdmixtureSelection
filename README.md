# Example scripts for object detection-based selection scans using images of ancestry patterns

## Software versions used in this project
[SLiM](https://messerlab.org/slim/) - v3.4

[R](https://cran.r-project.org/) - v4.0.0

[Python](https://www.python.org/) - v3.7.4

Python libraries:
* [IceVision](https://airctic.com/0.5.2/) - v0.5.2
* [tskit](https://tskit.dev/tskit/docs/stable/introduction.html) - v0.2.3 (included in [msprime](https://tskit.dev/msprime/docs/stable/intro.html) v0.7.4)
* [pyslim](https://tskit.dev/pyslim/docs/latest/introduction.html) - v0.401

R packages:
* [tidyverse](https://www.tidyverse.org/) - v1.3.0
* [magrittr](https://cran.r-project.org/web/packages/magrittr/vignettes/magrittr.html) - v2.0.1
* [plyr](https://www.rdocumentation.org/packages/plyr/versions/1.8.6) - v1.8.6 

## Notes for generalizable SLiM simulations:

A. [admixture.slim](./admixture.slim) - this is a programmable/general SLiM script for admixture simulations. Selection strength is randomly drawn from a uniform distribution s~U(0, 0.5). As is, user must specify the following parameters from the command line:

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

In the simulation script, there are some lines that can be uncommented to include population size changes, three-way admixture, two selected mutations, continuous migration each generation. I haven't tested these completely, so there may be bugs.

B. [run_admixture.sh](./run_admixture.sh) - example job array script to generate 1000 SLiM simulations with the [admixture.slim](./admixture.slim) file.

C. [localancestry_alltracts.py](./localancestry_alltracts.py) - script to create bed-like file of ancestry tracts for 200 samples (haploid chromosomes, not diploid individuals) from the .trees file. Assumes two-way admixture and 1 ancestor in each source population.

D. [admixture_ancestrytracts_jobarray.sh](./admixture_ancestrytracts_jobarray.sh) - example job array to generate bed-like ancestry tract files for 1000 SLiM simulations with the [localancestry_alltracts.py](./localancestry_alltracts.py) script.

E. [admixture_makeimage.R](./admixture_makeimage.R) - script to generate b&w ancestry images. Assumes two-way admixture. Height is hard-coded to 200 pixels. Chromosome length and image width must be specified at command line. e.g. `admixture_makeimage.R filename_alltracts.txt 50000000 400` would create a 200x400 image, assuming a chromosome length of 50 Mb and `admixture_makeimage.R filename_alltracts.txt 295 200` would create a 200x200 image, assuming a chromosome with max genetic map length of 295 cM. Excpects bed-like file of ancestry tracts (exclusive. e.g. intervals are \[start, end)) with at least the following columns (any order, labeled):
   * *start_bp* - first position of ancestry tract (0-based, can be physical or genetic map positions, correct corresponding chromosome length must be specified at command line)
   * *end_bp* - last position of ancestry tract (exclusive)
   * *ancID* - ancestry label for that tract (expects 0 or 1)
   * *childID* - unique haplotype ID (e.g. for a diploid indiviudal "SUBJ-A" you would have tracts mapping to SUBJ-A_Hap1 and SUBJ-A_Hap2)

F. [admixture_makeimages_jobarray.sh](./admixture_makeimages_jobarray.sh) - example job array to generate images for 1000 simulations with [admixture_makeimage.R](./admixture_makeimage.R) script

Misc scripts:

* alternate admixture SLiMulation files:
  * [admixture_popsize.slim](./admixture_popsize.slim) - similar to above, but includes block for bottleneck at 25-35 generations
  * [admixture_Fst.slim](./admixture_Fst.slim) - similar to above, but draws beneficial mutation from both populations
  * [admixture_whole-genome.slim](./admixture_whole-genome.slim) - similar to above, but for "whole genome" (multiple chromosomes)


## Training & Inference w/ [IceVision v0.5.2](https://airctic.com/0.5.2/)

Example code and notes for training and inference can be found in [objectdetection_ancestryimages_example.ipynb](./objectdetection_ancestryimages_example.ipynb)

* [inference.py](./inference.py) - skip training & get precision & recall values across varying threshholds for a set of images, using a pre-trained model

#### Notes for running in SLURM environment

In order to run IceVision on the Duke Compute Cluster (slurm), we built a Singularity container image (see e.g. [Singularity.def](./Singularity.def)), which can be pulled down by running:

```curl -k -O https://research-singularity-registry.oit.duke.edu/goldberglab/selectionscansingularity.sif```

Then you can run scripts on the cluster, for example:

```singularity exec --nv -B /work selectionscansingularity.sif inference.py simulation_scripts_directory analysis_sub_directory```
