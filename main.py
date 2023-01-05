import argparse
import os, os.path as osp

from hibernation_no1.configs.config import Config
from utils.dvc_utils import check_dvc_dataset_status
from utils.db_utils import create_table, whether_run_commit

import pymysql

def _parse_args():
    parser = argparse.ArgumentParser() 
    parser.add_argument("--cfg", required = True, help="path of config file") 
    
    parser.add_argument('--db_host', type = str, required= True,
                        help= "host account of database")
    parser.add_argument('--db_port', type = int, required = True, 
                        help= "port number to connect to database")
    parser.add_argument('--db_passwd', type = str, required = True,
                        help= "password to connect to database")
    
    parser.add_argument('--db_user', type = str, help= "user name to connect to database")
    parser.add_argument('--db_name', type = str, help= "database name to connect")
    
    
    args = parser.parse_args()
    
    return args


def set_config(args, cfg):
    if args.db_user is not None: cfg.db.user = args.db_user
    if args.db_name is not None: cfg.db.db_name = args.db_name
    

if __name__=="__main__":
    args  =_parse_args()
    
    cfg = Config.fromfile(args.cfg)
    set_config(args, cfg)
    
    image_list, json_list, target_dataset = check_dvc_dataset_status(cfg)
  
    target_dataset_dvc = osp.join(os.getcwd(), f"{target_dataset}.dvc")
    assert osp.isfile(target_dataset_dvc), f"\n>> Path: {target_dataset_dvc} is not exist!!"\
            f"\n>> run      $ dvc add {osp.basename(target_dataset_dvc).split('.')[0]}"
    
    database = pymysql.connect(host=args.db_host, 
                        port=args.db_port, 
                        user=cfg.db.user, 
                        passwd=args.db_passwd, 
                        database=cfg.db.db_name, 
                        charset=cfg.db.charset)
    cursor = database.cursor() 
    
    
    create_table(cursor, cfg.db.table.anns, cfg.db.table.anns_schema)
    create_table(cursor, cfg.db.table.image_data, cfg.db.table.image_data_schema)
    create_table(cursor, cfg.db.table.dataset, cfg.db.table.dataset_schema)

    num_results = cursor.execute(f"SELECT * FROM {cfg.db.table.anns} WHERE ann_version = '{cfg.dvc.ann.version}'")
    assert num_results == 0, f"ann version: {cfg.dvc.ann.version} has been stored in DB!!  "\
           f"\n     DB: {cfg.db.db_name},         table: {cfg.db.table.anns},     quantity: {num_results} "
    
   
                              
    # insert dataset to database
    for i, img_json_path in enumerate(zip(image_list, json_list)):
        image_path, json_path = img_json_path
        image_name, json_name = os.path.basename(image_path), os.path.basename(json_path)
        insert_sql = f"INSERT INTO {cfg.db.table.anns} "\
                     f"(json_name, image_name, category, ann_version) "\
                     f"VALUES('{json_name}', '{image_name}', '{cfg.dvc.dataset_cate}', '{cfg.dvc.ann.version}');"
        
        cursor.execute(insert_sql)
    
    num_results = cursor.execute(f"SELECT * FROM {cfg.db.table.anns} WHERE ann_version = '{cfg.dvc.ann.version}'")
    assert num_results == len(json_list), f"sql:: `INSERT INTO {cfg.db.table.anns}` didn't work"
    
    
    whether_run_commit(cfg, database, image_list)
    
    database.close()


    
    
