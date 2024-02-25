import gradio as gr
import subprocess

def start(online_mode):
    command = f"sudo docker run --volume=./data:/data -e \
        EULA=TRUE \
        ONLINE_MODE={online_mode} \
        itzg/minecraft-server -d"
    subprocess.run(command, shell=True)

with gr.Blocks() as interface:
    online_mode = gr.Dropdown(choices=["TRUE", "FALSE"], label="ONLINE MODE")
    start_btn = gr.Button("Start Server")
    start_btn.click(fn=start, inputs=online_mode, api_name="start")

interface.launch()
