import gradio as gr
import subprocess

def start(online_mode, version, memory):
    command = f"sudo docker run --name mc_server --volume=./data:/data \
        -e EULA=TRUE \
        -e ONLINE_MODE={'TRUE' if online_mode else 'FALSE'} \
        -e VERSION={version} \
        -e MEMORY={memory}G \
        itzg/minecraft-server -d"
    print(command)
    subprocess.run(command, shell=True)

def debug(online_mode, version, memory):
    print("============================================================================")
    print("online mode:", online_mode)
    print("version:", version)
    print("memory:", memory)
    print("============================================================================")

def stop():
    command = f"sudo docker stop mc_server"
    print(command)
    subprocess.run(command, shell=True)

with gr.Blocks() as interface:
    online_mode = gr.Checkbox(label="ONLINE MODE", info="Check it if the accounts are paid, don't if they are cracked.")
    version = gr.Textbox(label="Version", info="e.g. 1.12.2, 1.20.4", value="1.16.5")
    memory = gr.Slider(1, 64, value=4, label="Memory", info="How much RAM do you want the server to use?", step=1)
    start_btn = gr.Button("Start Server")
    start_btn.click(fn=start, inputs=[online_mode, version, memory], api_name="start")
    debug_btn = gr.Button("Debug")
    debug_btn.click(fn=debug, inputs=[online_mode, version, memory], api_name="debug")
    stop_btn = gr.Button("Stop Server", variant="stop")
    stop_btn.click(fn=stop, api_name="stop")

interface.launch()
