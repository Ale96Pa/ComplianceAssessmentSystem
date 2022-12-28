# Compliance Assessment System

## Description

This system is a process compliance assessment system that can be used by a process analyst to detect and analyze process deviations particularly dangerous.
The inputs are a process log and the target process model (see configuration section for details).
The output is a pdf with analyses about the _non-compliance cost_ trend, the analysis of _severity_ to detect particularly dangerous combination of deviations, the weigths of each single _cost component_ (i.e., deviation), the _detailed assessment_ of the specific activities causing errors in the process, and _trace analysis_ basing on a feature in the log characterizing categories of traces (i.e., incident types).

## Installation requirement

The following libraries are required for the correct execution:

- pip install pm4py
- pip install matplotlib
- pip install numpy
- pip install pandas

## Configuration

If you want to just reproduce a simplified run of the system, then follow the installation instructions.

If you want customize your assessment, then add in the _inputs_ folder:

- your log file in csv or xes format;
- your target process model in petri net format (pnml)

In addition, the following configurations are settable in the file _config.py_:

- log and model paths;
- separator (in case of csv file with a separator different from comma), case ID attribute name (case_k), process activities attribute name(activity_key), timestamp attribute name (timestamp_key), cost attribute name (cost_key), trace category attribute name (category_key);

Notice: if your dataset does not have a non-compliance cost attribute, you can ALWAYS use the "fitness_cost" attribute, automatically evaluated with trace alignment algorithms.

## Installation

Download this github repositiory, set the configuration (if any) and run the command from your terminal:

$ python -u "<path_to_this_folder>\src\main.py"
