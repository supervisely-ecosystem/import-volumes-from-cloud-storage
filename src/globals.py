import os

import supervisely as sly
from dotenv import load_dotenv

if sly.is_development():
    load_dotenv("local.env")
    load_dotenv(os.path.expanduser("~/supervisely.env"))

api: sly.Api = sly.Api.from_env()

TEAM_ID = sly.env.team_id()
WORKSPACE_ID = sly.env.workspace_id()
STORAGE_DIR = sly.app.get_data_dir()

USER_PREVIEW_LIMIT = 100
FILE_SIZE = None
BATCH_SIZE = 10000
