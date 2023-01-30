from setuptools import setup, find_packages
from distutils.core import setup 

with open('README.md') as f:
    README = f.read()
  
# Calling the setup function
setup(
      name = 'as2orgplus',
      version = '1.0.0',
      license="MIT",
      packages=find_packages(),
      install_requires=['numpy', 'pandas',],
      python_requires='>=3',
      author ='Augusto Arturi and Esteban Carisimo',
      author_email = 'esteban.carisimo@northwestern.edu',
      url = 'https://github.com/NU-AquaLab/as2orgplus',
      description = 'AS-to-Organization mappings with PeeringDB data',
      long_description=README,
      keywords='Autonomous Systems, AS2Org',
      classifiers=[
            # Trove classifiers
            # (https://pypi.python.org/pypi?%3Aaction=list_classifiers)
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
            'Topic :: System :: Networking :: Monitoring',
            'Intended Audience :: Science/Research',
      ],
      entry_points={'console_scripts': ['pdb2org=tools.pdb2org:main',],}
)