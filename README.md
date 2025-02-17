<div align="center" markdown>
<img src="https://user-images.githubusercontent.com/48913536/211368662-fe22dbe0-0542-4694-b1b9-8fdcb68216a4.png"/>

# Import volumes from cloud storage

<p align="center">
  <a href="#Overview">Overview</a> •
  <a href="#How-To-Use">How To Use</a>
</p>

[![](https://img.shields.io/badge/supervisely-ecosystem-brightgreen)](https://ecosystem.supervisely.com/apps/supervisely-ecosystem/import-volumes-from-cloud-storage)
[![](https://img.shields.io/badge/slack-chat-green.svg?logo=slack)](https://supervisely.com/slack)
![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/supervisely-ecosystem/import-volumes-from-cloud-storage)
[![views](https://app.supervisely.com/img/badges/views/supervisely-ecosystem/import-volumes-from-cloud-storage.png)](https://supervisely.com)
[![runs](https://app.supervisely.com/img/badges/runs/supervisely-ecosystem/import-volumes-from-cloud-storage.png)](https://supervisely.com)

</div>

# Overview

This apps allows to import volumes from most popular cloud storage providers to Supervisely Private instance.

List of providers:
- Amazon s3
- Google Cloud Storage (CS)
- Microsoft Azure
- and others with s3 compatible interfaces

Files in `DICOM` format will be automatically converted to `NRRD` format during import.
App is compatible with `.DCM` and `.NRRD` formats.

# How To Use

0. Ask your instance administrator to add cloud credentials to instance settings. It can be done both in .env
   configuration files or in Admin UI dashboard. Learn more in docs: [link1](https://docs.supervisely.com/enterprise-edition/installation/post-installation#configure-your-instance),
   [link2](https://docs.supervisely.com/enterprise-edition/advanced-tuning/s3#links-plugin-cloud-providers-support).
   In case of any questions or issues, please contact tech support.
1. Add app to your team from Ecosystem
2. Run app from `Ecosystem` Page
3. Connect to cloud bucket, preview and select files and directories, import selected files to some project/dataset.
   You can perform these actions as many times as needed
4. Once you are done with the app, you should close app manually

# Screenshot

<img src="https://user-images.githubusercontent.com/48913536/211368654-336c49cb-aa0d-4ee2-b9c7-65b783ab9c59.png"/>
