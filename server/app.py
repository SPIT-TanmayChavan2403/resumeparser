from flask import Flask,  jsonify
from flask_cors import CORS
from flask import request
import scorer

app = Flask(__name__)
CORS(app)

# The directory where the files will be saved
UPLOAD_FOLDER = "Resume"

@app.route("/upload", methods=["POST"])
def upload_files():
  # Loop through the files in request.files
  for file in request.files.values():
    print(file)
  for file in request.files.values():
    # Get the file name and extension
    filename = file.filename
    # Save the file to the upload folder
    file.save(UPLOAD_FOLDER + "/" + filename)
  resp = scorer.main()
  return jsonify(resp)


if __name__ == '__main__':
    app.run(debug=True)