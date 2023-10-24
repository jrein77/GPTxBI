from flask import Flask, request, render_template, send_from_directory
import pandas as pd
import os
import openai

app = Flask(__name__)

UPLOAD_FOLDER = "uploads/"
ALLOWED_EXTENSIONS = {'xls', 'xlsx', 'csv'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

openai.api_key = '...'  # Replace with your API Key

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    optimized_data_link = None
    optimized_data = None

    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']
        if file.filename == '':
            return 'No selected file'
        if file and allowed_file(file.filename):
            filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filename)
            optimized_data_path = optimize_data_for_powerbi(filename)
            
            if optimized_data_path.endswith('.csv'):
                df = pd.read_csv(os.path.join(app.config['UPLOAD_FOLDER'], optimized_data_path))
                optimized_data = df.to_html(classes='data-table', border=0)
            else:
                df = pd.read_excel(os.path.join(app.config['UPLOAD_FOLDER'], optimized_data_path))
                optimized_data = df.to_html(classes='data-table', border=0)

            optimized_data_link = f"/download/{optimized_data_path}"

    return render_template('upload.html', link=optimized_data_link, data=optimized_data)

@app.route('/download/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

def optimize_data_for_powerbi(filepath):
    # Read data
    if filepath.endswith('.csv'):
        df = pd.read_csv(filepath)
    else:
        df = pd.read_excel(filepath)
    
    # Using the GPT API to get recommendations for column renaming.
    for column in df.columns:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": f"Optimal name for column '{column}' in PowerBI?"}
            ]
        )
        optimized_name = response.choices[0].message['content'].strip()
        df.rename(columns={column: optimized_name}, inplace=True)
    
    # Save optimized data
    optimized_filepath = os.path.join(UPLOAD_FOLDER, "optimized_" + os.path.basename(filepath))
    if optimized_filepath.endswith('.csv'):
        df.to_csv(optimized_filepath, index=False)
    else:
        df.to_excel(optimized_filepath, index=False)

    return "optimized_" + os.path.basename(filepath)

if __name__ == "__main__":
    app.run(debug=True)
