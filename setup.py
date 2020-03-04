import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fiscal445", 
    version="1.0.1",
    author="Dv8edRoute",
    author_email="dv8edroute@protonmail.com",
    description="Returns 445 Fiscal calendar week and month ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dv8edroute/fiscal445/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
       "pandas >= 1.0.0",
       "numpy"
   ],
)

