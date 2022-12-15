import pymysql
import glob
import os

def print_mysql(str):
    print(f"mysql>>   {str}")

class Connect_DB():
    def __init__(self, database_name, host, port, user, passwd, charset):
        self.database_name = database_name
        self.host = host
        self.user = user
        self.charset = charset
        
        self.database = pymysql.connect(host=self.host, 
                                        port=port, 
                                        user=self.user, 
                                        passwd=passwd, 
                                        database=self.database_name, 
                                        charset=self.charset)
        
        self.print_connect_info()
        self.cursor = self.database.cursor()
        self.use_database()
        
    def print_connect_info(self):
        print_mysql(f"connect to database successfully!!     "
                    f"database: [{self.database_name}],     user : [{self.user}],     charset: [{self.charset}]")


    def check_table_exist(self, table_name, schema):
        self.cursor.execute(f"SHOW TABLES")
        fetchs = self.cursor.fetchall()
        if len(fetchs) !=0:
            tables = fetchs[0]
            if table_name not in tables:
                print_mysql(f"create table: [{table_name}]")
                self.cursor.execute(schema)
            else:
                print_mysql(f"table: [{table_name}] is already exist!")
        else:
            print_mysql(f"create table: [{table_name}]")
            self.cursor.execute(schema)
                    
    
    def use_database(self):
        use = f"USE {self.database_name};"
        self.cursor.execute(use)
    

    def commit(self):
        self.database.commit()
        
    def close(self):
        self.database.close()
        
        
    def return_result(self, result, table_name):
        if len(result) == 0:
            print_mysql(f"None selected in table: [{table_name}]")
            return ()
        else:
            return result
        
        
    def desc_table(self, table_name):
        self.cursor.execute(f"DESC {table_name};")
        result = self.cursor.fetchall()
        return self.return_result(result, table_name)
        
    def drop_table(self, table_name):
        self.cursor.execute(f"DROP {table_name};")
        print_mysql(f"drop table: '{'{table_name}'}'")


    def select_all(self, table_name):            
        self.cursor.execute(f"SELECT * FROM {table_name}")
        result = self.cursor.fetchall()
        return self.return_result(result, table_name)


def update_ann_table(db, db_cfg, dataset_cfg, commit = False):
    # create table
    db.check_table_exist(db_cfg.ann_dataset_table, 
                         db_cfg.ann_dataset_table_schema)  
    
    # comfirm dataset
    ann_path = os.path.join(os.getcwd(), dataset_cfg.ann_dataset_dir_name)
    image_list = glob.glob(ann_path +"/*.jpg")
    json_list = glob.glob(ann_path +"/*.json")
    assert len(image_list) == len(json_list), f"number of images and json files are not same!!  \n"\
           f"number of images {len(image_list)},     number of json files : {len(json_list)}"

    num_results = db.cursor.execute(f"SELECT * FROM {db_cfg.ann_dataset_table} WHERE ann_version = '{db_cfg.version}'")
    assert num_results == 0, f"ann version: {db_cfg.version} has been stored in DB!!  "\
           f"DB: [{db_cfg.db_name}],         table: [{db_cfg.ann_dataset_table}]"
    
    # insert dataset to database
    for i, img_json_path in enumerate(zip(image_list, json_list)):
        image_path, json_path = img_json_path
        image_name, json_name = os.path.basename(image_path), os.path.basename(json_path)
        insert_sql = f"INSERT INTO {db_cfg.ann_dataset_table} "\
                     f"(json_name, image_name, ann_path, ann_version) "\
                     f"VALUES('{json_name}', '{image_name}', '{ann_path}', '{db_cfg.version}');"
        db.cursor.execute(insert_sql)
        
    # result_desc = db.desc_table(db_cfg.ann_dataset_table)
    # print(f"result_desc ; {result_desc}")
    
    if commit: 
        print_mysql("run commit!")
        db.commit()
    db.close()


def update_db(db_cfg, dataset_cfg, port, passwd, ann = True, commit = False):
    db = connect_db(port, passwd, db_cfg)
    if ann:
        update_ann_table(db, db_cfg, dataset_cfg, commit = commit)
    else: 
        pass
        # updata_record_table()
    
    

def connect_db(port, passwd, db_cfg):
    # connect to database
    database_cfg = dict(database_name = db_cfg.db_name, 
                        host = db_cfg.host, 
                        port = port, 
                        user = db_cfg.user, 
                        passwd = passwd, 
                        charset = db_cfg.charset)
    db = Connect_DB(**database_cfg)
    return db


    

           
    

    
    
    
    
    
    