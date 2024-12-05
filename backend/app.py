import os
import subprocess
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///voice_app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# Initialize the database and migration
db = SQLAlchemy(app)
migrate = Migrate(app, db)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Backend folder
SEED_VC_DIR = os.path.join(BASE_DIR, '../seed-vc')  # Navigate to seed-vc folder
EXAMPLES_FOLDER = os.path.join(SEED_VC_DIR, 'examples')
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')  # Inside backend folder
OUTPUT_FOLDER = os.path.join(BASE_DIR, 'output')  # Inside backend folder

# Configure Flask app
app.config['EXAMPLES_FOLDER'] = EXAMPLES_FOLDER
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER
app.config['ALLOWED_EXTENSIONS'] = {'wav', 'mp3', 'flac'}  # Allowed file types

# Ensure directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Paths to source and reference folders
SOURCE_FOLDER = os.path.join(EXAMPLES_FOLDER, 'source')
REFERENCE_FOLDER = os.path.join(EXAMPLES_FOLDER, 'reference')



# Function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']
    db.init_app(app)
from models import User
with app.app_context():
    db.create_all()


# @app.route('/users', methods=['POST'])
# def create_user():
#     data = request.get_json()

#     # Validate input
#     if not data or not all(key in data for key in ('first_name', 'last_name', 'password')):
#         return jsonify({"error": "Missing required fields: first_name, last_name, password"}), 400

#     first_name = data.get('first_name')
#     last_name = data.get('last_name')
#     password = data.get('password')

#     try:
#         # Create new user
#         new_user = User(first_name=first_name, last_name=last_name, password=password)
#         db.session.add(new_user)
#         db.session.commit()

#         return jsonify({"message": "User created successfully!", "user_id": new_user.id}), 201

#     except Exception as e:
#         db.session.rollback()
#         return jsonify({"error": f"Failed to create user: {str(e)}"}), 500
#db.init_app(app)

# Ensure tables are created
with app.app_context():
    db.create_all()

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()

    # Validate input
    if not data or not all(key in data for key in ('first_name', 'last_name', 'password')):
        return jsonify({"error": "Missing required fields: first_name, last_name, password"}), 400

    first_name = data.get('first_name')
    last_name = data.get('last_name')
    password = data.get('password')

    try:
        # Create new user
        new_user = User(first_name=first_name, last_name=last_name, password=password)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({"message": "User created successfully!", "user_id": new_user.id}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to create user: {str(e)}"}), 500


@app.route('/view_users', methods=['GET'])
def view_users():
    users = User.query.all()
    return jsonify([{
        'first_name': user.first_name,
        'last_name': user.last_name,
        'password': user.password
    } for user in users])


@app.route('/list_examples', methods=['GET'])
def list_examples():
    """
    List example source and reference files from their respective directories.
    """
    try:
        source_files = [f for f in os.listdir(SOURCE_FOLDER) if os.path.isfile(os.path.join(SOURCE_FOLDER, f))]
        reference_files = [f for f in os.listdir(REFERENCE_FOLDER) if os.path.isfile(os.path.join(REFERENCE_FOLDER, f))]
    except FileNotFoundError:
        return jsonify({"error": "Example folders not found"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({
        "source_files": source_files,
        "reference_files": reference_files
    }), 200

# Route to handle file uploads
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)
        return jsonify({"message": "File uploaded successfully", "filename": file.filename}), 200
    else:
        return jsonify({"error": "Invalid file type"}), 400

# Route to run the inference CLI
@app.route('/run_inference', methods=['POST'])
def run_inference():
    """
    Runs the inference.py script with the specified source and reference files.
    """
    data = request.get_json()

    # Extract the source and target file paths from the request
    source_file = data.get('source_file')
    target_file = data.get('target_file')

    if not source_file or not target_file:
        return jsonify({"error": "Source or target file not provided"}), 400

    # Construct file paths for the example files
    source_file_path = os.path.join(SOURCE_FOLDER, source_file)
    target_file_path = os.path.join(REFERENCE_FOLDER, target_file)

    # Ensure the source and reference files exist
    if not os.path.exists(source_file_path) or not os.path.exists(target_file_path):
        return jsonify({"error": "Source or reference file not found"}), 404

    # Prepare the command to run inference.py with the provided arguments
    output_file_path = os.path.join(app.config['OUTPUT_FOLDER'], f"{source_file}_to_{target_file}.wav")
    command = [
        'python3', os.path.join(SEED_VC_DIR, 'inference.py'),  # Ensure the script path is correct
        '--source', source_file_path,
        '--target', target_file_path,
        '--output', output_file_path,
        '--diffusion-steps', '25',
        '--checkpoint', '',
        '--config', ''
    ]

    try:
        # Run the inference command
        subprocess.run(command, check=True)

        # Return the output file URL
        return jsonify({"message": "Inference completed", "output_file": output_file_path}), 200
    except subprocess.CalledProcessError as e:
        return jsonify({"error": "Error running inference", "details": str(e)}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route to download the output file
@app.route('/download_output', methods=['GET'])
def download_output():
    filename = 'result.wav'  # Adjust this based on your output file name
    output_dir = app.config['OUTPUT_FOLDER']  # Path to the output directory

    try:
        return send_from_directory(directory=output_dir, path=filename, as_attachment=True)
    except FileNotFoundError:
        return jsonify({"error": "Output file not found"}), 404

# You can add other routes or logic here as needed, for example, database handling for AudioFile model, etc.

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create tables
        print("Tables created successfully!")
    app.run(debug=True)
