# Project Guide

This project covers **graph-coloring** and **domino-tiling** problems, encoded as SAT formulae and solved using the clasp SAT solver. Follow the instructions below to install clasp, generate CNF files, solve them, and apply optimization modes.

### Requirements
- **clasp** must be preinstalled to solve SAT encodings.

### clasp Installation
To install clasp, please follow the instructions on the [clasp GitHub page](https://github.com/potassco/clasp.git).

### Instructions

1. **Generate CNF files**:
   - To create the CNF files for graph-coloring or domino-tiling encodings, run:
     ```bash
     python file_name
     ```

2. **Solve CNF files using clasp**:
   - Use the following command to solve generated CNF files:
     ```bash
     clasp file_name
     ```

3. **Run Optimizations for Various Modes**:
   - Place the required CNF files in the `cnf_files` folder for analysis or optimization. Automation is done here, using bash files and python files, as these apply many methods, store the results in csv files, then plot them as required.
   - Execute the bash script:
     ```bash
     bash bash_file_name
     ```
   - Run the Python script for plotting results:
     ```bash
     python plotting_python_file_name
     ```
