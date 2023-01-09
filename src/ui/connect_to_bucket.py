import os

from supervisely.app.widgets import Button, Card, Container, Field, Input, SelectString

import src.globals as g
import src.ui.import_settings as import_settings
import src.ui.preview_bucket_items as preview_bucket_items

provider_selector = SelectString(
    values=["google", "s3", "azure"], labels=["google cloud storage", "amazon s3", "azure storage"]
)
provider = Field(title="Provider", content=provider_selector)

remote_path_input = Input()
connect_button = Button(text="Connect", icon="zmdi zmdi-cloud")
bucket_name = Field(title="Bucket name", content=remote_path_input)


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
    bucket_name = remote_path_input.get_value()

    path = f"{provider}://{bucket_name}"
    files = g.api.remote_storage.list(path, recursive=True, limit=g.USER_PREVIEW_LIMIT + 1)

    files = [f for f in files if f["type"] == "folder" or (f["type"] == "file" and f["size"] > 0)]
    tree_items = []
    for file in files:
        path = os.path.join(f"/{bucket_name}", file["prefix"], file["name"])
        tree_items.append({"path": path, "size": file["size"], "type": file["type"]})
        g.FILE_SIZE[path] = file["size"]
    preview_bucket_items.file_viewer.update_file_tree(files_list=tree_items)
    preview_bucket_items.card.show()
    import_settings.card.show()
