import shlex
import subprocess

import modal

image = (
    modal.Image.debian_slim(python_version="3.11")
    .uv_pip_install(
        "streamlit>=1.62.0",
        "pandas>=3.0.5",
        "matplotlib>=3.11.1",
        "seaborn>=0.13.2",
        "supabase>=2.31.0",
        "python-dotenv>=1.2.3",
    )
    .add_local_file("app.py", remote_path="/root/app.py")
)

app = modal.App(name="ev-population-dashboard", image=image)


@app.function(secrets=[modal.Secret.from_name("supabase-secret")])
@modal.concurrent(max_inputs=100)
@modal.web_server(8000)
def run():
    target = shlex.quote("/root/app.py")
    cmd = (
        f"streamlit run {target} --server.port 8000 "
        "--server.enableCORS=false --server.enableXsrfProtection=false"
    )
    subprocess.Popen(cmd, shell=True)
