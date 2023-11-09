import os
import supervisely as sly
from supervisely.app.widgets import Button, Card, Container, Text, Input, Select

import src.globals as g
import src.ui.import_settings as import_settings
import src.ui.preview_bucket_items as preview_bucket_items

providers_info = g.api.remote_storage.get_list_available_providers()
providers = [provider["defaultProtocol"].rstrip(":") for provider in providers_info]

provider_items = [
    Select.Item(value=provider["defaultProtocol"].rstrip(":"), label=provider["name"])
    for provider in providers_info
]

provider_buckets = {
    provider["defaultProtocol"].rstrip(":"): [
        Select.Item(value=bucket, label=bucket) for bucket in provider["buckets"]
    ]
    for provider in providers_info
}

provider_selector = Select(
    items=provider_items,
    placeholder="Select cloud provider",
    width_percent=100,
)

provider_title = Text("<b>Provider</b>", "text")
provider = Container([provider_title, provider_selector])


bucket_items = []
if len(providers) > 0:
    bucket_items = provider_buckets[providers[0]]

bucket_name_selector = Select(
    items=bucket_items,
    filterable=True,
    placeholder="Select bucket",
    width_percent=100,
)

bucket_name_input = Input()
connect_button = Button(text="Connect", icon="zmdi zmdi-cloud")

bucket_name_title = Text("<b>Bucket name</b>", "text")
bucket_name = Container([bucket_name_title, bucket_name_selector])

card = Card(
    title="1️⃣ Connect to the cloud storage",
    description="Choose cloud service provider and bucket name",
    content=Container(
        widgets=[provider, bucket_name, connect_button],
    ),
)


@provider_selector.value_changed
def on_provider_changed(provider):
    if provider == "fs":
        bucket_name_title.set("<b>Storage ID</b>", "text")
    else:
        if bucket_name_title.text == "<b>Storage ID</b>":
            bucket_name_title.set("<b>Bucket name</b>", "text")

    bucket_name_selector.set(items=provider_buckets[provider])
    bucket_name_selector.set_value(None)


@connect_button.click
def preview_items():
    g.FILE_SIZE = {}
    provider = provider_selector.get_value()
    bucket_name = bucket_name_selector.get_value()

    path = f"{provider}://{bucket_name}"
    try:
        files = g.api.remote_storage.list(path, recursive=False, limit=g.USER_PREVIEW_LIMIT + 1)
    except Exception as e:
        sly.logger.warn(repr(e))
        raise sly.app.DialogWindowWarning(
            title="Can not find bucket or permission denied.",
            description="Please, check if provider / bucket name are "
            "correct or contact tech support",
        )

    files = [f for f in files if f["type"] == "folder" or (f["type"] == "file" and f["size"] > 0)]
    if len(files) > g.USER_PREVIEW_LIMIT:
        files.pop()

    tree_items = []
    for file in files:
        path = os.path.join(f"/{bucket_name}", file["prefix"], file["name"])
        tree_items.append({"path": path, "size": file["size"], "type": file["type"]})
        g.FILE_SIZE[path] = file["size"]
    preview_bucket_items.file_viewer.update_file_tree(files_list=tree_items)
    preview_bucket_items.card.show()
    import_settings.card.show()


@preview_bucket_items.file_viewer.path_changed
def refresh_tree_viewer(current_path):
    new_path = current_path
    provider = provider_selector.get_value()
    bucket_name = bucket_name_selector.get_value()
    g.FILE_SIZE = {}

    path = f"{provider}://{new_path.strip('/')}"
    try:
        files = g.api.remote_storage.list(path, recursive=False, limit=g.USER_PREVIEW_LIMIT + 1)
    except Exception as e:
        sly.logger.warn(repr(e))
        raise sly.app.DialogWindowWarning(
            title="Can not find bucket or permission denied.",
            description="Please, check if provider / bucket name are "
            "correct or contact tech support",
        )

    files = [f for f in files if f["type"] == "folder" or (f["type"] == "file" and f["size"] > 0)]

    if len(files) > g.USER_PREVIEW_LIMIT:
        files.pop()

    tree_items = []
    for file in files:
        path = os.path.join(f"/{bucket_name}", file["prefix"], file["name"])
        tree_items.append({"path": path, "size": file["size"], "type": file["type"]})
        g.FILE_SIZE[path] = file["size"]
    preview_bucket_items.file_viewer.update_file_tree(files_list=tree_items)
    preview_bucket_items.file_viewer.loading = False
