import supervisely as sly
from supervisely.app.widgets import Card, FileViewer

import src.globals as g

card = Card(
    title="2️⃣ Preview bucket and select items",
    description="All selected volume/directories will be imported",
    content=FileViewer(files_list=g.CURRENT_FILES),
)
