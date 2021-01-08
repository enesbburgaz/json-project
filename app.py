from flask import Flask, render_template, request, redirect, url_for, send_file
import json
import os

app = Flask(__name__)

@app.route('/')
def index():
    files = os.listdir('json')
    files = [file for file in files]
    return render_template('index.html', files=files)

@app.route('/create', methods=['GET', 'POST'])
def createJson():
    if request.method == 'POST':
        fileName = request.form.get("fileName")
        data = request.form.get("jsonData")
        data = data.replace("\r", "")
        data = data.replace("\n", "")
        data = data.replace(" ", "")
        jsonData = json.loads(data)
        with open(f"json/{fileName}", "w") as p:
            json.dump(jsonData, p)
        return redirect(url_for('index'))
    else:
        return render_template('create.html')

@app.route('/edit/<filenamejson>', methods=['GET', 'POST'])
def editJson(filenamejson, static_folder="json"):
    output_path = os.path.join(static_folder, filenamejson)
    json_file= open(output_path, encoding="utf8")
    data = json_file.read()
    return render_template('edit.html', data=[filenamejson, data])

@app.route('/view/<filenamejson>')
def viewJson(filenamejson, static_folder="json"):
    output_path = os.path.join(static_folder, filenamejson)
    json_file= open(output_path, encoding="utf8")
    data = json_file.read()
    return data

@app.route('/delete/<filenamejson>')
def deleteJson(filenamejson):
    os.remove(f'json/{filenamejson}')
    return redirect(url_for('index'))

@app.route('/import')
def importJson():
    pass

@app.route('/export/<filenamejson>')
def exportJson(filenamejson):
    return send_file(f"json/{filenamejson}", as_attachment=True)

if __name__ == '__main__':
    app.run()

