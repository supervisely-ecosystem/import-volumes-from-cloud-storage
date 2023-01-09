import supervisely as sly
import os
from supervisely.app.widgets import (
    Button,
    Card,
    Container,
    DestinationProject,
    Checkbox,
    Text,
    ProjectThumbnail,
    Progress,
)

from supervisely.io.fs import (
    get_file_ext,
    get_file_name,
)

import src.ui.connect_to_bucket as connect_to_bucket
import src.ui.preview_bucket_items as preview_bucket_items

import src.globals as g

anonym_checkbox = Checkbox(content=Text(text="Anonymize patient name and ID for DICOM files"))
destination = DestinationProject(workspace_id=g.WORKSPACE_ID, project_type="volumes")
import_button = Button(text="Start")

progress_bar = Progress()
progress_bar.hide()

output_project = ProjectThumbnail()
output_project.hide()

destination_container = Container(
    widgets=[anonym_checkbox, destination, import_button, progress_bar, output_project]
)

card = Card(
    "3️⃣ Output project",
    "Select output destination",
    collapsable=False,
    content=destination_container,
)

card.hide()


@import_button.click
def import_volumes():
    progress_bar.hide()
    output_project.hide()

    paths = preview_bucket_items.file_viewer.get_selected_items()
    remote_paths = []
    local_paths = []

    provider = connect_to_bucket.provider_selector.get_value()
    bucket_name = connect_to_bucket.remote_path_input.get_value()

    def _add_to_processing_list(path):
        nonlocal remote_paths, local_paths
        if sly.volume.has_valid_ext(path) is False:
            sly.logger.warning(f"Unsupported volume extension for path: {path}")
            return
        full_remote_path = f"{provider}://{path.lstrip('/')}"
        remote_paths.append(full_remote_path)
        local_path = os.path.join(g.STORAGE_DIR, path.lstrip("/"))
        sly.fs.ensure_base_path(local_path)
        local_paths.append(local_path)

    # find selected dirs
    selected_dirs = []
    for path in paths:
        if sly.fs.get_file_ext(path) == "":
            # path to directory
            selected_dirs.append(path)

    # get all files from selected dirs
    if len(selected_dirs) > 0:
        g.FILE_SIZE = {}
        for dir_path in selected_dirs:
            full_dir_path = f"{provider}://{dir_path.strip('/')}"
            files_cnt = 0
            for file in list_objects(g.api, full_dir_path):
                if file["size"] <= 0:
                    continue

                path = os.path.join(f"/{bucket_name}", file["prefix"], file["name"])
                g.FILE_SIZE[path] = file["size"]
                files_cnt += 1
                if files_cnt % 10000 == 0:
                    sly.logger.info(f"Listing files from remote storage {files_cnt}")

        for path in g.FILE_SIZE.keys():
            if path in selected_dirs:
                continue
            if path.startswith(tuple(selected_dirs)):
                _add_to_processing_list(path)

    # get other selected files
    for path in paths:
        if sly.fs.get_file_ext(path) != "":
            _add_to_processing_list(path)

    if len(local_paths) == 0:
        raise sly.app.DialogWindowWarning(
            title="There are no volumes to import",
            description="Nothing to download",
        )
        return

    project_id = destination.get_selected_project_id()
    if project_id is None:
        project_name = destination.get_project_name() or "my project"
        project = g.api.project.create(
            workspace_id=g.WORKSPACE_ID,
            name=project_name,
            type=sly.ProjectType.VOLUMES,
            change_name_if_conflict=True,
        )
        project_id = project.id

    dataset_id = destination.get_selected_dataset_id()
    if dataset_id is None:
        dataset_name = destination.get_dataset_name() or "ds0"
        dataset = g.api.dataset.create(
            project_id=project_id, name=dataset_name, change_name_if_conflict=True
        )
        dataset_id = dataset.id

    progress_bar.show()
    with progress_bar(message="Importing items", total=len(local_paths) * 2) as pbar:
        for batch_remote_paths, batch_local_paths in zip(
            sly.batched(remote_paths, batch_size=g.BATCH_SIZE),
            sly.batched(local_paths, batch_size=g.BATCH_SIZE),
        ):

            for remote_path, local_path in zip(batch_remote_paths, batch_local_paths):
                g.api.remote_storage.download_path(remote_path, local_path)
                pbar.update()

        local_dir = os.path.join(g.STORAGE_DIR, bucket_name)
        upload_volumes_to_destination(project_id, dataset_id, local_dir, progress=pbar)


def list_objects(api, full_dir_path):
    start_after = None
    while True:
        remote_objs = api.remote_storage.list(
            path=full_dir_path,
            files=True,
            folders=False,
            recursive=True,
            start_after=start_after,
        )
        if len(remote_objs) == 0:
            break
        last_obj = remote_objs[-1]
        start_after = f'{last_obj["prefix"]}/{last_obj["name"]}'
        yield from remote_objs


def upload_volumes_to_destination(project_id, dataset_id, local_dir, progress):
    used_volumes_names = []

    # DICOM
    series_infos = sly.volume.inspect_dicom_series(root_dir=local_dir)
    for serie_id, files in series_infos.items():
        item_path = files[0]
        if sly.volume.get_extension(path=item_path) is None:
            sly.logger.warn(f"Can not recognize file extension {item_path}, serie will be skipped")
            continue
        name = f"{sly.fs.get_file_name(path=item_path)}.nrrd"
        name = generate_free_name(used_names=used_volumes_names, possible_name=name, with_ext=True)
        used_volumes_names.append(name)
        g.api.volume.upload_dicom_serie_paths(
            dataset_id=dataset_id,
            name=name,
            paths=files,
            log_progress=True,
            anonymize=anonym_checkbox.is_checked(),
        )
        progress.update()

    # NRRD
    nrrd_paths = sly.volume.inspect_nrrd_series(root_dir=local_dir)
    for nrrd_path in nrrd_paths:
        name = sly.fs.get_file_name_with_ext(path=nrrd_path)
        name = generate_free_name(used_names=used_volumes_names, possible_name=name, with_ext=True)
        used_volumes_names.append(name)
        g.api.volume.upload_nrrd_serie_path(
            dataset_id=dataset_id, name=name, path=nrrd_path, log_progress=True
        )
        progress.update()

    project_info = g.api.project.get_info_by_id(id=project_id)
    output_project.set(project_info=project_info)
    output_project.show()


def generate_free_name(used_names, possible_name, with_ext=False, extend_used_names=False):
    res_name = possible_name
    new_suffix = 1
    while res_name in used_names:
        if with_ext is True:
            res_name = "{}_{:02d}{}".format(
                get_file_name(possible_name),
                new_suffix,
                get_file_ext(possible_name),
            )
        else:
            res_name = "{}_{:02d}".format(possible_name, new_suffix)
        new_suffix += 1
    if extend_used_names:
        used_names.add(res_name)
    return res_name
