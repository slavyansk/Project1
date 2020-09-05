#             Flask-based app for creating medical reports


![2](https://user-images.githubusercontent.com/44552657/92303352-30ab5100-ef74-11ea-982e-f1e062c72c0c.png)

1. config.py - set folder (path), to which images will be sent.

2. initialise() and write_to_db() defs create DataFrame based database according DICOM-tags of all ".bin" files in path.

3. refresh burtton in main.html add new patient ino dataframe.

4. App support main table sorting by all columns (study date, birth date, modality, exist report or not exist, id, patient name).

5. by default all reports create with empty field. App support create and save into dataframe report text field, whuch can be edited.


![1](https://user-images.githubusercontent.com/44552657/92303350-2f7a2400-ef74-11ea-96fa-d477270593e5.png)


status of project: MVP/demo

in next step:
1. reformat code, replace all globals by classes
2. auto add .rtf reports instead empty field, if .rtf report exists
3. expansion to .dicom files not only .bin
4. add postgresql-based database
5. search by all tags
6. add DICOM_viewer
