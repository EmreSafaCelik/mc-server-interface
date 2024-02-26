import gradio as gr
import subprocess
import json
import shlex
import threading

# run a docker terminator command when CTRL+C is recieved with signal package
# modpack server should work
# ./start.sh echoing the old args.json to create it, won't start the app cuz of it
# a way to save, add and switch between worlds

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
    version_string = f"-e VERSION={args_dict['version']}" 
    command = f"docker run -it -p 25565:25565 --name mc_server --volume=./data:/data \
               -p 25565:22565 \
               -e EULA=TRUE \
               -e SERVER_NAME=0.0.0.0 \
               -e TYPE={args_dict['server_type']} \
               -e ONLINE_MODE={'TRUE' if args_dict['online_mode'] else 'FALSE'} \
               {version_string if not args_dict['server_type'] == 'AUTO_CURSEFORGE' else ''} \
               -e MEMORY={args_dict['memory']}G \
               -e CF_PAGE_URL={args_dict['cf_page_url']} \
               -e CF_API_KEY={args_dict['cf_api_key']} \
               itzg/minecraft-server"
    return command

def execute_docker_command(command):
    def run_command():
        try:
            print(command)
            subprocess.run(shlex.split(command), check=True)
        except subprocess.CalledProcessError as e:
            print(f"Docker command failed: {e}")

    thread = threading.Thread(target=run_command)
    thread.start()

def start():
    command = create_docker_command(args_dict)
    execute_docker_command(command)
    return update_ui(server_running=True)

def debug():
    print("============================================================================")
    print(args_dict)
    print("============================================================================")

def stop():
    command = "docker stop mc_server" 
    execute_docker_command(command)
    command = "docker rm mc_server"
    execute_docker_command(command)
    return update_ui(server_running=False)

def update_ui(server_running):
    return gr.Button(interactive=server_running)

def assign(server_type=None, online_mode=None, version=None, memory=None, cf_page_url=None, cf_api_key=None):
    args_dict['server_type'] = server_type if server_type != None else args_dict['server_type']
    args_dict['online_mode'] = online_mode if online_mode != None else args_dict['online_mode']
    args_dict['version'] = version if version != None else args_dict['version']
    args_dict['memory'] = memory if memory != None else args_dict['memory']
    args_dict['cf_page_url'] = cf_page_url if cf_page_url != None else args_dict['cf_page_url']
    args_dict['cf_api_key'] = cf_api_key if cf_api_key != None else args_dict['cf_api_key']
    validate_args(args_dict)
    save_args(args_dict)

# Does not yet work
def execute_minecraft_command(command):
    command = f"docker exec mc rcon-cli {command}"
    execute_docker_command(command)

def add_change(ui_element):
    ui_element.change(fn=assign, inputs=[server_type, online_mode, version, memory, cf_page_url, cf_api_key])

args_dict = load_args() 

with gr.Blocks() as home:
    with gr.Tab("Server Settings"):
        with gr.Row():
            server_type = gr.Dropdown(['VANILLA', 'AUTO_CURSEFORGE'], label='Server Type', value=args_dict['server_type'])
            minecraft_command = gr.Textbox(label="Minecraft Command", value="", interactive=False)
            send_command_btn = gr.Button('Execute Minecraft Command', variant="primary", interactive=True)

        with gr.Row():
            online_mode = gr.Checkbox(label="ONLINE MODE", value=args_dict['online_mode'])
            version = gr.Textbox(label="Version", value=args_dict['version'])
            memory = gr.Slider(1, 64, label="Memory", step=1, value=args_dict['memory'])

            start_btn = gr.Button("Start Server", variant="primary")
            debug_btn = gr.Button("Debug")
            stop_btn = gr.Button("Stop Server", variant="stop")

    with gr.Tab("CurseForge"):
        cf_page_url = gr.Textbox(label="CF_PAGE_URL", info="The url of the modpack page", value=args_dict['cf_page_url']) 
        cf_api_key = gr.Textbox(label="CF_API_KEY", value=args_dict['cf_api_key'])

    add_change(server_type)
    add_change(online_mode)
    add_change(version)
    add_change(memory)
    add_change(cf_page_url)
    add_change(cf_api_key)

    send_command_btn.click(fn=execute_minecraft_command, inputs=minecraft_command)
    start_btn.click(fn=start, outputs=send_command_btn)
    debug_btn.click(fn=debug)
    stop_btn.click(fn=stop, outputs=send_command_btn)

home.launch(server_name="0.0.0.0")
