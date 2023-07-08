# Managing Dataset 

google cloud storage와 연동하여 dataset의 version을 관리하는 repository입니다.



## How to Use

### install dvc 

```
$ pip install dvc[gs]
```



#### + initialize

1. git init

   ```
   $ git init
   ```

2. dvc init

   ```
   $ dvc init
   ```





#### + set remote

remote는 아래와 같이 구성했습니다.

1. **`ann_dataset`**: `url = gs://ann_dataset_hibernation`
2. **`train_dataset`**: `url = gs://train_dataset_hibernation`



- add

  ```
  $ dvc remote add -d ann_dataset gs://ann_dataset_hibernation
  ```

- set default

  ```
  $ dvc remote default ann_dataset 
  ```

> bucket name: **ann_dataset_hibernation** 인 경우







### dvc push to google storage

#### 1. dvc add dataset

```
$ dvc add ann_dataset/board_dataset
```

`ann_dataset/board_dataset` 하위 `.gitignore`, `board_dataset.dvc` 파일은 git으로 version관리하게 됩니다.



#### 2. dvc push

```
$ dvc push
```

> 이 과정을 최초로 수행할 때 아래 출력이 나오며 인증 과정이 필요.
>
> ```
> Go to the following link in your browser:
> 
>     https://accounts.google.com/o/oauth2/auth?client_id=710796635688-iivsgbgsb6uv1fap6635dhvuei09o66c.apps.googleusercontent.com&redirect_uri=urn%3Aietf%3Awg%3Aoauth%3A2.0%3Aoob&scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fdrive+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fdrive.appdata&access_type=offline&response_type=code&approval_prompt=force
> 
> Enter verification code:
> ```
>
> 인증을 수행하는 과정에서 아래와 같은 code를 얻을 수 있습니다. (아래는 예시 code)
>
> ```
> 4/1AdQt8qgp7fYSoMCqitgBxY7BOOgrbDqZJ8m6o06Lqu3oRgCdJwjB
> ```
>
> 이를 `Enter verification code:` 에 입력 후 아래 출력 확인
>
> ```
> Authentication successful.
> ```

- google storage에 접근 권한을 갖기 위해 google cloud `credentials`을 통해 프로젝드에 대한 엑세스 권한을 부여했습니다.

  접속 key값은 해당 dir에 `client_secrets.json`으로 저장했으며, `.gitignore`에 포함시켜 사용자 개인이 직접 관리하도록 합니다.

  

  `client_secrets.json`의 path는 `.dvc/config/local`에 명시하여 **`dvc push`**를 수행 시 참조되도록 했습니다.

  ```
  $ dvc remote modify --local {remote name} credentialpath {path of client_secrets.json}
  ```

  

## Insert dataset information into DataBase

#### 1. Create DateBase

Ubuntu 20.03의 환경에 Mysql DB를 구축했습니다.

1. install mysql

   ```
   $ sudo apt-get update
   $ sudo apt-get install mysql-server
   $ sudo ufw allow mysql					# set open 3306 port
   $ sudo systemctl enable mysql			# restart mysql automatically when ubuntu reboot
   ```

   ```
   $ sudo mysql -u root -p 
   ```

   

2. create user

   ```
   mysql> GRANT ALL PRIVILEGES ON *.* TO 'hibernation'@'%' WITH GRANT OPTION;		
   ```

   > confirm
   >
   > ```
   > mysql> SELECT User, Host, authentication_string FROM mysql.user;
   > ```

3. create database

   ```
   mysql> CREATE DATABASE pipeline_database DEFAULT CHARACTER SET=utf8 COLLATE=utf8_bin;
   ```

   ```
   mysql> FLUSH PRIVILEGES;
   ```

   > confirm
   >
   > ```
   > mysql> SHOW DATABASES;
   > ```



추가로 해당 DB에 외부에서 접근이 가능하게 하기 위해 mysql의 설정 file을 변경했습니다.

```
$ sudo vi /etc/mysql/mysql.conf.d/mysqld.cnf
```

```
bind-address            = 0.0.0.0 			# 127.0.0.1  >> 0.0.0.0 으로 변경
```

```
$ sudo systemctl restart mysql
```



#### 2. Insert into DataBase

`DVC`, `MySQL` python SDK를 활용하여 특정 device에 구축된 DB에 dataset의 각 data에 대한 정보를 저장합니다.

```
python main.py \
    --cfg configs/config.py \
    --db_host 192.168.219.100 \
    --db_port **** \
    --db_passwd ****  
```







**DB map**

- **ann_data**(table) : image data에 대한 라벨링 정보를 담고 있는 json format의 file에 대한 정보를 담은 table입니다.

  - `id`(column) 

  - `json_name`(column) : path of `.json` file

  - `image_name`(column) : path of `.jpg` image file 

  - `category`(column) : category of annotation dataset 

    > ex) `test_dataset`, `board_dataset`

  - `ann_version`(column) : version of annotation dataset 

  

- **image_data**(table) : 라벨링이 완료된 jpg format의 image에 대한 정보를 담은 table입니다.

  - `id`(column) 

  - `dataset_purpose`(column) :  purpose of using the image during training. one of `train` and `val`

  - `image_name`(column) : path of `.jpg` image file 

  - `record_file`(column): path of the file that labeling information is recorded

    > ex) `train_dataset.json`, `val_dataset.json`

  - `category`(column) : category of annotation dataset 

  - `record_version`(column) : version of recorded dataset 

  

- **train_data**(table) : 라벨링이 완료된 jpg format의 image에 대한 정보를 담은 table입니다.

  - `id`(column) 
  - `dataset_purpose`(column) :  purpose of using the image during training. one of `train` and `val`
  - `category`(column) : category of annotation dataset 
  - `record_file`(column): path of the file that labeling information is recorded
  - `record_version`(column) : version of recorded dataset 

