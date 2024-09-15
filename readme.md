# Homebuyer Allocation Algorithm

## Overview

This project implements an algorithm for assigning homebuyers to neighborhoods based on their preferences and scores. The goal is to match homebuyers with neighborhoods that best fit their needs while respecting constraints and priorities.

## Table of Contents

1. [Project Description](#project-description)
2. [Usage](#usage)
3. [Directory Structure](#code-structure)
4. [Algorithm Details](#algorithm-details)

## Project Description

The Homebuyer Allocation Algorithm is designed to match homebuyers with neighborhoods based on various attributes and preferences. The core functionality includes parsing input data, processing preferences, and generating allocation results.

## Usage

To get started with this project, just clone the repository and run `main.py`:

```bash
git clone https://github.com/pedrohnq/neighborhood_match.git
cd neighborhood_match
python3 main.py
```

## Directory Structure

### `data/`

The `data/` directory contains the input and output files used by the project.

- **`input.txt`**: This is the input file containing the data required by the algorithm. It should include information about neighborhoods and homebuyers, formatted according to the expectations of the allocation script.

- **`output.txt`**: This is the output file where the result of the homebuyer-to-neighborhood allocation is saved. The content of this file is generated after the algorithm is executed, reflecting the final allocation based on preferences and scores.

### `entities/`

The `entities/` directory contains the definitions of the main entities used in the project, which are used to represent and manipulate data related to neighborhoods and homebuyers.

- **`__init__.py`**: Initializes the `entities` module, allowing the classes defined in this directory to be imported.

- **`base.py`**: Defines the base class for all entities. This class may include common attributes and methods used by other classes, such as `HomeBuyer` and `Neighborhood`.

- **`homebuyer.py`**: Defines the `HomeBuyer` class. This class represents a homebuyer and includes attributes related to their preferences and scores, as well as methods for setting and manipulating this information.

- **`neighborhood.py`**: Defines the `Neighborhood` class. This class represents a neighborhood and includes attributes related to its characteristics and methods for manipulating and accessing this information.

### `algorithm/`

The `algorithm/` directory contains the implementation of the algorithm that allocates homebuyers to neighborhoods.

- **`__init__.py`**: Initializes the `algorithm` module, allowing the functions and classes defined in this directory to be imported.

- **`place_homebuyers_in_neighborhoods.py`**: Contains the core logic of the algorithm that assigns homebuyers to neighborhoods based on their preferences and scores. This script manages data reading, algorithm execution, and result writing.

Each of these directories and files serves a specific role in the organization and functionality of the project, helping to keep the code modular and maintainable.