from setuptools import setup

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

setup(
    name='NlpToolkit-MorphologicalAnalysis',
    version='1.0.42',
    packages=['MorphologicalAnalysis', 'MorphologicalAnalysis.data', 'DisambiguationCorpus'],
    package_data={'MorphologicalAnalysis.data': ['*.xml']},
    url='https://github.com/StarlangSoftware/TurkishMorphologicalAnalysis-Py',
    license='',
    author='olcaytaner',
    author_email='olcay.yildiz@ozyegin.edu.tr',
    description='Turkish Morphological Analysis',
    install_requires=['NlpToolkit-Dictionary', 'NlpToolkit-Corpus', 'NlpToolkit-DataStructure'],
    long_description=long_description,
    long_description_content_type='text/markdown'
)
