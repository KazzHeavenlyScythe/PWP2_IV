from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from database import get_db

app = Flask(__name__)
app.secret_key = "responsi_pwp_2026"

# HALAMAN REGISTER
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nim = request.form['nim']
        nama = request.form['nama']
        password = request.form['password']

        db = get_db()
        cursor = db.cursor()

        cursor.execute("SELECT id FROM mahasiswa WHERE nim = %s", (nim,))
        if cursor.fetchone():
            flash('NIM sudah terdaftar!')
        else:
            password_hash = generate_password_hash(password)

            cursor.execute(
                "INSERT INTO mahasiswa (nim, nama, password) VALUES (%s, %s, %s)",
                (nim, nama, password_hash)
            )
            db.commit()
            flash('Registrasi berhasil! Silakan login.')
            cursor.close()
            db.close()
            return redirect(url_for('login'))

        cursor.close()
        db.close()

    return render_template('register.html')

# HALAMAN LOGIN
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nim = request.form['nim']
        password = request.form['password']

        db = get_db()
        cursor = db.cursor(dictionary=True)

        cursor.execute("SELECT * FROM mahasiswa WHERE nim = %s", (nim,))
        user = cursor.fetchone()

        cursor.close()
        db.close()

        if user and check_password_hash(user['password'], password):
            session['mahasiswa_id'] = user['id']
            session['nama'] = user['nama']
            return redirect(url_for('dashboard'))

        flash('NIM atau password salah!')

    return render_template('login.html')

# HALAMAN DASHBOARD
@app.route('/')
def dashboard():
    if 'mahasiswa_id' not in session:
        return redirect(url_for('login'))

    return render_template('dashboard.html', nama=session['nama'])

# LOGOUT
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# HALAMAN DAFTAR MATA KULIAH
@app.route('/matakuliah')
def matakuliah():
    if 'mahasiswa_id' not in session:
        return redirect(url_for('login'))

    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT m.*,
        EXISTS(
            SELECT 1 FROM matakuliah_diambil d
            WHERE d.matakuliah_id = m.id
            AND d.mahasiswa_id = %s
        ) AS sudah_diambil
        FROM matakuliah m
        ORDER BY FIELD(m.hari, 'Senin', 'Selasa',
                       'Rabu', 'Kamis', 'Jumat'),
                 m.jam_mulai
    """, (session['mahasiswa_id'],))

    data = cursor.fetchall()

    cursor.execute("""
        SELECT
            COUNT(m.id) AS jumlah_mk,
            COALESCE(SUM(m.sks), 0) AS total_sks,
            COALESCE(SUM(CASE WHEN m.jenis='Teori'
                THEN m.sks ELSE 0 END), 0) AS teori,
            COALESCE(SUM(CASE WHEN m.jenis='Praktik'
                THEN m.sks ELSE 0 END), 0) AS praktik
        FROM matakuliah_diambil d
        JOIN matakuliah m ON d.matakuliah_id = m.id
        WHERE d.mahasiswa_id = %s
    """, (session['mahasiswa_id'],))

    statistik = cursor.fetchone()

    cursor.close()
    db.close()

    return render_template('matakuliah.html', data=data, statistik=statistik)


# PROSES MENGAMBIL MATA KULIAH (AJAX)
@app.route('/ambil-matakuliah', methods=['POST'])
def ambil_matakuliah():
    if 'mahasiswa_id' not in session:
        return jsonify({'status': False, 'pesan': 'Silakan login terlebih dahulu!'})

    matakuliah_id = request.json.get('matakuliah_id')

    db = get_db()
    cursor = db.cursor()

    try:
        cursor.execute(
            "INSERT INTO matakuliah_diambil (mahasiswa_id, matakuliah_id) VALUES (%s, %s)",
            (session['mahasiswa_id'], matakuliah_id)
        )
        db.commit()
        pesan = 'Mata kuliah berhasil diambil!'
        status = True

    except Exception:
        db.rollback()
        pesan = 'Mata kuliah sudah pernah diambil atau data tidak valid!'
        status = False

    cursor.close()
    db.close()

    return jsonify({'status': status, 'pesan': pesan})


# HALAMAN MATA KULIAH SAYA
@app.route('/matakuliah-saya')
def matakuliah_saya():
    if 'mahasiswa_id' not in session:
        return redirect(url_for('login'))

    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT m.*, d.tanggal_ambil
        FROM matakuliah_diambil d
        JOIN matakuliah m ON d.matakuliah_id = m.id
        WHERE d.mahasiswa_id = %s
        ORDER BY FIELD(m.hari, 'Senin', 'Selasa',
                       'Rabu', 'Kamis', 'Jumat'),
                 m.jam_mulai
    """, (session['mahasiswa_id'],))

    data = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template('matakuliah_saya.html', data=data)


if __name__ == '__main__':
    app.run(debug=True)