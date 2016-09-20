from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()


setup(
    name='merge_closest',
    version='0.1b160919_2',
    description='Merge two pandas DataFrames using closest match',
    long_description=readme(),
    keywords='pandas merge join closest approximate',
    url='https://github.com/RobinFiveWords/merge_closest',
    author='Robin Fishbein',
    author_email='robinfishbein@yahoo.com',
    license='MIT',
    packages=['merge_closest'],
    install_requires=[
        'pandas',
        'numpy',
    ],
    include_package_data=True,
    zip_safe=False,
)
