from huggingface_hub import hf_hub_download
import os

id = "Sparcos/TinyLlama_v1.1-qlora-finetunined-UFV_GGUF"
local_dir = "./model"
arquivo = "FP16.gguf"

if not os.path.exists(local_dir):
    os.makedirs(local_dir)

# Define a pasta temporária com espaço suficiente
temp_dir = "./temp_dir"  # Substitua pelo caminho de um diretório com espaço suficiente

# Certifique-se de que o diretório temporário existe
if not os.path.exists(temp_dir):
    os.makedirs(temp_dir)

# Defina a variável de ambiente para usar este diretório temporário
os.environ["HF_HOME"] = temp_dir



hf_hub_download(repo_id=id, filename=arquivo)

print(f"File downloaded to: {local_dir}")