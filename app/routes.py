import os
from app import app, UPLOAD_FOLDER
from werkzeug.utils import secure_filename
from app.features import join_user_data, pdf_generator
from flask import render_template, request, flash, url_for, get_flashed_messages, redirect

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form.get('username')
        csv_file = request.files.get('csv')

        if not username and not csv_file:
            flash('To make a CV you need at least a GitHub username or a CSV file.')
            return redirect(url_for('index'))

        try:
            if csv_file and csv_file.filename != '':
                filename = secure_filename(csv_file.filename)
                csv_path = os.path.join(UPLOAD_FOLDER, filename)
                csv_file.save(csv_path) 
            else:
                csv_path = None
            
            print("DEBUG:", username, csv_file)
            print("Is csv None?", csv_file is None)
            print("Is username empty?", not username)

        
            user_data = join_user_data(csv_path=csv_path, github_username=username)

            print(user_data.projects)
            print(type(user_data.projects))

            pdf_generator(user_data)

            flash('CV generated successfully!')
            return redirect(url_for('index'))

        except Exception as e:
            flash(f'Error generating CV: {str(e)}')
            return redirect(url_for('index'))

    return render_template('index.html')