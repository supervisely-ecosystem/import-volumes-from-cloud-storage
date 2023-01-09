<div align="center" markdown>
<img src="https://user-images.githubusercontent.com/48913536/211333857-d7f7a37d-5a71-456c-ab22-0f73a40cda4d.png"/>

# Import volumes from cloud storage

<p align="center">
  <a href="#Overview">Overview</a> •
  <a href="#How-To-Use">How To Use</a>
</p>


[![](https://img.shields.io/badge/supervisely-ecosystem-brightgreen)](https://ecosystem.supervise.ly/apps/supervisely-ecosystem/import-volumes-from-cloud-storage)
[![](https://img.shields.io/badge/slack-chat-green.svg?logo=slack)](https://supervise.ly/slack)
![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/supervisely-ecosystem/import-volumes-from-cloud-storage)
[![views](https://app.supervise.ly/img/badges/views/supervisely-ecosystem/import-volumes-from-cloud-storage.png)](https://supervise.ly)
[![runs](https://app.supervise.ly/img/badges/runs/supervisely-ecosystem/import-volumes-from-cloud-storage.png)](https://supervise.ly)

</div>

# Overview

This apps allows to import volumes from most popular cloud storage providers to Supervisely Private instance.

List of providers:
- Amazon s3
- Google Cloud Storage (CS)
- Microsoft Azure
- and others with s3 compatible interfaces

Files in `DICOM` format will be automatically converted to `NRRD` format during import.
App is compatible with `.DCM` and `.NRRD` formats, dicom files without `.dcm` extension are also compatible.

⚠️ Notice: for any of these import types app downloads video to its temp directory, processes it and extracts some 
technical information like timestamp-frame index mapping, number of streams, resolution and so on. Once the video is 
processed, it will be removed from temp directory. This is the one time procedure.

# How To Use

0. Ask your instance administrator to add cloud credentials to instance settings. It can be done both in .env
   configuration files or in Admin UI dashboard. Learn more in docs: [link1](https://docs.supervise.ly/enterprise-edition/installation/post-installation#configure-your-instance),
   [link2](https://docs.supervise.ly/enterprise-edition/advanced-tuning/s3#links-plugin-cloud-providers-support).
   In case of any questions or issues, please contact tech support.
1. Add app to your team from Ecosystem
2. Run app from `Ecosystem` Page
3. Connect to cloud bucket, preview and select files and directories, import selected files to some project/dataset.
   You can perform these actions as many times as needed
4. Once you are done with the app, you should close app manually

# Screenshot

<img src="https://user-images.githubusercontent.com/48913536/211333848-cabe2038-97bc-49d0-ad4e-827cc674a661.png"/>
