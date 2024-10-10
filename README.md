# Components
A repository of physics models and components for use with [Artifact](https://artifact.engineer).

# Getting Started
## Physics Models

The physics models in this repository are specified in Jupyter notebooks for interactive development.

## Setup and Usage

To work with these models, follow these steps:

1. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Launch Jupyter Notebook:
   ```
   jupyter notebook
   ```

4. Open and run the desired notebook.

5. To interact with the notebook outputs from the command line, use:
   ```
   jupyter console --existing
   ```
   This connects to the running notebook kernel, allowing you to access variables and execute code interactively.