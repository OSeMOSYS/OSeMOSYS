# Contributing to OSeMOSYS

We are very grateful that you are looking into how you can contribute to OSeMOSYS.
OSeMOSYS is an amazing project, which has already helped introduce systems
modelling to many new communities.

Contributing to OSeMOSYS is open to everyone who is interested, and we adopt an
inclusive and open policy which is described in our
[code of conduct](./code_of_conduct.md)

Some resources:

- The main OSeMOSYS [website](http://www.osemosys.org/) is a good place to get
  started with OSeMOSYS
- The [forum](https://groups.google.com/forum/#!forum/osemosys) is a great place
  to ask questions and search for answers from our knowledgeable community
- [Sign up](http://www.osemosys.org/news-and-events.html) to our monthly
  newsletter to be the first to learn of the latest developments

## Bugs

If you find a programming error in one of the OSeMOSYS implementations, please
submit an Issue in the relevant repository. Follow the issue template for submitting a bug.

- For the GNU MathProg version, please create a new issue
  [here](http://github.com/OSeMOSYS/OSeMOSYS_GNU_MathProg/issues/new).
- For the GAMS version, please create a new issue
  [here](http://github.com/OSeMOSYS/OSeMOSYS_GAMS/issues/new).
- For the Pyomo version, please create a new issue
  [here](http://github.com/OSeMOSYS/OSeMOSYS_Pyomo/issues/new).
- For the PuLP version, please create a new issue
  [here](http://github.com/OSeMOSYS/OSeMOSYS_PuLP/issues/new).

If you find a more fundamental issue which you think is related with the
formulation of OSeMOSYS, please submit the issue
[here](http://github.com/OSeMOSYS/OSeMOSYS/issues/new).

## Errors, typos or spelling mistakes in the documentation

The documentation can be found in the `docs` directory and is rendered on
[readthedocs](https://osemosys.readthedocs.io/en/latest/).

You can read about contributing to the documentation
[here](./docs/contributing.md)

## Ideas and Suggestions

If you have a great idea for how OSeMOSYS could be improved, or to suggest a
useful addition to the model, please submit a feature request using the Github
issue tracker at [here](http://github.com/OSeMOSYS/OSeMOSYS/issues/new).

Please follow the **OSeMOSYS Enhancement Proposal** issue template.

## Git Workflow

To work with any of the OSeMOSYS code bases, please follow the forking workflow
recommended for contributing to open-source projects. The steps below assume
you have a Github account.

1. Fork the repository to which you wish to contribute by clicking the grey
   `fork` button or visiting https://github.com/osemosys/osemosys/fork
2. Clone your fork of the repository
   `git clone http://github.com/<user>/osemosys`
3. Create a new branch on which you will commit your changes
   `git checkout -b <branchname>`
4. Do the work and stage and commit your changes: `git add ...`,
   `git commit -m "A nice descriptive message"`
5. Push the changes to your fork `git push -u <branchname> origin/<branchname>`
6. Submit a pull request from your fork of the repository to the master branch
   of the original repository.
7. The pull request is reviewed. Any changes required by the review can be
   performed on the same branch and pushed to the forked repo as in the steps
   above.
8. Once the pull request has been reviewed and accepted,
   you may delete your local copy of the branch `git branch -d <branchname>` and
   update your copy of the master branch `git checkout master`,
   `git pull origin master`