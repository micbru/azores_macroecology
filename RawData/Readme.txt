NB: This data is also available at DataDryad as: https://doi.org/10.6078/D1CD97

A large arthropod dataset from the Azores. In it, arthropods have been sampled over many years in multiple sites within four land-use types: native forest, exotic planatation forest, semi-natural pasture (less intensive arable), and intensive arable. All sampled individuals are identified to (morpho)species level and there is good abundance data (1000s of individuals). Additionally, many species (particularly beetles) have body size measurements which can be converted to body mass measurements.

The required data files are:

Azores_Combined.csv - This file has abundances for all juvenile and adult individuals. Order is the taxonomic classification of a species, and MF is the the unique species / morpho species code. N/E/I is whether the species is native (but non-endemic), endemic or introduced. N and E can be combined to form the native category. Note that for four species, this classification is uncertain (NA value). Trophic is a code for the trophic status of the species (e.g. predator, herbivore). After the initial data, each column is an individual transect, with a unique name and the first row states whether the transect was in the plantation/exotic forest, native forest, semi-natural pasture or intensive pasture (i.e. the four land-uses). Each cell in these columns is the abundance (number of individuals) of a given species in a given transect. 
 
Azores_Adults.csv - This file is as the combined file, but additionally includes body size measurements in mm and converted body mass measurements. It additionally contains Family, Species name, OTU taxonomic information. It only contains information for the adult species, as the metabolic scaling laws are not available for the juveniles. 

IndividualPitfalls.csv - This file is to calculate the 1D SARs and contains spatial abundance information for several individual transects. There should be 30 pitfalls per site, with the site indexed by Site Code, and the sample indexed by Sample number and Sample code, but some sites have fewer samples as they had no adults present. The year, month, and site name are also available. The other columns are as in the other datasets.

(beetles/spider)_body_size_indivs.csv - These files contain a subset of beetles and spiders which had multiple measurements rather than means of their mass across all individuals. The columns are simply species, body length, and body mass. This is important to try to determine the amount of variance in body mass within a species and is used in the IntraspecificBodyMassVariation.ipynb.

LISTA MFs guilds_Body_Size_Fev_2021.xlsx - This file contains the species identification information for different MF codes.

Note that many of the .csv files have multiple header rows, so to read into python, multiindex is required. (Example: pd.read_csv('./RawData/Azores_Combined.csv',header=[0,1]))

The other files can be ignored but are mainly excel versions of the same data.