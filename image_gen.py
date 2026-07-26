import shutil
import os

def generate_image_mock(prompt, job_id, reference_image_path=None):
    """
    Fake image generator — copies a placeholder image and returns its path.
    Accepts a reference_image_path to match the real interface, but doesn't
    use it yet since this is a mock (per assignment brief, this is fine).
    """
    os.makedirs("static/results", exist_ok=True)
    output_path = f"static/results/{job_id}.png"
    shutil.copy("static/placeholder.png", output_path)
    return output_path