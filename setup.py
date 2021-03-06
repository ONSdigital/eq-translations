from setuptools import setup
from eq_translations import __version__

setup(
    name="eq_translations",
    version=__version__,
    description="Translations infrastructure for EQ Questionnaire Runner",
    url="http://github.com/ONSDigital/eq-translations",
    author="ONSDigital",
    author_email="",
    license="MIT",
    packages=["eq_translations", "eq_translations.cli"],
    entry_points={
        "console_scripts": [
            "extract_template=eq_translations.cli.extract_template:main",
            "translate_census=eq_translations.cli.translate_census:main",
            "translate_schema=eq_translations.cli.translate_schema:main",
            "compare_schemas=eq_translations.cli.compare_schemas:main",
        ]
    },
    install_requires=[
        "babel",
        "jsonpointer",
        "jsonpath-rw",
        "tqdm",
        "requests",
        "termcolor",
    ],
    zip_safe=False,
)
