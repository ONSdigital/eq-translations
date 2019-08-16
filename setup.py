from setuptools import setup

setup(name='eq_translations',
      version='0.2',
      description='Translations infrastructure for EQ Questionnaire Runner',
      url='http://github.com/ONSDigital/eq-translations',
      author='ONSDigital',
      author_email='',
      license='MIT',
      packages=['eq_translations', 'eq_translations.cli'],
      entry_points = {
          'console_scripts': [
              'template_extractor=eq_translations.cli.template_extractor:main',
              'translate_all_surveys=eq_translations.cli.translate_all_surveys:main',
              'translate_census=eq_translations.cli.translate_census:main',
              'translate_survey=eq_translations.cli.translate_survey:main',
              'compare_schemas=eq_translations.cli.compare_schemas:main',
          ]
      },
      install_requires=[
          'babel',
          'jsonpointer',
          'tqdm',
          'requests'
      ],
      zip_safe=False)

