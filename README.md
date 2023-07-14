# SeedTree



## Dependencies
To run the simulation-code, it is sufficient to install the module ```bitstring```.

For the plotting functionality, other packages, such as ```seaborn``` are used. A detailed list can be found in ```requirements.txt```. 

## Experiments

The experimentation code can be found in ```simulation/server_experiment.py```. It fetches the datasets from ```temp-seq``` and ```real-seq``` and uses the code of the ```pushdown``` folder to run the algorithms on the defined data-structure.

### Experiment setup

We advise to use PyCharm (it offers the possibility to take care of the dependencies) and set the working directory to the parent folder ``` .\SeedTree\ ```.

### Run the experiments

All relevant experiments can be run from ```main.py``` in the ```simulation``` folder. The output will be printed on the console and logged in the ```results``` folder.


## Plotting

The logged results have partly been normalized before being manually inserted into the ```.py``` files of ```visualization```. The plotting code can be found in the latter folder.

An exception has been made to generate ```Fig. 4.c)```, for which we take the data from ```Results_f_c12_sns.xlsx``` in ```results```.
