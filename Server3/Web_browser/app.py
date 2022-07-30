from flask import Flask

app = Flask(__name__)
app.secret_key = b'Ll\x89(\xdb\x13bM\x1f\xe9\xb3\x16\x83u\xa0\t'
app.config['UPLOAD_FOLDER'] = 'static/uploads/'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
