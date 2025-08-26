from multiprocessing import freeze_support
from watchfiles import run_process
import app  # Import app module

def start_app():
    app.launch_app()

if __name__ == "__main__":
    freeze_support()
    run_process('.', target=start_app)
