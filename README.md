# openHTS
Software for generating media libraries for high-throughput screening via OpenTrons pipetting robots.


## Installation
We develop openHTS primarily using conda for package management. The conda environment file in the repository root directory ('environment.yaml') specifies all the necessary packages for installation. You can download and install all dependencies in a conda environment by navigating to the openHTS root directory in the commandline and entering this command:

```
conda env create -f environment.yml
```

Below is a summary of folders in the repository.

## test
Contains scripts for performing software tests and generating test files (e.g., simulated input)

## sandbox
Contains in-progress methods that need testing on the OT-2 prior to being moved into the main package. The sandbox should be cleaned of all code remnants after a new method has been migrated out of the sandbox.