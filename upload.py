import subprocess
import os

secret_file_path = os.path.join(os.getcwd(), "adroit-producer-358501-0b55d0921ca3.json")
set_ = f"export GOOGLE_APPLICATION_CREDENTIALS='D:\Noh_TaeUk\pipeline_project\pipeline_dataset\adroit-producer-358501-0b55d0921ca3.json'"
print(f"set_ : {set_}")
exit()
set_2 = f"dvc remote modify --local bikes credentialpath '{secret_file_path}'"
subprocess.call([set_2], shell = True)