import gradio as gr
import subprocess

def start(online_mode):
    command_env_file = f"""echo GRADIO_SERVER_NAME=0.0.0.0\
    ONLINE_MODE={online_mode}\
    > .env"""
    subprocess.run(command_env_file, shell=True)

    command = f"sudo docker run --volume=./data:/data --env-file=.env itzg/minecraft-server -d"
    subprocess.run(command, shell=True)

with gr.Blocks() as interface:
    online_mode = gr.Dropdown(choices=["TRUE", "FALSE"], label="ONLINE MODE")
    start_btn = gr.Button("Start Server")
    start_btn.click(fn=start, inputs=online_mode, api_name="start")

interface.launch()
