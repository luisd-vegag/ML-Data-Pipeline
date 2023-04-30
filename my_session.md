# Set up a Python virtual environment and install necessary libraries, such as Airflow, pandas, scikit-learn, FastAPI, and others.
python3 -m venv env
source env/bin/activate
pip install pandas scikit-learn fastapi uvicorn apache-airflow
pip freeze
----------------------------
# Download the stock market dataset and store it under the data/raw directory.
mkdir -p data/raw
kaggle datasets download jacksoncrow/stock-market-dataset -p data/raw

## Go to Kaggle.com, login, settings, API, Create New Token 
mkdir ~/.kaggle/
mv kaggle.json ~/.kaggle/
sudo chmod 600 ~/.kaggle/kaggle.json

sudo pip install kaggle
kaggle datasets list

unzip data/raw/stock-market-dataset.zip -d data/raw