import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="guildeduapy",
    version="0.0.1",
    author="ComfyDev",
    author_email="comfydev@protonmail.com",
    description="Wrapper for the Guilded user API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/TheComfyDev/guildeduapy",
    project_urls={
        "Bug Tracker": "https://github.com/TheComfyDev/guildeduapy/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: No License Yet...",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "."},
    packages=setuptools.find_packages(where="."),
    python_requires=">=3.6",
)
