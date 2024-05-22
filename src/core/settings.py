import os
from dotenv import load_dotenv
import logging

# current_dir = os.path.dirname(__file__)
# parent_dir = os.path.dirname(current_dir)
# env_path = os.path.join(parent_dir, '.env')
# print(env_path)
#
# load_dotenv(env_path)

load_dotenv()

config = {}
config["db_user"] = os.environ.get("db_user")
config["db_password"] = os.environ.get("db_password")
config["db_host"] = os.environ.get("db_host")
config["db_port"] = os.environ.get("db_port")
config["db_name"] = os.environ.get("db_name")

config[
    "dsl"
] = f"postgresql+psycopg2://{config['db_user']}:{config['db_password']}@{config['db_host']}:{config['db_port']}/{config['db_name']}"

config["app_key"] = os.environ.get("app_key")
config["debug"] = os.environ.get("debug")


log_settings = {
    "dir_name": "logs",
    "file_name": "app.log",
    "log_level": logging.INFO,
    "log_size": 10024,
    "backup_num": 5,
}
