from supervisely.app.widgets import Card, Container, Field, Input, SelectString, Button, FileViewer
import src.globals as g
import os

provider_selector = SelectString(
    values=["google", "s3", "azure"], labels=["google cloud storage", "amazon s3", "azure storage"]
)
provider = Field(title="Provider", content=provider_selector)

remote_path_input = Input()
connect_button = Button(text="Connect", icon="zmdi zmdi-cloud")
bucket_name = Field(
    title="Bucket name",
    content=Container(widgets=[remote_path_input, connect_button], direction="horizontal"),
)


card = Card(
    title="1️⃣ Connect to the cloud storage",
    description="Choose cloud service provider and bucket name",
    content=Container(
        widgets=[provider, bucket_name],
        direction="horizontal",
        gap=1,
        fractions=["1", "5"],
    ),
)

file_viewer = FileViewer(files_list=[])


@connect_button.click
def preview_items():
    bucket_name = provider_selector.get_value()
    remote_path = remote_path_input.get_value()

    path = f"{bucket_name}://{remote_path}"

    files = g.api.remote_storage.list(path, recursive=False, limit=g.USER_PREVIEW_LIMIT + 1)

    files = [f for f in files if f["type"] == "folder" or (f["type"] == "file" and f["size"] > 0)]
    tree_items = []
    for file in files:
        path = os.path.join(f"/{bucket_name}", file["prefix"], file["name"])
        tree_items.append({"path": path, "size": file["size"], "type": file["type"]})

    g.CURRENT_FILES = tree_items

    # card.update_data()
