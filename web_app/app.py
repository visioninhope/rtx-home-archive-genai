from flask import Flask, request, render_template, send_from_directory, url_for, jsonify
import uuid
import os
from vector_db_chroma import chroma_collection, chroma_client
from PIL import Image
from werkzeug.utils import secure_filename
import fitz  # PyMuPDF
import chromadb
from langchain.text_splitter import RecursiveCharacterTextSplitter
from chromadb.utils import embedding_functions
import io
from PIL import Image
import requests
import logging
import re
# Make sure Tesseract OCR is installed
# for Windows see https://github.com/UB-Mannheim/tesseract/wiki
# for Linux, Mac see https://tesseract-ocr.github.io/tessdoc/Installation.html
import pytesseract
from flask import make_response
from auth import authenticate, login_required, roles_required
from flask import redirect



app = Flask(__name__)

app.secret_key = 'e95dbfb1266a5eb1bfcfacc52015f937'

llama2_llm_url= "http://localhost:8081/v1/chat/completions"

# Set the Tesseract command to include the full path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'

pytesseract_text_extract_path = r'C:\Users\tarun\private_contents\image_text'


import subprocess

def get_tesseract_version():
    try:
        # Set the path to the Tesseract executable
        tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
        # Run the command 'tesseract --version'
        result = subprocess.run([tesseract_cmd, '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        # Return the standard output (stdout)
        return result.stdout
    except Exception as e:
        # In case of any errors, return the error message
        return str(e)

# Call the function and print the result
print(get_tesseract_version())


# Where to store the uploaded images
# Initialize text splitter and embeddings
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
#embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-large-en-v1.5")
embeddings = embedding_functions.DefaultEmbeddingFunction()

# Where to store the images
PRIVATE_CONTENT_PATH = 'C:\\Users\\tarun\\private_contents'

app.config['UPLOAD_FOLDER'] = PRIVATE_CONTENT_PATH

@app.route('/upload_view')
@login_required
def upload_view():
    return render_template('Upload.html')

@app.route('/login', methods=['POST'])
def login():
    # Assuming `authenticate` returns a user object on success
    user = authenticate(request.form['username'], request.form['password'])
    if user:
        response = make_response(redirect(url_for('home')))
        # Set a secure cookie. Consider adding `secure=True` and `httponly=True` in production
        response.set_cookie('user_id', user['userId'], httponly=True)
        return response
    else:
        return render_template('login.html', error='Invalid credentials')

@app.route('/admin_dashboard')
@roles_required('admin')
def admin_dashboard():
    return render_template('admin_dashboard.html')

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/home')
@login_required
def home():
    return render_template('home.html')

@app.route('/logout')
@login_required
def logout():
    response = make_response(redirect(url_for('/')))
    response.set_cookie('user_id', '', expires=0)
    return response


@app.route('/explore')
@roles_required('family_member', 'admin')
def explore():
    return render_template('Explore.html')

# Function to convert PDF to text
def pdf_to_text(file_path):
    pdf_file = open(file_path, 'rb')
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page_num in range( len(pdf_reader.pages)):
        text += pdf_reader.pages[page_num].extract_text()
    pdf_file.close()
    return text

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif', 'pdf'}

def is_image_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}


@app.route('/upload', methods=['POST'])
@roles_required('family_member', 'admin','guest')
def upload():
    try:
        tags = request.form.getlist('tags[]')  # Retrieve tags
        print("Tags: ", tags)  # Debugging line to check the received tags
        if 'file' not in request.files:
            return {'message': 'No file part'}, 400
        file = request.files['file']
        if file.filename == '':
            return {'message': 'No selected file'}, 400

        # Process the uploaded file
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_id = str(uuid.uuid4()) + filename
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file_id)
            file.save(filepath)
        
       

        # Determine if the file is an image or a text document
        if is_image_file(filename):
            # Extract text from the image
            text = extract_text_from_image(filepath,file_id)
        else:
            # Open the saved PDF file and read text from the document
            with fitz.open(filepath) as pdf:  # This opens the file from the saved path
                text = ''
                for page in pdf:
                    text += page.get_text()
        
        text_filename = os.path.splitext(file_id)[0] + '.txt'
        text_filepath = os.path.join(app.config['UPLOAD_FOLDER'], text_filename)
        # Write the extracted text to a new text file
        with open(text_filepath, 'w', encoding='utf-8') as text_file:
            text_file.write(text)
        
        summary = get_text_summary(filename,text)
        # print(summary)

        summary_text_filename = os.path.splitext(file_id)[0] + '_summary.txt'
        summary_text_filepath = os.path.join(app.config['UPLOAD_FOLDER'], summary_text_filename)
        # Write the extracted text to a new text file
        with open(summary_text_filepath, 'w', encoding='utf-8') as text_file:
            text_file.write(summary)

        # Split text into chunks
        chunks = text_splitter.split_text(text)


        # Convert chunks to vector representations and store in Chroma DB
        documents_list = []
        embeddings_list = []
        ids_list = []
        metadatas_list = []
        metadata_for_document = {"tags": ', '.join(tags)}
        metadatas_list.append(metadata_for_document)
        
        #for i, chunk in enumerate(chunks):
        vector = embeddings([chunks[0]])[0]
        
        documents_list.append(chunks[0])
        embeddings_list.append(vector)
        ids_list.append(f"{file_id}")
       
            
    # print(ids_list)

        chroma_collection.add(
            embeddings=embeddings_list,
            documents=documents_list,
            ids=ids_list,
            metadatas=metadatas_list 
        )
        #chroma_client.persist()
        return {'message': 'File processed', 'job_id': filename}, 200
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return {'message': 'An error occurred during file processing', 'error': str(e)}, 500



def extract_text_from_image(image_path,file_id):

    extracted_image2text_path = "C:\\Users\\tarun\\private_contents\\image_text\\"+file_id

    # Define the Tesseract command
    run_tesseract_cmd = ["C:\\Program Files\\Tesseract-OCR\\tesseract", image_path, extracted_image2text_path]

    # Execute the command
    subprocess.run(run_tesseract_cmd, check=True)
    # Read and print the output text
    with open(extracted_image2text_path+".txt", 'r') as file:
        extracted_text = file.read()
    print("Good extract_text_from_image")
    return extracted_text     

from flask import Flask, send_file, safe_join, abort
import os


@app.route('/doc/<job_id>', methods=['GET'])
@login_required
def get_doc(job_id):
    try:
        file_path = safe_join(PRIVATE_CONTENT_PATH, job_id)
    except ValueError:
        abort(400, "Invalid path.")

    if os.path.exists(file_path) and os.path.isfile(file_path):
        return send_file(file_path)
    else:
        abort(404, description="File not found")


@app.route('/files/<filename>')
@login_required
def serve_private_file(filename):
    try:
        # Prevent directory traversal attack
        return send_from_directory(PRIVATE_CONTENT_PATH, filename, as_attachment=False, download_name=None)
    except FileNotFoundError:
        abort(404)


@app.route('/browse', methods=['GET'])
@login_required
def retrieve_doc():
    prompt_text = request.args.get('prompt')
    tags = request.args.getlist('tags[]')
    print(tags)

    



    if not prompt_text:
        return jsonify({"error": "No prompt provided"}), 400
    
    query_vector = embeddings([prompt_text]) if prompt_text else None

    # Query Chroma DB with the vector representation
    results = chroma_collection.query(query_embeddings=query_vector if query_vector else None, n_results=10,include=["metadatas", "documents", "distances"])

   #print(results)

    response_data = []
    for i, doc_id in enumerate(results['ids']):
        # Remove file extension and prefix with PRIVATE_CONTENT_PATH
        file_name = os.path.splitext(results['ids'][i][0])[0] + '_summary.txt'
        file_path = os.path.join(PRIVATE_CONTENT_PATH, file_name)
        print(file_path)
        # Attempt to load content of the file as text
        try:
            with open(file_path, 'r') as file:
                doc_text = file.read()
                print(doc_text)
        except FileNotFoundError:
        # If summary file not found, use original document text
            doc_text = results['documents'][i][0]

        doc_tags = results['metadatas'][i][0]  # Assuming tags are stored as a string
        print(doc_tags)
        file_url = url_for('serve_private_file', filename=results['ids'][i][0], _external=True)
        response_data.append({"url": file_url, "text": doc_text, "tags": doc_tags})

    return jsonify(response_data)


# Define the route for explaining text
@app.route('/explain_text', methods=['POST'])
@login_required
def explain_text():
    data = request.json
    logging.debug("Received data: %s", data)

    DocumentTitle = "General Personal Document"
    selectedText = data.get('selectedText')

    logging.debug("Document Title: %s", DocumentTitle)
    logging.debug("Selected Text: %s", selectedText)

    messages = [
        {
            "role": "system",
            "content": "You are an AI trained to provide maximum three lines precise explanations of text content. Aim to clarify, elucidate, and expand upon the given content where possible."
        },
        {
            "role": "user",
            "content": f"I need an explanation for this text from the document titled '{DocumentTitle}': {selectedText}"
        }
    ]

    payload = {
        "messages": messages
    }

    response = requests.post(llama2_llm_url, json=payload)  
    

    logging.debug("GenAI response: %s", response.json())

    if response.status_code == 200:
        try:
            explanation = response.json().get('choices', [{}])[0].get('message', {}).get('content', '')
            explanation = re.sub(r'</.*?>', '', explanation)
            return jsonify({"explanation": explanation})
        except KeyError as e:
            logging.error("Error parsing the response: %s", e)
            return jsonify({"error": "Failed to parse the explanation from the AI model."}), 500
    else:
        logging.error("Model response error: Status code %s", response.status_code)
        return jsonify({"error": "Failed to get a valid response from the AI model."}), response.status_code



@app.route('/summarize_text', methods=['POST'])
@login_required
def summarize_text():
    data = request.json
    logging.debug("Received data: %s", data)

    DocumentTitle = "General Personal Document"
    selectedText = data.get('selectedText')

    logging.debug("Document Title: %s", DocumentTitle)
    logging.debug("Selected Text: %s", selectedText)

    messages = [
        {
            "role": "system",
            "content": "You are an AI trained to provide concise summaries. Aim to condense and highlight the main points or insights from the given content where possible."
        },
        {
            "role": "user",
            "content": f"I need a summary for this text from the document titled '{DocumentTitle}': {selectedText}"
        }
    ]

    payload = {
        "messages": messages
    }

    response = requests.post(llama2_llm_url, json=payload)  

    logging.debug("GenAI response: %s", response.json())

    if response.status_code == 200:
        try:
            summary = response.json().get('choices', [{}])[0].get('message', {}).get('content', '')
            summary = re.sub(r'</.*?>', '', summary)
            return jsonify({"summary": summary})
        except KeyError as e:
            logging.error("Error parsing the response: %s", e)
            return jsonify({"error": "Failed to parse the summary from the AI model."}), 500
    else:
        logging.error("Model response error: Status code %s", response.status_code)
        return jsonify({"error": "Failed to get a valid response from the AI model."}), response.status_code



def get_text_summary(DocumentTitle,selectedText):

    messages = [
        {
            "role": "system",
            "content": "You are an AI trained to provide concise summaries. Aim to condense and highlight the main points or insights from the given content where possible."
        },
        {
            "role": "user",
            "content": f"I need a summary for this text from the document titled '{DocumentTitle}': {selectedText}"
        }
    ]

    payload = {
        "messages": messages
    }

    response = requests.post(llama2_llm_url, json=payload)  


    if response.status_code == 200:
        try:
            summary = response.json().get('choices', [{}])[0].get('message', {}).get('content', '')
            summary = re.sub(r'</.*?>', '', summary)
            return summary
        except KeyError as e:
            logging.error("Error parsing the response: %s", e)
            return "Error parsing the response"
    else:
        logging.error("Model response error: Status code %s", response.status_code)
        return "Error parsing the response"




# AI Blog Content


@app.route('/explore_document')
@login_required
def explore_document():
    docName = request.args.get('docName', 'Default Document Title')
    # You might want to set a more meaningful default or handle the absence of docName differently
    return render_template('explore_document.html', document_title=docName.replace('.txt', '').replace('_', ' ').title())


@app.route('/get_ai_generated_blog')
@login_required
def get_ai_generated_blog():
    docName = request.args.get('docName')
    filePath = os.path.join(PRIVATE_CONTENT_PATH, docName)
    try:
        with open(filePath, 'r', encoding='utf-8') as file:
            text = file.read()
            ai_content = generate_blog_content_from_text(text)
            return jsonify(ai_content)
    except FileNotFoundError:
        return jsonify({"error": "Document not found"}), 404
    except Exception as e:
        return jsonify({"error": f"Failed to process the document: {str(e)}"}), 500


def generate_blog_content_from_text(document_text):
    """
    Sends the document text to the AI model to generate a blog post title and HTML content.
    """
    
    # Refined AI model prompt
    prompt = f"""
    Create a blog post with the following guidelines:
    - Start with a blog post title that captures the essence of the document text, followed immediately by 'Title End'.
    - Immediately after the title indication, begin the HTML content with 'Content Start', ensuring no additional text or instructions precede it.
    - Use Tailwind CSS for styling, with a consistent text color of black. Apply bold or distinctive styles to headers or sections to highlight them effectively.
    - Incorporate Font Awesome icons where relevant to enhance the content visually and support the narrative or points made.
    - Organize the content into an engaging introduction, informative sections throughout the body, and a succinct conclusion that summarizes the key points.
    - Conclude the HTML content with 'Content End', directly after the content's conclusion without adding any extraneous text or instructions.
    - Aim for a clean, professional design that adheres to fundamental design principles, enhancing the reader's experience and engagement with the content.

    Document Text:
    {document_text}
    """





    messages = [
        {
            "role": "system",
            "content": "You are an AI trained to generate blog post titles and structured HTML content from provided text. Create a title, introduction, main sections, and a conclusion."
        },
        {
            "role": "user",
            "content": prompt
        }
    ]

    payload = {
        "messages": messages
    }

    print(payload)

    try:
        response = requests.post(llama2_llm_url, json=payload)  
        if response.status_code == 200:
            output = response.json().get('choices', [{}])[0].get('message', {}).get('content', '')
            output = parse_ai_output(output)
            # Simplified: Directly returning the output for integration into the response.
            # You may need to further parse or clean this output depending on the AI's response format.
            return output
        else:
            logging.error("Model response error: Status code %s", response.status_code)
            return "Error from AI model"
    except Exception as e:
        print(str(e))
        logging.error("Failed to generate blog content: %s", str(e))
        return "Failed to communicate with AI model"

def parse_ai_output(output):
    title_end_index = output.find('Title End')
    content_start_index = output.find('Content Start', title_end_index)
    content_end_index = output.find('Content End', content_start_index)

    title = output[:title_end_index].strip()
    content = output[content_start_index+len('Content Start'):content_end_index].strip()

    return title, content

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8894, debug=True, use_reloader=True)