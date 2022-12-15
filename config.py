
class Dataset_cfg():
    ann_dataset_dir_name = "ann_dataset"
    record_dataset_dir_name = 'record_dataset'
    target_dir = None 
    

class DB_cfg():
    db_name = 'test_db'
    host = 'localhost'
    user = 'root'
    charset = 'utf8'
    
    ann_dataset_table = Dataset_cfg().ann_dataset_dir_name
    ann_dataset_table_schema = f"""
                                    CREATE TABLE {ann_dataset_table} (
                                    id INT UNSIGNED NOT NULL AUTO_INCREMENT,
                                    json_name VARCHAR(200),
                                    image_name VARCHAR(200),
                                    ann_path VARCHAR(100),
                                    ann_version VARCHAR(10),
                                    PRIMARY KEY(id)
                                    );
                                """
    
    version = '0.0.0'
    
class DVC_cfg():
    remote_list = [[f"{Dataset_cfg().ann_dataset_dir_name}", "gs://ann_dataset_taeuk4958"],
                   [f'{Dataset_cfg().record_dataset_dir_name}', "gs://record_dataset_taeuk4958"]]
 
    default_remote = None