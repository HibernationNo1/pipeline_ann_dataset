import subprocess
import os, os.path as osp
import re
from dvc.config import Config



def dvc_print(srting):
    print(f"dvc >>   {srting}")


def get_dvc_config(remote_name):
    dvc_config_path = osp.join(Config().dvc_dir, "config")
    with open(dvc_config_path, "r") as dvc_config:
        if len(list(dvc_config)) <= 1:      # in here, will be erased all contents of 'dvc_config'
            dvc_print("No remote configuration!  run 'remote add'!")
            return None
    
    dvc_cfg_dict = dict()
    remotes = []
    urls = []
    with open(dvc_config_path, "r") as dvc_config:      # re open 'dvc_config'
        core_flag = False
        url_flag = False
        for i, line in enumerate(dvc_config):
            if i == 0 :
                if len(re.findall('core', line)) == 0:   # default remote not set
                    # set default remote
                    dvc_set_default_remote(dvc_cfg_dict, remote_name)
                    continue
                
                if re.findall('core', line)[0] == 'core' :
                    core_flag = True
                    continue
            
            if core_flag:
                dvc_cfg_dict['defualt_remote'] = line.split(" ")[-1].split("\n")[0]
                core_flag = False
                continue
            
            if len(line.split("[")) == 2: 
                remotes.append(line.split(" ")[-1].split("\"")[1]) 
                url_flag = True
                continue
            
            if url_flag:
                urls.append(line.split(" ")[-1].split("\n")[0])
                url_flag = False
    
    
    assert len(remotes) == len(urls)
    dvc_cfg_dict['remotes'] = []
    
    for remote, url in zip(remotes, urls):
        dvc_cfg_dict['remotes'].append(dict(remote = remote, url = url))

    return dvc_cfg_dict

def dvc_set_default_remote(dvc_cfg_dict, remote_name):
    assert remote_name is not None
    dvc_remote_default = f"dvc remote default {remote_name}"
    subprocess.call([dvc_remote_default], shell=True)
    dvc_cfg_dict['defualt_remote'] = remote_name
    

def dvc_set_remote(dvc_cfg):
    dvc_cfg_dict = get_dvc_config(dvc_cfg.default_remote)
    if dvc_cfg_dict is None:
        for remote in dvc_cfg.remote_list:
            remote_bucket_command = f"dvc remote add {remote[0]} {remote[1]}"
            subprocess.call([remote_bucket_command], shell=True)
        dvc_cfg_dict = get_dvc_config(dvc_cfg)
        assert dvc_cfg_dict is not None
    return dvc_cfg_dict
    

 
def dvc_git_push(dir_name, version):
    dir_paht = osp.join(os.getcwd(), dir_name)
    assert osp.isdir(dir_paht), f"path is not exist!!  path : {dir_paht}"
    
    dvc_add_command = f"dvc add {dir_name}/"
    subprocess.call([dvc_add_command], shell=True)
    subprocess.call(["dvc push"], shell=True)
    
    git_add_command = f"git add {dir_name}.dvc .gitignore"
    subprocess.call([git_add_command], shell=True)
    git_commit_command = f"git commit -m '{version}'"
    subprocess.call([git_commit_command], shell=True)
    subprocess.call(["git push"], shell=True)
    


def dvc_GCP_credentials(screts):
    client_secrets_path = osp.join(os.getcwd(), screts)
    assert osp.isfile(client_secrets_path), f"path is not exist!!  path : {client_secrets_path}"

    credentials_command = f"dvc remote modify --local bikes credentialpath '{client_secrets_path}'" 
    subprocess.call([credentials_command], shell=True)
        


def upload_dvc(dvc_cfg, screts, dataset_vers):   
    dvc_cfg_dict = dvc_set_remote(dvc_cfg)
    
    if dvc_cfg_dict['defualt_remote'] != dvc_cfg.default_remote:
        dvc_set_default_remote(dvc_cfg_dict, dvc_cfg.default_remote)
        
        
    dvc_GCP_credentials(screts)
    dvc_git_push(dvc_cfg.default_remote, dataset_vers)
    
    