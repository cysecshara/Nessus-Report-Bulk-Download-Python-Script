# Nessus Scan Report Automation (Python)

## Author
cysecshara

## Overview

This project automates the export and download of vulnerability scan reports from Nessus using the Nessus REST API.

Instead of manually exporting reports from the Nessus UI, the scripts allow security engineers to download scan reports in bulk.

## Features

- Bulk export of Nessus scan reports
- Folder-based scan retrieval
- Automatic report download
- CSV export support
- API-based automation

## Use Case

During vulnerability assessment and security audits, organizations may have hundreds of scans across multiple folders. Manually downloading reports is time consuming.

This project automates the process using Python and the Nessus API.

## Scripts

### 1. Bulk Scan Export
Exports reports for all completed scans.
Nessus-allfileswithoutfolder.py

### 2. Multiple Folder-Based Export
Exports scans only from selected folders.
Nessus-folderwiseallfilesmethod.py


### 3. One Specific-Folder Export
Downloads exported scan reports automatically.
Nessus-targetfolderonly.py
