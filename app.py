import os

from flask import Flask, render_template, request

from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField

from data_base import patient, study, \
    write_to_db, get_tags, current, \
    string_to_time, string_to_datetime

app = Flask(__name__)
app.secret_key = "randomstring"


class MyForm(FlaskForm):
    name = TextAreaField('Описание')
    submit = SubmitField()


@app.route('/')
def index_start():
    by_index = patient.sort_values(['id']).values
    return render_template('main.html', by_index=by_index, patient=patient, mode='hidden')


@app.route('/refresh')
def refresh_index():
    global patient
    global study
    # is there a new folders?
    table = study['dir'].unique()
    if len(table) == len(current()):
        pass
        new_dirs = []
    else:
        new_dirs = []
        for element in current():
            folder = element + '/'
            if folder not in table:
                new_dirs += [folder]
        # add element for patient
        for element in new_dirs:
            try:
                first_bin_file = [i for i in os.listdir(element) if i.endswith('.bin')][0]
                tag = get_tags(element + '/' + first_bin_file)
                tags = {
                    'id': tag[0], 'name': str(tag[1]), 'birth': string_to_time(tag[2]),
                    'study': string_to_time(tag[3]), 'report': '-', 'modality': tag[4]
                }
                if patient.loc[(patient.id == tags['id']) & (patient.study == tags['study'])].shape[0] == 0:
                    patient = patient.append(tags, ignore_index=True)
                else:
                    pass
            except:
                pass
            # add patient to study
            for el in ([i for i in os.listdir(element) if i.endswith('.bin')]):
                file_name = element + '/' + el
                try:
                    row = {'id': get_tags(file_name)[0], 'file': el, 'dir': element + '/'}
                    study = study.append(row, ignore_index=True)
                except:
                    row = {'id': 'Null', 'file': el, 'dir': element + '/'}
                    study = study.append(row, ignore_index=True)

    by_index = patient.sort_values(['id']).values

    return render_template('main.html', by_index=by_index, a=len(new_dirs), patient=patient)


@app.route('/sort/<how>')
def sorted_by(how):
    by_name = patient.sort_values(['name']).values
    by_modality = patient.sort_values(['modality']).values
    by_report = patient.sort_values(['report']).values
    by_index = patient.sort_values(['id']).values
    by_birth = patient.sort_values(['birth']).values
    by_study = patient.sort_values(['study']).values

    if how == 'by_name':
        return render_template('main.html', by_index=by_name, mode='hidden')
    elif how == 'by_modality':
        return render_template('main.html', by_index=by_modality, mode='hidden')
    elif how == 'by_index':
        return render_template('main.html', by_index=by_index, mode='hidden')
    elif how == 'by_birth':
        return render_template('main.html', by_index=by_birth, mode='hidden')
    elif how == 'by_study':
        return render_template('main.html', by_index=by_study, mode='hidden')
    else:
        return render_template('main.html', by_index=by_report, mode='hidden')


# add data
@app.route('/add_report/<id>/<study_date>/', methods=['GET', 'POST'])
def report(id, study_date):
    form = MyForm()
    form.name.data = list(patient.loc[(patient.id == id) & (patient.study == string_to_datetime(study_date))].report)[0]
    return render_template('report.html', form=form, id=id, study_date=study_date,
                           info=patient.loc[
                               (patient.id == id) & (patient.study == string_to_datetime(study_date))].values)


# add id and data
@app.route('/save/<id>/<study_date>/', methods=["GET", "POST"])
def render_save(id, study_date):
    form = MyForm()
    data = form.name.data
    for row in patient.loc[(patient.id == id) & (patient.study == string_to_datetime(study_date))].index:
        patient.loc[row, ['report']] = data
    if request.method == 'POST':
        by_index = patient.sort_values(['id']).values
        return render_template('main.html', by_index=by_index, patient=patient, mode='hidden')


app.run('127.0.0.1', 8000, debug=True)
