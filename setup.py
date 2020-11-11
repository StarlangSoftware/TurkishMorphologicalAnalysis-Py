from setuptools import setup

setup(
    name='NlpToolkit-MorphologicalAnalysis',
    version='1.0.23',
    packages=['MorphologicalAnalysis'],
    url='https://github.com/olcaytaner/TurkishMorphologicalAnalysis-Py',
    license='',
    author='olcaytaner',
    author_email='olcaytaner@isikun.edu.tr',
    description='Turkish Morphological Analysis',
    install_requires=['NlpToolkit-Dictionary', 'NlpToolkit-Corpus', 'NlpToolkit-DataStructure']
)
