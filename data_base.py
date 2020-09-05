import datetime
import os
import pandas as pd
import pydicom as pyd

from config import path


def string_to_datetime(string):
    b = string.split("-")
    return datetime.date(int(b[0]), int(b[1]), int(b[2]))


def initialise():
    global patient
    global study
    patient = pd.DataFrame()
    study = pd.DataFrame()


def is_base_clean():
    if 'patient' not in locals() and 'studies' not in locals():
        initialise()
        write_to_db(current())
    else:
        pass


def get_tags(image):
    image = pyd.dcmread(image, stop_before_pixels=True)
    return [image.PatientID, image.PatientName, image.PatientBirthDate, image.StudyDate, image.Modality]


def current():
    return [path + i for i in os.listdir(path) if os.path.isdir(path + i) == True]


def string_to_time(string):
    return pd.to_datetime(string, format='%Y%m%d', errors='ignore').date()


def write_to_db(this_dir):
    global patient
    global study
    for element in this_dir:
        try:
            first_bin_file = [i for i in os.listdir(element) if i.endswith('.bin')][0]

            tag = get_tags(element + '/' + first_bin_file)
            tags = {
                'id': tag[0], 'name': str(tag[1]), 'birth': string_to_time(tag[2]),
                'study': string_to_time(tag[3]), 'report': '-', 'modality': tag[4]
            }
            patient = patient.append(tags, ignore_index=True)
        except:
            pass
        for el in ([i for i in os.listdir(element) if i.endswith('.bin')]):
            file_name = element + '/' + el
            try:
                row = {'id': get_tags(file_name)[0], 'file': el, 'dir': element + '/'}
                study = study.append(row, ignore_index=True)
            except:
                row = {'id': 'Null', 'file': el, 'dir': element + '/'}
                study = study.append(row, ignore_index=True)

global patient
global study

initialise()
write_to_db(current())
