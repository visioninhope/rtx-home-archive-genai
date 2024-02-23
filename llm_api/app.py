from flask import Flask, jsonify, request
from trt_llama_api import TrtLlmAPI
from utils import messages_to_prompt, completion_to_prompt, ChatMessage, MessageRole, DEFAULT_SYSTEM_PROMPT
import os
import json
import logging

# Initialize the Flask application
app = Flask(__name__)

def is_key_present(json_data, key):
    """Check if a key is present and not None in a JSON object."""
    try:
        if json_data[key] is None:
            return False
        return True
    except KeyError:
        return False

def read_json_config(file_path):
    """Read and return the JSON configuration from a file."""
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        logging.error(f"The file {file_path} was not found.")
    except json.JSONDecodeError:
        logging.error(f"There was an error decoding the JSON from the file {file_path}.")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
    return None

def get_model_configuration(config, model_name=None):
    """Retrieve model configuration from the config JSON based on the model name."""
    models = config["models"]["supported"]
    selected_model = next((model for model in models if model["name"] == model_name), models[0])
    return {
        "model_path": os.path.join(os.getcwd(), selected_model["metadata"]["model_path"]),
        "engine": selected_model["metadata"]["engine"],
        "tokenizer_path": os.path.join(os.getcwd(), selected_model["metadata"]["tokenizer_path"]),
        "max_new_tokens": selected_model["metadata"]["max_new_tokens"],
        "max_input_token": selected_model["metadata"]["max_input_token"],
        "temperature": selected_model["metadata"]["temperature"]
    }

# Load model configuration
config_file_path = 'config\\config.json'
app_config = read_json_config(config_file_path)
model_name_preference = None

if model_name_preference is None:
    model_name_preference = app_config["models"].get("selected")

model_settings = get_model_configuration(app_config, model_name_preference)
engine_path = model_settings["model_path"]
engine_name = model_settings["engine"]
tokenizer_directory = model_settings["tokenizer_path"]

verbose_logging = False
server_host = "0.0.0.0"
server_port = "8081"
disable_system_prompt = False

# Initialize the model API
llama_model_api = TrtLlmAPI(
    model_path=engine_path,
    engine_name=engine_name,
    tokenizer_dir=tokenizer_directory,
    temperature=0.1,
    max_new_tokens=2048,
    context_window=2048,
    messages_to_prompt=messages_to_prompt,
    completion_to_prompt=completion_to_prompt,
    verbose=verbose_logging
)

@app.route('/models/Llama2', methods=['POST', 'GET'])
@app.route('/v1/models/Llama2', methods=['POST', 'GET'])
def handle_llama2_model_request():
    """Endpoint to provide Llama2 model information."""
    model_info = {
        "id": "Llama2",
        "object": "model",
        "created": 1675232119,
        "owned_by": "Meta"
    }
    return jsonify(model_info)

@app.route('/models', methods=['POST', 'GET'])
@app.route('/v1/models', methods=['POST', 'GET'])
def handle_models_request():
    """Endpoint to list available models."""
    models_list = {
        "object": "list",
        "data": [
            {
                "id": "Llama2",
                "object": "model",
                "created": 1675232119,
                "owned_by": "Meta"
            },
        ],
    }
    return jsonify(models_list)

@app.route('/chat/completions', methods=['POST'])
@app.route('/v1/chat/completions', methods=['POST'])
def handle_chat_completions():
    """Endpoint for processing chat completion requests."""
    assert request.headers.get('Content-Type') == 'application/json'
    request_body = request.get_json()
    is_stream = False
    user_temperature = 1.0
    if is_key_present(request_body, "stream"):
        is_stream = request_body["stream"]
    if is_key_present(request_body, "temperature"):
        user_temperature = request_body["temperature"]
    
    prompt_text = ""
    formatted_request = False
    if "messages" in request_body:
        # Process and format chat messages
        prompt_text, formatted_request = format_chat_messages(request_body)
    elif "prompt" in request_body:
        prompt_text = request_body["prompt"]

    # Log input for verbose mode
    if verbose_logging:
        log_input_details(prompt_text, is_stream)

    # Invoke the model API based on whether streaming is enabled
    return process_completion_request(llama_model_api, prompt_text, is_stream, user_temperature, formatted_request)

@app.route('/completions', methods=['POST'])
@app.route('/v1/completions', methods=['POST'])
def handle_completions():
    """Endpoint for processing general completion requests."""
    assert request.headers.get('Content-Type') == 'application/json'
    request_body = request.get_json()
    is_stream = False
    user_temperature = 1.0
    if is_key_present(request_body, "stream"):
        is_stream = request_body["stream"]
    if is_key_present(request_body, "temperature"):
        user_temperature = request_body["temperature"]

    prompt_text = ""
    if "prompt" in request_body:
        prompt_text = request_body["prompt"]

    # Append prompt text to file (for logging or debugging purposes)
    log_prompt_to_file(prompt_text, is_stream)

    if not disable_system_prompt:
        # Prepend system prompt if enabled
        prompt_text = prepend_system_prompt(prompt_text)

    formatted_request = True

    # Process the completion request with model API
    return process_completion_request(llama_model_api, prompt_text, is_stream, user_temperature, formatted_request, get_stop_strings(request_body))

if __name__ == '__main__':
    app.run(server_host, port=server_port, debug=True, use_reloader=False, threaded=False)
