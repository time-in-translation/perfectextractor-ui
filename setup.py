import setuptools


def readme():
    with open('README.md') as f:
        return f.read()


setuptools.setup(
    name='perfectextractor-ui',
    version='0.1.6',
    author='Ben Bonfil',
    author_email='bonfil@gmail.com',
    description='A web frontend for perfectextractor',
    long_description=readme(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'Topic :: Text Processing :: Linguistic',
    ],
    url='https://github.com/time-in-translation/perfectextractor-ui',
    license='MIT',
    packages=setuptools.find_packages(),
    include_package_data=True,
    python_requires='>=3.6',
    install_requires=['django-widget-tweaks',
                      'perfectextractor'])
