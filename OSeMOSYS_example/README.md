# Example OSeMOSYS Implementation

This folder demonstrates the required structure for implementations of the
OSeMOSYS formulation.

```bash
OSeMOSYS_example $ tree
.
├── README.md
├── docs
│   └── index.md
└── scripts
    └── README.md
├── src
    └── README.md
```

## Creating a new implementation

Create a new git repository containing your OSeMOSYS implementation, and copy
in the contents of the `OSeMOSYS_example` folder.

### Ensure your implementation can be run from the command line

The implementation should be runnable from the command line, taking the input
location, and output location as arguments.

For example, create a script which runs your implementation with any pre- and post- processing.

```bash
INPUT_LOCATION=$1
OUTPUT_LOCATION=$1
scripts/pre-processing.sh $INPUT_DATA > data/pre_processed.dat
src/my_implementation.sh data/pre_processed.dat > data/results.dat
scripts/post_processing.sh data/results.dat $OUTPUT_LOCATION
```

This script could then be called as follows:

```bash
run.sh ./my_project/input_data ./my_project/results
```

You may like to use a Makefile to run the pipeline of pre-processing -> run the model -> post-process the results.

### Ensure that your implementation can read and run the example models

The example model definitions can be found in `./examples`.

### Ensure that your implementation writes results in the common format

Implementations should write their results into the common format detailed in
the documentation.

## Adding your implementation to the main OSeMOSYS repository

When you have finished creating your new implementation of OSeMOSYS, submit a
pull request at http://github.com/OSeMOSYS/OSeMOSYS in which you add your
implementation as a submodule.

For example, first [fork](https://github.com/OSeMOSYS/OSeMOSYS/fork)
the OSeMOSYS code on Github. Then, add your implementation
as a submodule, and push your changes to your fork:

```bash
git clone http://github.com/my_name/OSeMOSYS # clone the main repository
git branch my_implementation
git checkout my_implementation
git add submodule http://github.com/my_name/my_implementation OSeMOSYS_my_implementation
git push
```

Finally submit a pull request.

As part of the process of reviewing a new implementation of OSeMOSYS, we need to
setup the continuous integration tests to check that the results from running the
example model files match those of the other implementations. This is due to the
principle of harmonisation between OSeMOSYS implementations.
