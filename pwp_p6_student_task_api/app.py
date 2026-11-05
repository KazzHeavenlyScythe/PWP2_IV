
from flask import Flask, request, jsonify

app = Flask(__name__)

# Data tugas
tasks = [
    {
        "id": 1,
        "nama": "Membuat Laporan Praktikum",
        "mata_kuliah": "Pemrograman Web",
        "status": "Belum Selesai"
    },
    {
        "id": 2,
        "nama": "Mempelajari REST API",
        "mata_kuliah": "Pemrograman Web",
        "status": "Selesai"
    }
]

# Endpoint 1: Informasi API
@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "message": "Selamat datang di Student Task Management API",
        "total_endpoint": 5
    })

# Endpoint 2: Menampilkan semua tugas
@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify({
        "message": "Berhasil mengambil semua data tugas",
        "dataset": tasks
    })

# Endpoint 3: Menampilkan tugas berdasarkan ID
@app.route('/tasks/<int:id>', methods=['GET'])
def get_task(id):
    task = next((t for t in tasks if t["id"] == id), None)

    if task is None:
        return jsonify({"message": "Tugas tidak ditemukan"}), 404

    return jsonify({
        "message": "Berhasil mengambil data tugas",
        "dataset": task
    })

# Endpoint 4: Menambahkan tugas
@app.route('/tasks', methods=['POST'])
def add_task():
    data = request.get_json()

    if not data or not data.get("nama") or not data.get("mata_kuliah"):
        return jsonify({
            "message": "Nama dan mata kuliah wajib diisi"
        }), 400

    new_task = {
        "id": max([t["id"] for t in tasks], default=0) + 1,
        "nama": data["nama"],
        "mata_kuliah": data["mata_kuliah"],
        "status": data.get("status", "Belum Selesai")
    }

    tasks.append(new_task)

    return jsonify({
        "message": "Tugas berhasil ditambahkan",
        "dataset": new_task
    }), 201

# Endpoint 5: Menghapus tugas
@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    task = next((t for t in tasks if t["id"] == id), None)

    if task is None:
        return jsonify({"message": "Tugas tidak ditemukan"}), 404

    tasks.remove(task)

    return jsonify({
        "message": "Tugas berhasil dihapus",
        "dataset": task
    })

if __name__ == '__main__':
    app.run(debug=True)
