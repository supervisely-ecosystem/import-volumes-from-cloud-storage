from supervisely.app.widgets import Card, FileViewer

file_viewer = FileViewer(
    files_list=[],
    extended_selection=True,
)

card = Card(
    title="2️⃣ Preview bucket and select items",
    description="All selected volumes/directories will be imported",
    content=file_viewer,
)

card.hide()
