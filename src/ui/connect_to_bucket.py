import os
import supervisely as sly
from supervisely.app.widgets import Button, Card, Container, Field, Input, SelectString

import src.globals as g
import src.ui.import_settings as import_settings
import src.ui.preview_bucket_items as preview_bucket_items

provider_selector = SelectString(
    values=["google", "s3", "azure"], labels=["google cloud storage", "amazon s3", "azure storage"]
)
provider = Field(title="Provider", content=provider_selector)

bucket_name_input = Input()
connect_button = Button(text="Connect", icon="zmdi zmdi-cloud")
bucket_name = Field(title="Bucket name", content=bucket_name_input)


card = Card(
    title="1️⃣ Connect to the cloud storage",
    description="Choose cloud service provider and bucket name",
    content=Container(
        widgets=[provider, bucket_name, connect_button],
    ),
)


@connect_button.click
def preview_items():
    g.FILE_SIZE = {}
    provider = provider_selector.get_value()
    bucket_name = bucket_name_input.get_value()

    path = f"{provider}://{bucket_name}"
    try:
        files = g.api.remote_storage.list(path, recursive=False, limit=g.USER_PREVIEW_LIMIT + 1)
        sly.logger.debug(msg=f"Current path: {path}.\nRefreshed items tree (try): {files}")

    except Exception as e:
        sly.logger.warn(repr(e))
        raise sly.app.DialogWindowWarning(
            title="Can not find bucket or permission denied.",
            description="Please, check if provider / bucket name are "
            "correct or contact tech support",
        )

    files = [f for f in files if f["type"] == "folder" or (f["type"] == "file" and f["size"] > 0)]
    sly.logger.debug(msg=f"Current path: {path}.\nInitial items tree before limit: {files}")

    if len(files) > g.USER_PREVIEW_LIMIT:
        files.pop()

    sly.logger.debug(msg=f"Current path: {path}.\nInitial items tree after limit: {files}")

    tree_items = []
    for file in files:
        path = os.path.join(f"/{bucket_name}", file["prefix"], file["name"])
        tree_items.append({"path": path, "size": file["size"], "type": file["type"]})
        g.FILE_SIZE[path] = file["size"]
    preview_bucket_items.file_viewer.update_file_tree(files_list=tree_items)
    preview_bucket_items.card.show()
    import_settings.card.show()
    sly.logger.debug(msg=f"Current path: {path}.\nInitial result items tree: {tree_items}")


@preview_bucket_items.file_viewer.path_changed
def refresh_tree_viewer(current_path):
    new_path = current_path
    provider = provider_selector.get_value()
    bucket_name = bucket_name_input.get_value()
    g.FILE_SIZE = {}

    path = f"{provider}://{new_path.strip('/')}"
    try:
        files = g.api.remote_storage.list(path, recursive=False, limit=g.USER_PREVIEW_LIMIT + 1)
        sly.logger.debug(msg=f"Current path: {current_path}.\nRefreshed items tree (try): {files}")

    except Exception as e:
        sly.logger.warn(repr(e))
        raise sly.app.DialogWindowWarning(
            title="Can not find bucket or permission denied.",
            description="Please, check if provider / bucket name are "
            "correct or contact tech support",
        )

    files = [f for f in files if f["type"] == "folder" or (f["type"] == "file" and f["size"] > 0)]
    sly.logger.debug(
        msg=f"Current path: {current_path}.\nRefreshed items tree before limit: {files}"
    )

    if len(files) > g.USER_PREVIEW_LIMIT:
        files.pop()

    sly.logger.debug(
        msg=f"Current path: {current_path}.\nRefreshed items tree after limit: {files}"
    )

    tree_items = []
    for file in files:
        path = os.path.join(f"/{bucket_name}", file["prefix"], file["name"])
        tree_items.append({"path": path, "size": file["size"], "type": file["type"]})
        g.FILE_SIZE[path] = file["size"]
    preview_bucket_items.file_viewer.update_file_tree(files_list=tree_items)
    preview_bucket_items.file_viewer.loading = False
    sly.logger.debug(
        msg=f"Current path: {current_path}.\nRefreshed result items tree: {tree_items}"
    )
    # sly.app.show_dialog(title=, description=, status="")
