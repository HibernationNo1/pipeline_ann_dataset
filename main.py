import argparse
import os, os.path as osp

from config import DVC_cfg, Dataset_cfg, DB_cfg
from database import update_db
from dvc_dataset import upload_dvc


# python main.py --port 3306 --passwd 7679 --screts client_secrets.json --ann --version 0.0.0
if __name__=="__main__":
    dvc_cfg, dataset_cfg, db_cfg = DVC_cfg(), Dataset_cfg(), DB_cfg()
    
    parser = argparse.ArgumentParser() 
    parser.add_argument('--port', type = int, required = True, 
                        help= "port number to connect to database")
    parser.add_argument('--passwd', type = str, required = True,
                        help= "password to connect to database")
    parser.add_argument('--commit', default= False, action="store_true",
                        help= "whether use commit to database")
    parser.add_argument('--version', default= str, help= "version of ann_dataset or recorc_dataset")
    
    parser.add_argument('--screts', type = str, required = True,
                        help= "path of client_secrets")
    
    
    parser.add_argument('--ann', default= False, action="store_true",  
                        help= "if True, run 'ann' mode")
    parser.add_argument('--record', default= False, action="store_true",  
                        help= "if True, run 'record' mode")
    
    
    
    
    args = parser.parse_args()
    
    assert (args.ann != args.record), f"Only one mode between 'ann' and 'record' shuold be runing"\
                                      f" [ann: {args.ann}, record: {args.record}]"
    assert osp.isfile(osp.join(os.getcwd(), args.screts)), f"Path that does not exist!  "\
                                                           f"path: [{osp.join(os.getcwd(), args.screts)}]"
                                                           
    if args.ann: dataset_cfg.target_dir = dvc_cfg.default_remote = dataset_cfg.ann_dataset_dir_name
    else: dataset_cfg.target_dir = dvc_cfg.default_remote = dataset_cfg.record_dataset_dir_name
        
    if args.version is not None: db_cfg.version = args.version
    
  
    update_db(db_cfg, dataset_cfg, 
              args.port, args.passwd, 
              ann = args.ann, commit = args.commit)
        
  
    upload_dvc(dvc_cfg, args.screts, db_cfg.version)