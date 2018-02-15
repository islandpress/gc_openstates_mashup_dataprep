# Overview
This project is for obtaining and preparing location data about climate change bills and environmental organizations.

# Setup
## Package Installs
* Download and install conda:
<https://conda.io/docs/install/quick.html>

* Setup a virtual environment for python 3
`conda create -n osgc python=3`
`source activate osgc`

* Install packages in pip that aren't found in conda
`pip install -r requirements.txt`

* Deactivate the conda session when finished
`source deactivate osgc`

## API Keys

Get an Open States API key and set it in environment
variable: OPEN\_STATES\_API\_KEY

For obtaining the key, see:

* <http://docs.openstates.org/en/latest/api/>
* <https://openstates.org/api/register/>


# Running
* Get Open States bill name and state data:
	* `python openstates.py os.csv`
* Get Green Commons orgs profile name and address data, as well as State lookup data:
	* `python greencommons.py gc.csv lu.csv`
