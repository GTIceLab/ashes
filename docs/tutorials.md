# Tutorials

## Instructions for Contributing and Building Documentation Site
The following instructions details how to setup and build a local site for the ASHES documentation. This documentation site is built with Mkdocs with the Material theme.

1. Navigate to the directory `ashes/`
2. Checkout the `ORS2526` branch.
3. Execute `python -m venv .env` to create a Python virtual environment.
4. Execute `source .env/bin/activate` to activate the environment.
5. Execute `python -m pip install -r requirements.txt` to install necessary dependencies for mkdocs.
6. To edit the documentation, simply edit the markdown file inside `ashes/docs/` you believe your notes should go into. You can also create another markdown file, which will create a new page in the documentation accessible through the left sidebar.
7. Execute `mkdocs build` to build the documentation site after any updates to the docstrings or markdown files under `ashes/docs/`.
8. From here, you have a couple of different directions to view your updates in the form of a published website:
   1. Execute `mkdocs serve` to setup a site on you local machine. Your site will probably be served at the local address `http://127.0.0.1:8000/`, which you can copy into a preferred web browser. This is useful for quick preview of how your changes will be rendered on the live site.
   2. Execute `mkdocs gh-deploy` to send your updates to be deployed by Github. What happens is the built documentation is pushed to the `gh-pages` branch in the `ashes` repository, and the repository will automatically deploy any updates it sees in `gh-pages`. After a couple minutes, your updates will show up in the live documentation deployed at `https://gticelab.github.io/ashes/`.

For additional information and guides, please visit the [Official MkDocs Documentation](https://www.mkdocs.org/) or the [Material for MkDocs Documentation](https://squidfunk.github.io/mkdocs-material/).
