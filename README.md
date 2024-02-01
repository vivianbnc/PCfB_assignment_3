# README

# Owner
Vivian Bonacker

# Editing
vivianbnc Mi, 31.01.24 23:00

# Practical Information
This document should be used to understand the python script "pcfb_script_assignment_3.py".
The script was created as part of the course Practical Computing for Biologists at the University of Groningen.
More information on this course can be found here: https://ocasys.rug.nl/current/catalog/course/WMBY008-05

# Information on the script
The script aims to import an excel file and create a boxplot to visualise the results. Optionally an interactive plot can be created. However, this is only a basic plot.

# Prerequisites
the listed modules are needed to use the script:
pandas, 
matplotlib.pyplot, 
seaborn, 
plotly.graph_objects, 
plotly.express, 
plotly.io, 

# Using the script
All Functions have docstrings that explain the usage of the function.Some functions have an extra explanation below.

### import_excel function
This function can be used to import a certain sheet of an excel file.
If "usecol=" is specified, only certain columns will be included. Otherwise all columns will be included.
### remove_blanks function
This function can be used to remove rows that contain the statement 'blank' in a certain column.
If the removal of another words is wished, the function needs to be adjusted.
### interactive_boxplot function
This function produces an interactive boxplot in the browser. Please note that you need to open the html file in your browser (e.g. Firefox, Chrome, Safari) and that JavaScript needs t$
As this is more a little extra but not the main goal of the script, it was added as a function so it can be either called or not.

## Main script
Please see Docstring for detailed explanation of all paramaters.
"TODO" lines indicate where the user may need to change things according to their dataset.
The boxplot is not in a function as this is the main goal of the script and there would be a lot of input arguments which would make the calling ineffective.
### Possible problems
The following problems can arise if the script is not used correctly.
Please note that the name of the dataframe created with the basic_statistics function is used later in the boxplot and saving of the file.
If you name your dataset differently when calling the function, this needs to be adjusted accordingly.The same is true for the dataframe created with the
remove_blanks function. If you rename the dataframe when calling the function, this needs to be adjusted at the bottom of the script when the cleaned dataset is downloaded. 

