import json
import os
import sys
import base64

from flask import Flask, render_template, abort, redirect, url_for

app = Flask(__name__)
ground_truth = {}
source_file_handler = None
label_file_handler = None

@app.route('/id/<pair_id>/label/<label>')
def label(pair_id, label):
    pair_id = (base64.urlsafe_b64decode(pair_id.encode('utf-8'))).decode('utf-8')

    if pair_id in ground_truth:
        return abort(400, 'Already labeled.')
    label = label.lower().strip()
    if label not in ('yes', 'no', 'not_sure'):
        return abort(400, 'Wrong label')

    # write to file first, then update memory
    label_file_handler.write(json.dumps({'id': pair_id, 'label': label}) + '\n')
    label_file_handler.flush()
    ground_truth[pair_id] = label
    return redirect(url_for('index'))

@app.route('/')
def index():
    if not source_file_handler:
        return abort(500, 'Missing source file handler.')

    for line in source_file_handler:
        obj = json.loads(line)
        # already labeled
        if obj['id'] in ground_truth:
            continue

        # construct label page
        context = {
            'title': 'GAIA TA2 Labeler',
            'id': obj['id'],
            'url_id': base64.urlsafe_b64encode(obj['id'].encode('utf-8')).decode('utf-8'),
            'r1': obj['r1'],
            'r2': obj['r2']
        }

        return render_template('index.html', **context)

    return 'Congrats, no more candidate pairs to label!'


if __name__ == '__main__':
    source_file, label_file = sys.argv[1], sys.argv[2]

    # create if label file doesn't exist
    if not os.path.exists(label_file):
        with open(label_file, 'w'):
            pass

    # load ground truth into memory
    with open(label_file, 'r') as label_file_handler:
        for line in label_file_handler:
            obj = json.loads(line)
            ground_truth[obj['id']] = obj['label']

    try:
        source_file_handler = open(source_file ,'r')
        label_file_handler = open(label_file, 'a')

        app.run('0.0.0.0', port=5999, debug=True)
    except:
        source_file_handler.close()
        label_file_handler.close()
    