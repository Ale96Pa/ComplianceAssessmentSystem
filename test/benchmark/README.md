# Compliance Assessment System - BENCHMARK

### Refer to this [work](https://github.com/Ale96Pa/BenchIMP) (https://github.com/Ale96Pa/BenchIMP) for a more extensive benchmark.

## Description

This bennshark contains the scripts (in the folder _test_) and the results (in the folder _benchmark_) to reproduce the validation.
The system can be configured as well to set most suitable the parameters as for the system execution.
The zip folder contains the set of all the experiments for the approaches presented in the paper.

## Installation requirement

The following libraries are required for the correct execution:

- pip install pm4py
- pip install matplotlib
- pip install numpy
- pip install pandas

## Configuration

If you want to just reproduce a simplified run of the benchmark, then follow the installation instructions.

If you want customize your assessment, then add in the _inputs_ folder:

- your log file in csv or xes format;
- your target process model in petri net format (pnml)

In addition, the following configurations are settable in the file _config.py_:

- log and model paths;
- separator (in case of csv file with a separator different from comma), case ID attribute name (case_k), process activities attribute name(activity_key), timestamp attribute name (timestamp_key), cost attribute name (cost_key), trace category attribute name (category_key);

Notice: if your dataset does not have a non-compliance cost attribute, you can ALWAYS use the "fitness_cost" attribute, automatically evaluated with trace alignment algorithms.

## Installation

Download this github repositiory, set the configuration (if any) and run the command from your terminal:

$ python -u "<path_to_this_folder>\test\benchmark_main.py"
