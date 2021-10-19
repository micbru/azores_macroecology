# All of this text is taken from an email chain with Dr. Tom Matthews and Dr. Paulo Borges

A large arthropod dataset from the Azores. In it, arthropods have been sampled over many years in multiple sites within four land-use types: native forest, exotic planatation forest, semi-natural pasture (less intensive arable), and intensive arable. All sampled individuals are identified to (morpho)species level and there is good abundance data (1000s of individuals). For beetles, all species have body length measurements which have been transformed into body mass estimates. There is also a very high proportion of alien arthropod species (almost half, depending on the land-use).

#number of transects per land use on Terceira island, Azores.
Native forest – 43 sites (actually 44)
Exotic Forest – 12 sites
Semi-Natural Pasture – 16 Sites
Intensive Pasture – 24 Sites

#Species and No. of individuals
There are data for all arthropods, and then beetles separately.
Across all sites, beetles represent 115 out of the 271 species and 9173 individuals out of the total 46,250.
All species are also further classified into endemic, non-endemic native (these two can be combined into native), and introduced.

MF is the the unique species / morpho species code. N/E/I is whether the species is native (but non-endemic), endemic or introduced. N and E can be combined to form the native category. Note that for four species, this classification is uncertain (NA value). (Tom originally told me 2 because it is 2 for adults only but four including juveniles.)

Trophic is a code for the trophic status of the species (e.g. predator, herbivore) but is perhaps not relevant for this. Body size is the length measurement done by Paulo in mm, and the body mass is this length converted into mg using the different equations mentioned in previous emails. Body mass is the mass of one individual. Then each column is a transect, with a unique name and the top row states whether the transect was in the plantation/exotic forest, native forest, semi-natural pasture or intensive pasture (i.e. the four land-uses). Each cell in these columns is the abundance (number of individuals) of a given species in a given transect.

The file ending andJUVENILES is the dataset including juveniles, which do not have body mass data and have only abundances.

###
Later, I requested more data on individual size variation for species so that we could estimate infraspecific metabolic rate distributions to better predict the MRDI. This was done separately for a subset of beetles and spiders which had multiple measurements rather than means and is in beetles/spider_body_size_indivs_MICAH.csv. The Spiders_Azores_Measur.xslx file is Paulo's version of this. Additionally, the Data_Adults_Land Use TER3.xlsx has updated mass estimates for spiders, as well as species identifications. It is the most up to date. 
More details on individual size files from Tom:
I have included a new version of the main dataset that included body size measurements (Data_Adults_Land Use TER3) - this now has the species names included and some updated body length / mass measurements (described below). In terms of individual body size measurements there are two datasets, one for beetles and one for spiders, but note that in both cases they only include a subset of the beetles and spiders in the main dataset:

1) Individual measurements for 26 of the 41 spiders species in the main dataset. This is from a newly assembled and published dataset of spider traits from Iberia ( https://bdj.pensoft.net/article/49159/ ) and includes more measurements of individuals from the Azores rather than the mainland. As such, we have updated the body size measurements in the main dataset for the relevant species with the mean calculated using these new values. Thus, the mean body length of any species in the attached spider dataset should match the mean body length in the main dataset - note that mean body mass in the main dataset will not match the mean of individual body masses in the spider dataset because body mass in the main dataset is calculated from the mean body length measurement, to match with how it was calculated for the other species where we don't have length measurements for individuals. Note also we use the mean across males and females (as this was what was done for the other species).

2) Individual measurements for 26 of the 115 beetle species in the main dataset. These come from an older project and importantly represent the body lengths of dried individuals. This is important because the body lengths in the main dataset are measured using specimens soaked in ethanol (as often done for inverts). As such, you cannot compare the absolute body length values in the attached beetles file with the values in the main dataset, but I don't see why we cannot look at variation still.

The LISTA MFs... file has the species relating to the MF codes.

I also wanted to calculate the 1D SAR in each transect. Paulo sent a list of individual pitfall traps as BD_LAND_USE_Individual pitfalls.xlsx. I saved this to a csv as IndividualPitfalls.csv
From Paulo:
We expect 30 pitfalls per site (see Sample number and Sample Code columns).
As you will see some of the Sites (Site code) have fewer samples due to the fact that had no adults in it. In some cases only juveniles were present.

Additional note: The xlsx files were uploaded to google drive then outputted as .csv files. I added "DATA" as a header so that we could have multi index throughout. The Adults.csv corresponds to TER3 which has updated spider masses and species names in the same files. Other than that it should be the same as the TER2 csv and xlsx. This means the adults and juveniles combined dataset shouldn't see any difference.

