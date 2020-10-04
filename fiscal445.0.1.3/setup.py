import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fiscal445", 
    version="0.1.3",
    author="Dv8edRoute",
    author_email="dv8edroute@protonmail.com",
    license="MIT",
    description="445 Fiscal calendar ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dv8edroute/fiscal445/tree/master/fiscal445.0.1.3",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Office/Business :: Financial :: Accounting",
    ],
    python_requires='>=3.6',
    install_requires=[
       "pandas>=0.25.3",
       "numpy"
   ],
)

