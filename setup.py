from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()


setup(
    name='perfectextractor-ui',
    version='0.1.1',
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
    packages=['perfectextractor_ui'],
    python_requires='>=3.6',
    install_requires=['django-widget-tweaks',
                      'perfectextractor'])
