import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fea2stl-chfrag",
    packages=["fea2stl"],
    version="0.0.1",
    description="Calculates the outer shell of unit cube complexes",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Christodoulos Fragkoudakis",
    author_email="chfrag@mail.ntua.gr",
    url="http://fea2stl.heroku.com",
    download_url="http://fea2stl.heroku.com/download/fea2srl-0.0.1.tgz",
    keywords=["fea", "stl"],
)
