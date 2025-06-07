import os
from app import app, UPLOAD_FOLDER
from werkzeug.utils import secure_filename
from app.features import join_user_data, pdf_generator
from flask import render_template, request, flash, url_for, get_flashed_messages, redirect

@app.route("/", methods=["GET", "POST"])
def choose_template():
    available_templates = ["template1", "template2"]  

    if request.method == "POST":
        selected_template = request.form["template"]
        return redirect(url_for("form_page", template=selected_template))

    return render_template("choose_template.html", templates=available_templates)


@app.route('/form', methods=['GET', 'POST'])
def form_page():
    template = request.args.get('template', 'template1')

    if request.method == 'POST':
        username = request.form.get('username')
        csv_file = request.files.get('csv')

        if not username and (not csv_file or csv_file.filename == ''):
            print('[DEBUG] Nenhum username ou CSV enviado', flush=True)
            flash('To make a CV you need at least a GitHub username or a CSV file.')
            return redirect(url_for('form_page', template=template))

        try:
            csv_path = None
            if csv_file and csv_file.filename != '':
                filename = secure_filename(csv_file.filename)
                csv_path = os.path.join(UPLOAD_FOLDER, filename)
                csv_file.save(csv_path)

            user_data = join_user_data(csv_path=csv_path, github_username=username)
            pdf_generator(user_data, template=template)  

            flash('CV generated successfully!')
            return redirect(url_for('form_page', template=template))

        except Exception as e:
            flash(f'Error generating CV: {str(e)}')
            return redirect(url_for('form_page', template=template))

    return render_template('form.html', template_name=template)