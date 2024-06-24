from huggingface_hub import hf_hub_download
import os

repo_id = "Sparcos/TinyLlama_v1.1-qlora-finetunined-UFV_GGUF"
local_dir = "./model"
filename = "FP16.gguf"

if not os.path.exists(local_dir):
    os.makedirs(local_dir)

# Define a pasta temporária com espaço suficiente
temp_dir = "./temp_dir"  # Substitua pelo caminho de um diretório com espaço suficiente

# Certifique-se de que o diretório temporário existe
if not os.path.exists(temp_dir):
    os.makedirs(temp_dir)

# Defina a variável de ambiente para usar este diretório temporário
os.environ["HF_HOME"] = temp_dir

file_path = hf_hub_download(repo_id=repo_id, filename=filename, cache_dir=temp_dir)

# Move the downloaded file to the local directory
os.rename(file_path, os.path.join(local_dir, filename))
print(f"File downloaded to: {local_dir}")