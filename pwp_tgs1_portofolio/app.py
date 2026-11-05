from flask import Flask, render_template

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True


# Halaman utama: Biodata
@app.route('/')
def home():
    return render_template('index.html')


# Halaman Proyek
@app.route('/proyek')
def proyek():
    return render_template('proyek.html')


# Halaman Pendidikan
@app.route('/pendidikan')
def pendidikan():
    return render_template('pendidikan.html')


# Halaman Keahlian
@app.route('/keahlian')
def keahlian():
    return render_template('keahlian.html')


# Halaman Kontak
@app.route('/kontak')
def kontak():
    return render_template('kontak.html')


if __name__ == '__main__':
    app.run(debug=True)