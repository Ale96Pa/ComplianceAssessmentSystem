# A compliance assessment system for Incident Management process

## Abstract 

The Incident Management (IM) process is one of the core activities for increasing the overall security level of organizations and better responding to cyber attacks. Different security frameworks (such as ITIL and ISO 27035) provide guidelines for designing and properly implementing an effective IM process. Currently, assessing the compliance of the actual process implemented by an organization with such frameworks is a complex task. The assessment is mainly manually performed and requires much effort in the analysis and evaluation. In this paper, we first propose a taxonomy of compliance deviations to classify and prioritize the impacts of non-compliant causes. We combine trace alignment techniques with a new proposed cost model for the analysis of process deviations rather than process traces to prioritize interventions. We put these contributions into use in a system that automatically assesses the IM process compliance with a reference process model (e.g., the one described in the chosen security framework). It supports the auditor with increased awareness of process issues to make more focused decisions and improve the process’s effectiveness. We propose a benchmark validation for the model, and we show the system’s capability through a usage scenario based on a publicly available dataset of a real IM log.

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

## Cite this work

```
@article{PALMA2024104070,
title = {A compliance assessment system for Incident Management process},
journal = {Computers & Security},
volume = {146},
pages = {104070},
year = {2024},
issn = {0167-4048},
doi = {https://doi.org/10.1016/j.cose.2024.104070},
url = {https://www.sciencedirect.com/science/article/pii/S0167404824003754},
author = {Alessandro Palma and Giacomo Acitelli and Andrea Marrella and Silvia Bonomi and Marco Angelini},
keywords = {Incident management, Security governance, Process compliance assessment, Cost model, Trace alignment},
}
```
