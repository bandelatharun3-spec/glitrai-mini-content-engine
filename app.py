from flask import Flask, request, jsonify, send_from_directory
from models import SessionLocal, Job
from llm import generate_image_prompt
from image_gen import generate_image_mock
import uuid
import threading
import os

app = Flask(__name__)

def process_job(job_id, product_name, description, input_image_path=None):
    db = SessionLocal()
    job = db.query(Job).filter(Job.id == job_id).first()
    try:
        job.status = "processing"
        db.commit()

        prompt = generate_image_prompt(product_name, description)
        job.generated_prompt = prompt
        db.commit()

        result_path = generate_image_mock(prompt, job_id, input_image_path)
        job.result_image_path = result_path
        job.status = "completed"
        db.commit()
    except Exception as e:
        job.status = "failed"
        job.error_message = str(e)
        db.commit()
    finally:
        db.close()
@app.route("/health")
def health():
    return {"status": "ok"}

@app.route("/generate", methods=["POST"])
def generate():
    product_name = request.form.get("product_name")
    description = request.form.get("description")
    image_file = request.files.get("product_image")

    if not product_name or not description:
        return jsonify({"error": "product_name and description are required"}), 400

    job_id = str(uuid.uuid4())

    input_image_path = None
    if image_file:
        os.makedirs("static/uploads", exist_ok=True)
        ext = os.path.splitext(image_file.filename)[1] or ".jpg"
        input_image_path = f"static/uploads/{job_id}{ext}"
        image_file.save(input_image_path)

    db = SessionLocal()
    job = Job(
        id=job_id,
        product_name=product_name,
        description=description,
        input_image_path=input_image_path,
        status="pending"
    )
    db.add(job)
    db.commit()
    db.close()

    thread = threading.Thread(target=process_job, args=(job_id, product_name, description, input_image_path))
    thread.start()

    return jsonify({"job_id": job_id}), 201
@app.route("/")
def index():
    return send_from_directory("static", "index.html")

    db = SessionLocal()
    job = Job(
        id=str(uuid.uuid4()),
        product_name=product_name,
        description=description,
        status="pending"
    )
    db.add(job)
    db.commit()
    job_id = job.id
    db.close()

    thread = threading.Thread(target=process_job, args=(job_id, product_name, description))
    thread.start()

    return jsonify({"job_id": job_id}), 201

@app.route("/jobs/<job_id>")
def get_job(job_id):
    db = SessionLocal()
    job = db.query(Job).filter(Job.id == job_id).first()
    db.close()

    if not job:
        return jsonify({"error": "job not found"}), 404

    return jsonify({
        "id": job.id,
        "product_name": job.product_name,
        "status": job.status,
        "generated_prompt": job.generated_prompt,
        "result_image_path": job.result_image_path,
        "error_message": job.error_message
    })

@app.route("/static/results/<filename>")
def get_result_image(filename):
    return send_from_directory("static/results", filename)

if __name__ == "__main__":
    app.run(debug=True)