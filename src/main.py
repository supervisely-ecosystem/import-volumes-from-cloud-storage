import supervisely as sly
import src.globals as g

from supervisely.app.widgets import Container
import src.ui.connect_to_bucket as connect_to_bucket
import src.ui.preview_bucket_items as preview_bucket_items


# step_1 = Container(
#     widgets=[connect_to_bucket.card, video_player.card],
#     direction="horizontal",
#     gap=15,
#     fractions=[1, 1],
# )

layout = Container(
    widgets=[connect_to_bucket.card, preview_bucket_items.card],
    direction="vertical",
    gap=15,
)

app = sly.Application(layout=layout)
