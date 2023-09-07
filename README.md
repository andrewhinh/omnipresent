# omnipresent

People Detection

## Setup

1. Create the conda environment locally:

    ```bash
    conda env update --prune -f environment.yml
    conda activate omnipresent
    pip install -r requirements.txt
    export PYTHONPATH=.
    echo "export PYTHONPATH=.:$PYTHONPATH" >> ~/.bashrc
    ```

2. Run the script:

    ```bash
    python omnipresent.py
    ```
