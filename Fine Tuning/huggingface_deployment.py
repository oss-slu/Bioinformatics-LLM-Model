from huggingface_hub import create_repo, upload_folder

repo_name = "Om368/Fine-tuned_CodeT5_Model"  # Example: "codet5-small-finetuned-r-code"
create_repo(repo_name, private=False)  # Set private=True if you want it private

# Upload your fine-tuned model
upload_folder(
    repo_id=repo_name,
    folder_path="./final_model",  # This is where your model + tokenizer are saved
    path_in_repo="",  # Upload everything at the root of the repo
)