#  Gmacht mit ❤️ in Basel
#
#  Copyright (c) 2019 University of Basel
#  Last modified 16/07/2019, 14:03.
#
#  Developed by Tom Cinbis and Tim Königl on 16/07/2019, 14:05

from setuptools import setup

setup(
    name="munki_promoter",
    description="This tool manages Munki packages and utilizes a Jira Kanban"
    "board as an user interface.",
    version="2.0",
    author=[
        "Tom Cinbis",
        "Tim Königl",
        "Client Services Team of the University of Basel IT Services",
    ],
    author_email="cinbist@gmail.com, tim.koenigl@unibas.ch",
    license="GPLv3",
    scripts=["src/munkipromoter.py"],
    packages=["src", "src.core", "src.core.provider", "src.utils"],
    package_data={"src.utils": ["default.ini"]},
    python_requires="~=3.7",
)
