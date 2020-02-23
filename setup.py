import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ucc2stl-chfrag",
    packages=["ucc2stl"],
    version="0.0.1",
    description="Calculates the outer shell of unit cube complexes",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Christodoulos Fragkoudakis",
    author_email="chfrag@mail.ntua.gr",
    url="http://ucc2stl.heroku.com",
    download_url="http://ucc2stl.heroku.com/download/ucc2srl-0.0.1.tgz",
    keywords=["fea", "stl"],
)
