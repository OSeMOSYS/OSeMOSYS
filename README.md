# OSeMOSYS - Open Source Energy Modelling System

[![Build Status](https://travis-ci.com/OSeMOSYS/OSeMOSYS.svg?branch=master)](https://travis-ci.com/OSeMOSYS/OSeMOSYS)
[![Documentation Status](https://readthedocs.org/projects/osemosys/badge/?version=latest)](https://osemosys.readthedocs.io/en/latest/?badge=latest)

Welcome to OSeMOSYS - the open source energy modelling system. This source code
repository contains the Apache-2.0 licensed source-code for three different
flavours of OSeMOSYS - GNU MathProg, Python and GAMS.
The different versions are contained in subfolders, together with readme files
which provide information of how to install and run the code.

## Background

OSeMOSYS is a full-fledged systems optimization model generator for long-term
energy planning.
Unlike long established energy systems models,
such as MARKAL/TIMES (ETSAP, 2010), MESSAGE (IAEA, 2010), PRIMES (NTUA, 2010),
EFOM (Van der Voort, 1982) and POLES (Enerdata, 2010),
OSeMOSYS potentially requires a less significant learning curve and time
commitment to build and operate. 
Additionally, by not using proprietary software or commercial programming
languages and solvers, OSeMOSYS requires no upfront financial investment.
These two advantages extend the availability of energy modeling 
to large communities of students, business analysts, government specialists
and developing countries energy researchers.

## Motivation

OSeMOSYS is designed to fill a gap in the analytical toolbox available to the energy research community and energy planners in developing countries. At present there exists a useful, but limited set of accessible energy system models. These tools often require significant investment in terms of human resources, training and software purchases in order to apply or further develop them. In addition, their structure is often such that integration with other tools, when possible, can be difficult.

## Energy Specialists

The OSeMOSYS code is relatively straightforward and transparent and allows for simple refinements and the ability to conduct sophisticated analyses. As models are made to generate insights, OSeMOSYS allows a test-bed for new energy model developments.

## Education

Enabling graduate students to build and iteratively develop formal energy models will impart this knowledge base to very wide range of energy market roles and positions. Extending the human capacity of private and public policy makers to use and understand energy models is a key step in the effective use and interpretation of formal analytical tools. And growing human capacity in energy modeling in developing countries – whose institutions have relatively fewer research resources – is particularly important, given the growth of developing countries in energy related emissions, resource use, and demand for energy services. 

## Community

OSeMOSYS community welcomes professionals and experts from different levels: decision makers, policy officers, energy planners, developers of new model functionalities, programmers.

## Getting the OSeMOSYS code

### Modellers

The OSeMOSYS code packages you need for writing your own models are released on the
[website](http://www.osemosys.org/get-started.html), along with a lot of useful
information on how to get started.

### Developers

OSeMOSYS consists of this repository and several submodules, which contain the different language implementations of
the OSeMOSYS formualation.

To obtain all the OSeMOSYS code including the language implementations 
for development purposes, run the following commands from your command line:

```bash
cd <name_of_folder>
git clone https://github.com/OSeMOSYS/OSeMOSYS # obtain the OSeMOSYS repository code
git submodule init # initialize your local submodule configuration file
git submodule update # fetch all the data from project and check out correct commit
```

If successful, this should download all the code to the folder you specified in
the first step.

Alternatively, use the `--recurse-submodules` argument to the `git clone` command:

```bash
cd <name_of_folder>
git clone https://github.com/OSeMOSYS/OSeMOSYS --recurse-submodules
# obtain the OSeMOSYS repository code and submodules all in one line
```
