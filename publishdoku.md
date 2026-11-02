### 🚀 How to Publish a New Version

Follow these steps to package and release a new version of the **CopyStyle** QGIS plugin:

1. **Create the Archive**
   * Compress the main `CopyStyle` plugin folder into a ZIP archive named `CopyStyle_VX.y` (replace `X.y` with your current version number, e.g., `CopyStyle_V2.0`).

2. **Clean up and Finalize the ZIP Archive**
   * Open the newly created ZIP file using **7-Zip** (or any archive manager).
   * **Remove:** Delete the development helper script `CreateTranslate_QGIS 3.40.6.bat` from inside the ZIP file Fodler "CopyStyle".
   * **Add:** Ensure the official `LICENSE` file is included in the "CopyStyle" folder inside the ZIP file.

3. **Publish on GitHub**
   * Navigate to your GitHub repository and draft a new **Release**.
   * Fill in the version tag and release notes (e.g., *Changes in Version 2.0*).
   * Attach the clean `CopyStyle_VX.y.zip` file as a release asset.
   * Publish the release.
