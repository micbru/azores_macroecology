These jupyter notebooks replicate all analysis in the paper "Land use change through the lens of macroecology: new
insights from Azorean arthropod communities", by M Brush, TJ Matthews, PAV Borges, J Harte.

The figures for the paper are all output to the Figures file. 
The RawData folder is the raw data from the Azorean arthropods, including the the transect level abundances, spatial information for certain transects, and intraspecific body mass information for a few species of beetles and spiders.
The ProcessedData folder includes means, state variables, and other useful data that has been summarized across land use for plotting.

The files SAD_*.ipynb and MRDI_*.ipynb replicate all of the analysis for the SAD and MRDI. The _combined file is for aggregating across transects, the _transect is the transect level analysis, and the _transect_indigenous is the analysis separating indigenous and introduced species. For the SAD, there is additionally a _transect_dgof_R file that is actually in R instead of python and uses the package dgof to get more accurate KS tests for the discrete log series distribution.

The files SAR_analysis and SAR_analysis_indigenous are the analysis for the SAR at the transect level, and the latter separates by indigenous and introduced species status.

The Plots_across_patterns files takes information from the SAD, MRDI, and SAR analysis and plots all of the summarized information on a single plot. This includes the means of the mlsq across land use, including with indigenous and introduced species separate, which are the main plots in the paper. It also has the KS comparison for the SAD and MRDI in the appendix.

The file StatisticalAnalyses.ipynb has the ANOVA + Tukey test as well as the Kruskal-Wallis + Dunn test used in the appendix to support our results.

The Table2_SN_data obtains all of the information for median S and N across land use, and the total S and N. This is all in the table in the main text.

Finally, IntraspecificBodyMassVariation obtains the relationship between mean and variance for body mass for a subset of beetle and spider species. This is in the appendix. These values are then used to reconstruct the intraspecific MRDI in the MRDI analysis.