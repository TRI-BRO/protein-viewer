from flask import Flask, render_template, request, Response
import requests

app = Flask(__name__)

def validate_sequence(sequence):
    valid_chars = set("ACDEFGHIKLMNPQRSTVWY")
    return all(c in valid_chars for c in sequence) and len(sequence) > 0

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        sequence = request.form['sequence'].upper().strip()
        if not validate_sequence(sequence):
            return "Invalid protein sequence!"
        
        # Get 3D structure from ESMFold
        try:
            response = requests.post(
                "https://api.esmatlas.com/foldSequence/v1/pdb/",
                data=sequence,
                headers={"Content-Type": "application/x-www-form-urlencoded"}
            )
            pdb_data = response.text
            return render_template('result.html', pdb_data=pdb_data)
        except Exception as e:
            return f"Error: {str(e)}"
    
    return render_template('index.html')

@app.route('/download')
def download_pdb():
    pdb_data = request.args.get('data')
    return Response(
        pdb_data,
        mimetype="text/plain",
        headers={"Content-disposition": "attachment; filename=structure.pdb"}
    )

if __name__ == '__main__':
    app.run(debug=True)
