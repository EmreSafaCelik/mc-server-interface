import gradio as gr
import subprocess

def start(online_mode):
    command = f"sudo docker run --volume=./data:/data \
        -e EULA=TRUE \
        -e ONLINE_MODE={'TRUE' if online_mode else 'FALSE'} \
        -e VERSION={version.value} \
        -e MEMORY={memory.value}G \
        itzg/minecraft-server -d"
    print(command)
    subprocess.run(command, shell=True)

with gr.Blocks() as interface:
    online_mode = gr.Checkbox(label="ONLINE MODE", info="Check it if the accounts are paid, don't if they are cracked.")
    version = gr.Textbox(label="Version", info="e.g. 1.12.2, 1.20.4")
    memory = gr.Slider(1, 64, value=4, label="Memory", info="How much RAM do you want the server to use?")
    start_btn = gr.Button("Start Server")
    start_btn.click(fn=start, inputs=online_mode, api_name="start")

interface.launch()
