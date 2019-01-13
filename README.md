# Plagiarism Detection System for Academic Texts

Plagiarism detection is an integral part of publishing academic papers. This project was an attempt to create a system for plagiarism detection that deals with academic texts written in the Macedonian language. To the best of my knowledge, this is the first attempt for such a system in this language.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine.

### Prerequisites

This project works currently only on Ubuntu 16.04.4 LTS. The system requires the following third-party tools.

* [Python 3.6](https://www.python.org/downloads/) - the programming language in which the program is written in.
* [Pip](https://pypi.org/project/pip/) - a tool for installing Python packages.
* [PyQt4](https://pypi.org/project/PyQt4/) - this tool helps in creating a Graphical User Interface.

### Directory structure

- main.py
   This module allows you to run the GUI.
- ./modules/plagiarism_detection.py
   The module that wraps up all of the plagiarism detection steps.
- ./modules/preprocessing.py
   This module prepares the data for processing and similarity calculation afterward.
- ./modules/similarity.py
   This module is responsible for calculating the similarity for all of the different categories.
- ./modules/user_interface.py
   This module is responsible for all of the code connected to the GUI.


### Running

In order to run the program, the user needs to enter the home directory of the project and the following command on the terminal should be run:

```
$ sudo ./main.py

```

The above command starts the program and a window pops up. There the user has the option to select which academic texts he/she wants to compare. In addition the user has the option to select custom categories for comparison: text, paraphrased text, style (frequencies of certain word groups) and references. All of the selected categories contribute to the final score. After the plagiarism detection is performed, the user has the option to check for more details for the similarities in each of the categories.

## Authors

* Stevica Bozhinoski stevica.bozhinoski@tum.de

## Acknowledgments

I would like to thank my professor and mentor prof. pr. Katerina Zdravkova for her guidance and support during this project.
