#  Gmacht mit ❤️ in Basel
#
#  Copyright (c) 2019 University of Basel
#  Last modified 16/07/2019, 14:03.
#
#  Developed by Tom Cinbis and Tim Königl on 16/07/2019, 14:05

from setuptools import setup, find_packages

setup(
    name="munki_promoter",
    description="This tool manages Munki packages and utilizes a Jira Kanban board as an user interface.",
    version="2.0",
    author=[
        "Tom Cinbis",
        "Tim Königl",
        "Client Services Team of the University of Basel IT Services",
    ],
    author_email="tom.cinbis@unibas.ch, tim.koenigl@unibas.ch",
    license="GPLv3",
    scripts=['src/munkipromoter.py'],
    packages=find_packages(where="src"),
    package_dir={"": "src"},
)
