from setuptools import setup, find_packages

setup(
    name="munki_promoter",
    description="This tool manages Munki packages and utilizes a Jira Kanban board as an user interface.",
    version="2.0",
    author="Tom Cinbis",
    author_email="tom.cinbis@unibas.ch",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
)
