from setuptools import setup, find_packages

setup(name='some_project',
      version='1.0',
      # python_requires='==3.6',
      packages=find_packages(),
      include_package_data=True,
      description='.......',
      author='Alex',
      license='Unlicense',
      install_requires=[
          'Keras==2.1.5',
          'tensorflow-gpu==1.6.0',
          'h5py',
          'numpy',
          'argparse',
          'Pillow',
          'matplotlib',
      ],
      zip_safe=False)
