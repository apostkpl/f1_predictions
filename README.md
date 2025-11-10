# Data Presentation and Analysis using the FastF1 API

#### Toying around with the FastF1 API and various data presentation (Matplotlib), data manipulation (Pandas) and predictions (Sklearn). This is a current work in progress, and definitely not a way to predict actual winners (for now 👀)

#### _UPDATE November 2025_:
- Seperated logic into different functions inside various py files.
- Used XGB Classifier for better results.
- Re-Created Main with Flask and serialized the results using json.
- Created a minimal Spring Boot app to display the results/predictions in a simple HTML page.

#### _TODO_:
- Refine features and predictions. Maybe add more model types (currently XGBC-only).
- Setup proper getter methods for some details, like track names etc.
- Beautify the end-result (HTML file).

## Tools used for this Project:
- _JupyterLab_
- _MiniConda/Python_
- _Python Libraries (NumPy, Matplotlib, Pandas, Sklearn)_
- _Bash/VIM (for minor details) and GitBash_
- _Java and Java Frameworks (Spring Boot)_

  [![tools](https://skillicons.dev/icons?i=anaconda,py,bash,sklearn,git,java,spring)](https://skillicons.dev)

## To create an environment with the basic libraries needed for this project:
- _Download the Anaconda Installer (MiniConda is recommended if you are used to the Terminal):_
  ```
  https://www.anaconda.com/download
  ```
  
- _Initialize the Conda environment in Powershell:_
  ```
  conda init powershell
  ```

- _Restart your terminal and check if conda works:_
  ```
  conda --version
  ```
  
- _Create a new virtual environment using Conda and the provided yml file above:_
  ```
  conda env create -f environment.yml -n <your_env_name_here>
  ```
- _Have fun_ 😎
  
