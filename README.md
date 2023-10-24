# GPTxBI
# Financial Document Optimizer

This Flask application allows users to upload financial documents (Excel/CSV files) and optimizes column names for better usage in tools like PowerBI. It leverages OpenAI's GPT-3 to suggest optimal names for columns based on their context.

## Installation

1. **Clone the repository**:
    ```bash
    git clone [[YOUR REPO URL]](https://github.com/jrein77/GPTxBI.git)
    cd Flask-Example
    ```

2. **Set up a virtual environment** (Recommended):
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. **Install the required packages**:
    ```bash
    pip install Flask pandas openai
    ```

## Configuration

1. **API Key**: Make sure to replace the placeholder '...' in the code with your actual OpenAI API key.

2. **Uploads folder**: By default, uploaded files are saved to an 'uploads' folder in the application's root directory. Ensure necessary permissions for file uploads or change the path if needed.

## Running the Application

1. **Activate the virtual environment** (if you set one up):
    ```bash
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

2. **Run the Flask application**:
    ```bash
    python app.py
    ```

3. Open a browser and navigate to `http://127.0.0.1:5000/` to use the application.

## Usage

1. Use the web interface to upload an Excel or CSV file containing financial data.
2. The application will process the file and optimize the column names for PowerBI usage.
3. Download the optimized file or view the data directly on the web page.
