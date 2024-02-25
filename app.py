import gradio as gr
import subprocess
import json


args_dict = {}
with open('args.json', 'r') as file:
    args_dict = json.load(file)    


def start():

    command = f"sudo docker run --name mc_server --volume=./data:/data \
        -e EULA=TRUE \
        -e ONLINE_MODE={'TRUE' if args_dict['online_mode'] else 'FALSE'} \
        -e VERSION={args_dict['version']} \
        -e MEMORY={args_dict['memory']}G \
        itzg/minecraft-server -d"
    print(command)
    subprocess.run(command, shell=True)

def debug():
    print("============================================================================")
    print("online mode:", args_dict['online_mode'])
    print("version:", args_dict['version'])
    print("memory:", args_dict['memory'])
    print("============================================================================")

def stop():
    command = f"sudo docker stop mc_server"
    print(command)
    subprocess.run(command, shell=True)

def assign(online_mode=None, version=None, memory=None):
    args_dict['online_mode'] = online_mode if online_mode != None else args_dict['online_mode']
    args_dict['version'] = version if version != None else args_dict['version']
    args_dict['memory'] = memory if memory != None else args_dict['memory']
    with open('args.json', 'w') as file:
        file.write(json.dumps(args_dict))

print(args_dict)

with gr.Blocks() as interface:
    online_mode = gr.Checkbox(label="ONLINE MODE", info="Check it if the accounts are paid, don't if they are cracked.", value=args_dict['online_mode'])
    online_mode.change(fn=assign, inputs=online_mode)

    version = gr.Textbox(label="Version", info="e.g. 1.12.2, 1.20.4", value=args_dict['version'])
    version.change(fn=assign, inputs=[None, version])
    
    memory = gr.Slider(1, 64, value=args_dict['memory'], label="Memory", info="How much RAM do you want the server to use?", step=1)
    memory.change(fn=assign, inputs=[None, None, memory])
    
    start_btn = gr.Button("Start Server")
    start_btn.click(fn=start, api_name="start")
    
    debug_btn = gr.Button("Debug")
    debug_btn.click(fn=debug, api_name="debug")
    
    stop_btn = gr.Button("Stop Server", variant="stop")
    stop_btn.click(fn=stop, api_name="stop")


interface.launch()
