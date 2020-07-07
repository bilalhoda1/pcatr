from setuptools import setup

setup(name="PCATR",
    version="0.0.2",
    description="PCATR is a closed source, non-licensed Python library providing efficient, \
        easy-to-use algorithms and data analysis tools for the prediction of call arrival times and rates.",
    long_description="",
    url="",
    download_url="",
    project_urls=dict(),
    author="Emad Bin Abid | Ateeb Ahmed | Syed Bilal Hoda",
    author_email="emad.bin.abid@gmail.com | aa02751@st.habib.edu.pk | sh02918@st.habib.edu.pk",
    maintainer="Emad Bin Abid | Ateeb Ahmed | Syed Bilal Hoda",
    maintainer_email="emad.bin.abid@gmail.com | aa02751@st.habib.edu.pk | sh02918@st.habib.edu.pk",
    license="",
    license_file="",
    long_description_content_type="",
    keywords=["library", "call time", "prediction", "call arrival times and rates"],
    platforms=[],
    provides=[
        'CallTimePredictor', 
        'DataTank', 
        'ValidationMetric', 
        'Logger'
        ],
    packages=[
        'PCATR',
        'PCATR/CallTimePredictor',
        'PCATR/CallTimePredictor/CTPAlgorithm',
        'PCATR/CallTimePredictor/CTPDataAnalysis',
        'PCATR/DataTank', 
        'PCATR/ValidationMetric', 
        'PCATR/Logger'
    ],
    install_requires=[
        'pandas',
        'numpy',
        'statsmodels',
        'matplotlib',
        'sklearn',
        'seaborn',
        'torch'
        ],
    obsoletes=[]
)