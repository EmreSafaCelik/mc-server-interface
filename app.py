import gradio as gr
import subprocess
import json
import shlex

def load_args():
    with open('args.json', 'r') as file:
        return json.load(file) 

def save_args(args_dict):
    with open('args.json', 'w') as file:
        file.write(json.dumps(args_dict))

def validate_args(args_dict):
    if not isinstance(args_dict['online_mode'], bool):
        raise ValueError("Online mode must be a boolean")
    # Must add validation for 'version' format (if any)
    # Must also check memory to be integer
    if not 1 <= args_dict['memory'] <= 64:
        raise ValueError("Memory must be between 1 and 64")

def create_docker_command(args_dict):
    command = f"docker run --name mc_server --volume=./data:/data \
               -e EULA=TRUE \
               -e ONLINE_MODE={'TRUE' if args_dict['online_mode'] else 'FALSE'} \
               -e VERSION={args_dict['version']} \
               -e MEMORY={args_dict['memory']}G \
               itzg/minecraft-server -d"
    return command

def execute_docker_command(command):
    try:
        print(command)
        subprocess.run(shlex.split(command), check=True)
    except subprocess.CalledProcessError as e:
        print(f"Docker command failed: {e}")

def start():
    command = create_docker_command(args_dict)
    execute_docker_command(command)

def debug():
    print("============================================================================")
    print("online mode:", args_dict['online_mode'])
    print("version:", args_dict['version'])
    print("memory:", args_dict['memory'])
    print("============================================================================")

def stop():
    command = "docker stop mc_server" 
    execute_docker_command(command)
    command = "docker rm mc_server"
    execute_docker_command(command)

def assign(online_mode=None, version=None, memory=None, cf_api_key=None):
    args_dict['online_mode'] = online_mode if online_mode != None else args_dict['online_mode']
    args_dict['version'] = version if version != None else args_dict['version']
    args_dict['memory'] = memory if memory != None else args_dict['memory']
    args_dict['cf_api_key'] = cf_api_key if cf_api_key != None else args_dict['cf_api_key']
    validate_args(args_dict)
    save_args(args_dict)

args_dict = load_args() 

with gr.Blocks() as home:
    with gr.Tab("Server Settings"):
        with gr.Row():
            online_mode = gr.Checkbox(label="ONLINE MODE", value=args_dict['online_mode'])
            version = gr.Textbox(label="Version", value=args_dict['version'])
            memory = gr.Slider(1, 64, value=args_dict['memory'], label="Memory", step=1)

            start_btn = gr.Button("Start Server")
            debug_btn = gr.Button("Debug")
            stop_btn = gr.Button("Stop Server", variant="stop")

    with gr.Tab("CurseForge"):
        cf_api_key = gr.Textbox(label="CF_API_KEY", value=args_dict['cf_api_key'])

    online_mode.change(fn=assign, inputs=[online_mode, version, memory, cf_api_key])
    version.change(fn=assign, inputs=[online_mode, version, memory, cf_api_key])
    memory.change(fn=assign, inputs=[online_mode, version, memory, cf_api_key])
    cf_api_key.change(fn=assign, inputs=[online_mode, version, memory, cf_api_key])
    start_btn.click(fn=start)
    debug_btn.click(fn=debug)
    stop_btn.click(fn=stop)

home.launch()
