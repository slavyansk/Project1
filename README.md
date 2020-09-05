# DICOM_reporter
flask-based app to create database from dicom images in folder and write medical reports


1.config.py - set folder (path), to which images will be sent.

2 initialise() and write_to_db() defs create DataFrame based database according DICOM-tags of all ".bin" files in path.

3. refresh burtton in main.html add new patient ino dataframe

4. App support main table sorting by all columns (study date, birth date, modality, exist report or not exist, id, patient name)

5. by default all reports create with empty field. App support create and save into dataframe report text field, whuch can be edited.

status of project: MVP/demo

in next step:
auto add .rtf reports instead empty field, if .rtf report exists
expansion to .dicom files
add postgresql-based database
search by all tags
add DICOM_viewer
