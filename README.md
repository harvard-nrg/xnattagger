# XNAT Tagger (beta)

xnattagger is a command line tool that queries and adds hashtags to the scan note field of MR Session 
scans on XNAT.

Tagging scans is a necessary precursor to running certain automated QC pipelines that require combinations 
of scans e.g., volumetric navigators and diffusion.

# Usage

xnat_tagger.py --xnat-alias myxnat --target-modality t1w t2w dwi --label AB1234C
