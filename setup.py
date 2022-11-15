import ast
import os.path

from setuptools import setup

try:
    from eq_translations import __version__ as version
except ImportError:
    version = str(
        ast.literal_eval(
            open(
                os.path.join(
                    os.path.dirname(__file__), "eq_translations", "__init__.py"
                ),
                "r",
            )
            .read()
            .split("=")[-1]
            .strip()
        )
    )

setup(
    name="eq_translations",
    version=version,
    description="Translations infrastructure for EQ Questionnaire Runner",
    url="http://github.com/ONSdigital/eq-translations",
    author="ONSDigital",
    author_email="",
    license="MIT",
    packages=["eq_translations", "eq_translations.cli"],
    entry_points={
        "console_scripts": [
            "extract_template=eq_translations.cli.extract_template:main",
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
