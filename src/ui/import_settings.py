import supervisely as sly
from supervisely.app.widgets import (
    Button,
    Card,
    Container,
    DestinationProject,
)

from supervisely.io.fs import mkdir, remove_dir, silent_remove

import src.globals as g

destination = DestinationProject(workspace_id=g.WORKSPACE_ID, project_type="volumes")


extract_button = Button(text="Start")
destination_container = Container(widgets=[destination, extract_button])

card = Card(
    "3️⃣ Output project",
    "Select output destination",
    collapsable=False,
    content=destination_container,
)
