Testing
=======

The main OSeMOSYS repository uses Travis CI to run regression tests and
harmonisation tests across each of the OSeMOSYS implementations.

Each push to a branch on the OSeMOSYS repository, or submission of a pull
request triggers a build on Travis, with the corresponding status reported
back in the pull request comments.

The tests must pass before a pull request may be merged into the main
repository.

Tests are defined using the Python package ``pytest`` and the runs are
configured within the Travis CI configuration file ``.travis.yml``.

The tests are stored in the ``tests`` folder.

Versioning
==========

We intend to follow semantic versioning, with major versions for any
backwards incompatible changes to the model formulation.
Note that tags should follow semantic versioning.

Releases
--------

Each of the OSeMOSYS implementations is deployed to Github Releases as a
separate package within the release.

If a tag is pushed to the master branch on the main OSeMOSYS project
Travis CI runs regression and harmonisation tests across the various
implementations, and if successful, run the build and deployment scripts.

Deployment to Github Releases is handled by Travis CI, and the versions
are controlled by git tags.

Make a new release
------------------

First update the CHANGELOG.rst with a short summary of fixes and new
features. Commit message summaries should give a reasonable starting point:

    git log v1.1.0..HEAD –oneline

To make a release, create an annotated tag:

    git tag -a v0.2.0       # create annotated tag (will need a message)
    git describe            # show current commit in relation to tags

You’ll need to specify you tag to push either using the --tags flag or the tag name:

    git push upstream master --tags
    git push upstream v0.2.0        # alternatively

This will trigger the Travis deploy stage which publishes to Github Releases
