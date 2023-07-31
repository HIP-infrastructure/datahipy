.. _contributing:

*************
Contributing 
*************

This project follows the `all contributors specification <https://allcontributors.org/>`_. Contributions in many different ways are welcome!

Contribution Types
------------------

Report Bugs
~~~~~~~~~~~

Report bugs at https://github.com/HIP-infrastructure/datahipy/issues.

If you are reporting a bug, please include:

* Your operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.

Fix Bugs
~~~~~~~~

Look through the GitHub issues for bugs. Anything tagged with "bug" and "help wanted" is open to whoever wants to implement it.

Implement Features
~~~~~~~~~~~~~~~~~~

Look through the GitHub issues for features. Anything tagged with "enhancement" and "help wanted" is open to whoever wants to implement it.

Write Documentation
~~~~~~~~~~~~~~~~~~~

`DataHIPy` could always use more documentation, whether as part of the official `datahipy` docs, in docstrings, or even on the web in blog posts, articles, and such.

Submit Feedback
~~~~~~~~~~~~~~~

The best way to send feedback is to create an issue at https://github.com/HIP-infrastructure/datahipy/issues.

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that contributions
  are welcome :)

Get Started!
------------

Ready to contribute? Here's how to set up `DataHIPy` for local development.

1. Fork the repository of `DataHIPy` on GitHub.

2. Clone your fork locally::

    git clone git@github.com:your_name_here/datahipy.git
    cd datahipy

3. Create a branch for local development::

    git checkout -b name-of-your-bug-fix-or-feature

4. Now you can make your changes locally.

.. important::
	Please keep your commit the most specific to a change it describes. It is highly advice to track unstaged files with ``git status``, add a file involved in the change to the stage one by one with ``git add <file>``. The use of ``git add .`` is highly disencouraged. When all the files for a given change are staged, commit the files with a brieg message using ``git commit -m "<type>[optional scope]: <description>"`` that describes your change and where ``<type>`` can be ``fix`` for a bug fix, ``feat`` for a new feature, ``refactor`` for a code change that neither fixes a bug nor adds a feature, ``docs`` for documentation, ``ci`` for continuous integration testing, and ``test`` for adding missing tests or correcting existing tests. This follows the Angular conventional commits, please see https://www.conventionalcommits.org/en/v1.0.0-beta.4/ for more details.

5. When you're done making changes, push your branch to GitHub::

    git push origin name-of-your-bugfix-or-feature

6. Submit a pull request through the GitHub website.

   .. important::
       Please make sure that the pull request is made against the ``dev`` branch. The ``master`` branch is used for the stable version releases of `DataHIPy`.

Pull Request Guidelines
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Before you submit a pull request, check that it meets these guidelines:

1. If the pull request adds functionality, the docs should be updated (See :ref:`documentation build instructions <instructions_docs_build>`). 

2. Make sure that the tests pass (See :ref:`instructions for testing <instructions_tests>` )

CI/CD Pipeline: Under the Hood
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

`DataHIPy` has a `mirror repository on GitLab <https://gitlab.hbp.link/hip/datahipy>`_ that is synced with a `GitHub Action <https://github.com/HIP-infrastructure/datahipy/actions/workflows/gitlab-sync.yml>`_, and that is used for continuous integration (CI) and continuous deployment (CD).

The pipeline, described by the file `.gitlab-ci.yml <https://github.com/HIP-infrastructure/datahipy/blob/master/.gitlab-ci.yml>`_, consists of the following stages:

    1. `test-install-python`: install Python and the dependencies of DataHIPy in a Docker container.

    2. `build`: Build the Docker image of DataHIPy in the GitLab Container Registry (Login to the GitLab Container Registry is done using the ``$CI_REGISTRY_USER`` and ``$CI_REGISTRY_PASSWORD`` environment variables).

    3. `test`: Run the tests with pytest using the built Docker image. Send the coverage report to `codecov.io <https://codecov.io/gh/HIP-infrastructure/datahipy>`_ using the ``$CODECOV_TOKEN`` environment variable.

    4. `clean`: Clean the Docker container.

    5. `semantic-release`: Make a version release of DataHIPy with semantic-release. This updates the version tag of DataHIPy, updates ``docs/CHANGES.md``, commits the changes, and creates a new tag on GitLab using ``$GL_TOKEN`` environment variable. The configuration of semantic-release is described by the file `.releaserc.json <https://github.com/HIP-infrastructure/datahipy/blob/master/.releaserc.json>`_. It uses the ``dev`` branch for beta releases and the ``master`` branch for stable releases.

    6. `deploy-release`: Build the Docker image with the new version of DataHIPy and push it to the GitLab Container Registry. This stage takes also care of pushing the changes and tags made by ``semantic-release`` stage to GitHub using SSH. A private key on gitlab is read from ``$SSH_PRIVATE_KEY`` variable and set in ``.gitlab-ci.yml``.

Depending on the event, the pipeline will run all the stages of the CI/CD pipeline or only a subset of them.

The diagram below shows the different stages of the pipeline and the events that trigger them:

.. mermaid::

    graph LR

    subgraph "Stages"
    test_python_install["test-python-install"]
    build["build"]
    test["test"]
    clean["clean"]
    semantic_release["semantic-release"]
    deploy_release["deploy-release"]
    end

    test_python_install --> build
    build --> test
    test --> clean
    clean -->|if $CI_COMMIT_REF_NAME == master or $CI_COMMIT_REF_NAME == dev| semantic_release

    semantic_release --> deploy_release

When a new branch is pushed on GitHub or a new commit is pushed to an existing branch (different than ``master`` or ``dev``) on GitHub, then only the stages `test-install-python`, `build`, `test`, `clean` are executed.

When a Pull Request towards the ``dev`` and ``master``branches is opened, updated, or merged on GitHub, then only the additional stages `semantic-release` and `deploy-release` are executed.


Not listed as a contributor?
----------------------------

This is easy, `DataHIPy` has the `all contributors bot <https://allcontributors.org/docs/en/bot/usage>`_ installed.

Just comment on Issue or Pull Request (PR), asking `@all-contributors` to add you as contributor::

    @all-contributors please add <github_username> for <contributions>

`<contribution>`: See the `Emoji Key Contribution Types Reference <https://github.com/all-contributors/all-contributors/blob/master/docs/emoji-key.md>`_ for a list of valid `contribution` types.

The all-contributors bot will create a PR to add you in the README and reply with the pull request details.

When the PR is merged you will have to make an extra Pull Request where you have to:

    1. add your entry in the `.zenodo.json` (for that you will need an ORCID ID - https://orcid.org/). Doing so, you will appear as a contributor on Zenodo in the future version releases of DataHIPy. Zenodo is used by DataHIPy to publish and archive each of the version release with a unique Digital Object Identifier (DOI), which can then be used for citation.

    2. update the content of the table in `documentation/contributors.rst` with the new content generated by the bot in the README. Doing so, you will appear in the :ref:`Contributing Page <contributing>`.

------------

This document has been inspired and adapted from `these great contributing guidelines <https://github.com/dPys/PyNets/edit/master/docs/contributing.rst>`_.
