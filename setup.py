from setuptools import setup

setup(
    name='NlpToolkit-MorphologicalAnalysis',
    version='1.0.29',
    packages=['MorphologicalAnalysis'],
    url='https://github.com/StarlangSoftware/TurkishMorphologicalAnalysis-Py',
    license='',
    author='olcaytaner',
    author_email='olcay.yildiz@ozyegin.edu.tr',
    description='Turkish Morphological Analysis',
    install_requires=['NlpToolkit-Dictionary', 'NlpToolkit-Corpus', 'NlpToolkit-DataStructure']
)
