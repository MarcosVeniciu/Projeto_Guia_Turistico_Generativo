from huggingface_hub import hf_hub_download

hf_hub_download(repo_id="Sparcos/TinyLlama_v1.1-qlora-finetunined-UFV_GGUF", filename="FP16.gguf", local_dir="./model")