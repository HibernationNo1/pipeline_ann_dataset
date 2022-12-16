import os, os.path as osp
import glob
import re
from dvc.config import Config


def check_dvc_config(remote_user_config):
    dvc_config_path = osp.join(Config().dvc_dir, "config")
    with open(dvc_config_path, "r") as dvc_config:
        # in here, will be erased all contents of 'dvc_config'
        assert len(list(dvc_config)) > 2,  "No remote configuration!  run 'remote add'!"
           
    
    dvc_cfg = dict()
    remotes = []
    urls = []
    with open(dvc_config_path, "r") as dvc_config:      # re open 'dvc_config'
        core_flag = False
        url_flag = False
        for i, line in enumerate(dvc_config):
            if i == 0 :
                if len(re.findall('core', line)) == 0:   # default remote not set
                    raise OSError(f"default remote is not set!!  \n"\
                                   "run:    $ dvc remote default `remote_name`")
                    
                
                if re.findall('core', line)[0] == 'core' :
                    core_flag = True
                    continue
            
            if core_flag:
                dvc_cfg['defualt_remote'] = line.split(" ")[-1].split("\n")[0]
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
    dvc_cfg['remotes'] = []
    
    for remote, url in zip(remotes, urls):
        dvc_cfg['remotes'].append(dict(remote = remote, url = url))
        
        
    if dvc_cfg['defualt_remote'] != remote_user_config: 
        raise OSError(f"Defualt_remote '.dvc/config: {dvc_cfg['defualt_remote']}' and "\
                      f"'cfg: {remote_user_config}' are not same!!")

    return dvc_cfg


def check_dvc_dataset_status(cfg):
    target_dataset = osp.join(os.getcwd(), cfg.dvc.dataset_cate)
    assert osp.isdir(target_dataset), f"\n>> Path: {target_dataset} is not exist!!"  
    
    # comfirm dataset quantity
    image_list = glob.glob(target_dataset +"/*.jpg")
    json_list = glob.glob(target_dataset +"/*.json")
    assert len(image_list) == len(json_list), f"number of images and json files are not same!!  \n"\
        f"number of images {len(image_list)},     number of json files : {len(json_list)}"\
    
    dvc_cfg = check_dvc_config(cfg.dvc.remote)
    
    credentials = osp.join(os.getcwd(), ".dvc", "config.local")
    assert osp.isfile(credentials), f"\n  >> Path: {credentials} is not exist!!   "\
        f"set google storage credentials! "\
        f"\n  >> run:   $ dvc remote modify --local {dvc_cfg['defualt_remote']} credentialpath `client_secrets_path`"
                                    
    return image_list, json_list