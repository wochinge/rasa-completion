from setuptools import setup, find_packages

setup(
    name="rasa-cli-completion",
    version="0.1.1",
    packages=find_packages(),
    license="Apache 2.0",
    maintainer="Tobias Wochinger",
    maintainer_email="tobias.wochinger@gmail.com",
    description="Bash / Zsh autocomplete script for Rasa",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    install_requires=["rasa~=1.3"],
    tests_require=["pytest>=4.5,<7.0", "black~=19.10b0"],
    project_urls={
        "Bug Reports": "https://github.com/wochinge/rasa-cli-completion/issues",
        "Source": "https://github.com/wochinge/rasa-cli-completion",
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        # supported python versions
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Software Development :: Libraries",
    ],
    python_requires=">=3.6",
    package_data={"": ["*.sh"]},
)
