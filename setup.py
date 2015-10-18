from setuptools import setup

setup(
    name='fatsort-wrapper',
    version='0.1',
    packages=['fatsort_wrapper'],
    url='',
    license='MIT',
    author='Margus Laak',
    author_email='margus.laak@redfunction.ee',
    description='Automatically sort and unmount all vfat filesystems',
    entry_points = {
              'console_scripts': [
                  'fatsort_wrapper = fatsort_wrapper.__main__:main',
              ],
          },
)
