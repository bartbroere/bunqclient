from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()


setup(
    name='bunqclient',
    version='2020.10.30',
    description='Python client for the bunq public API',
    long_description=readme(),
    keywords=["bunq", "client", "bank", "api", "bunqclient"],
    packages=['bunqclient'],
    url='https://github.com/bartbroere/bunqclient/',
    license='MIT',
    author='Bart Broere',
    author_email='mail@bartbroere.eu',
    install_requires=['requests', 'pycryptodome'],
    python_requires='>=2.7,>=3.5',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Office/Business :: Financial',
        'Topic :: Utilities',
    ],
)
