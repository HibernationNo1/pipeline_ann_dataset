

def create_table(cursor, table_name, schema):
    cursor.execute(f"SHOW TABLES")
    fetchs = cursor.fetchall()
    if len(fetchs) !=0:
        tables = fetchs[0]
        if table_name not in tables:
            print(f"  mysql>> create table: {table_name}")
            cursor.execute(schema)
        else:
            print(f"  mysql>> table: {table_name} is already exist!")
    else:
        print(f"  mysql>> create table: {table_name}")
        cursor.execute(schema)
        
        
def whether_run_commit(cfg, database, image_list):
    print(f" >> confirm before commit to database: {cfg.db.db_name}")
    print(f" >>     number of images: {len(image_list)}")
    print(f" >>     category of dataset: {cfg.dvc.dataset_cate}")
    print(f" >>     version of annotations dataset: {cfg.dvc.ann_version}")
    print(f" >>\n           enter 'y' to commit ")
    commit = input()
    
    if commit in ["y", "Y", "yes"]: 
        print(" >>          run commit!")
        database.commit()
    else:
        print(f" >>     user enter `{commit}`, not commit to database...  ")