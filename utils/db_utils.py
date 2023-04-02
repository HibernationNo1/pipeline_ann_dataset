def whether_run_commit(cfg, database, image_list):
    print(f" >> confirm before commit to database: {cfg.db.db_name}")
    print(f" >>     number of images: {len(image_list)}")
    print(f" >>     category of dataset: {cfg.dvc.target_dataset.category}")
    print(f" >>     version of annotations dataset: {cfg.dvc.target_dataset.version}")
    print(f" >>\n           enter 'y' to commit ")
    commit = input()
    
    if commit in ["y", "Y", "yes"]: 
        print(" >>          run commit!")
        database.commit()
    else:
        print(f" >>     user enter `{commit}`, not commit to database...  ")
        
        

def create_table(cursor, table_name: str, schema: str):
    """ create table_name if dose not exist in database 

    Args:
        cursor : database.cursor
        table_name (str): name of table
        schema (str): schema of expected table
    """
    cursor.execute(f"SHOW TABLES")
    fetchs = cursor.fetchall()
    
    tables = []
    if len(fetchs) !=0:
        for fetch in fetchs:
            tables.append(fetch[0])
    else:
        print(f"  mysql>> create table: {table_name}")
        cursor.execute(schema)
    
    if len(fetchs) !=0:
        if table_name not in tables:
            print(f"  mysql>> create table: {table_name}")
            cursor.execute(schema)
        else:
            print(f"  mysql>> table: {table_name} is already exist!") 
    
    check_table_exist(cursor, table_name)     
            


def check_table_exist(cursor, table_name):
    """ check tables are exist in database

    Args:
        cursor : pymysql.connect.cursor  
        table_name (str): table names
        after_create: whether run immediately after table creation
    """
    
    if isinstance(table_name, dict):
        table_names = []
        for _, name in table_name.items():
            table_names.append(name)
    elif isinstance(table_name, list):
        table_names = table_name
    elif isinstance(table_name, str):
        table_names = [table_name]
    else: raise TypeError(f" `table_name` type must be dict or list or str!")
    
    cursor.execute(f"SHOW TABLES")
    fetchs = cursor.fetchall()
    
    tables = []
    if len(fetchs) !=0:
        for fetch in fetchs:
            tables.append(fetch[0])
    else:
        raise AttributeError(f"Table does not exist in the database!")

    for table_name in table_names :
        if table_name not in tables:
            raise AttributeError(f"Table: {table_name} is not exist in database!")