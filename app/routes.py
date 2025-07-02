import os
import re
from weasyprint import HTML as WeasyHTML
from app import app, UPLOAD_FOLDER
from werkzeug.utils import secure_filename
from app.features import join_user_data
from flask import render_template, request, flash, url_for, get_flashed_messages, redirect, send_file

@app.route("/", methods=["GET", "POST"])
def choose_template():
    available_templates = ["template1", "template2", "template3"]  

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
            rendered_html = render_template(f"{template}.html", user=user_data)

            return render_template('editor.html', html_content=rendered_html, template=template)

        except Exception as e:
            flash(f'Error: {str(e)}')
            return redirect(url_for('form_page', template=template))

    return render_template('form.html', template_name=template)

@app.route('/generate_pdf', methods=['POST'])
def generate_pdf():
    edited_html = request.form['edited_html']
    template = request.form.get('template', 'template1')

    template_path = os.path.join(app.root_path, 'templates', f'{template}.html')
    css_content = ''
    if os.path.exists(template_path):
        with open(template_path, encoding='utf-8') as f:
            template_html = f.read()
            css_match = re.search(r'<style.*?>(.*?)</style>', template_html, re.DOTALL)
            if css_match:
                css_content = css_match.group(1)
    
    if css_content:
        edited_html = re.sub(r'<link[^>]*grapes[^>]*>', '', edited_html, flags=re.IGNORECASE)
        edited_html = re.sub(r'(<head.*?>)', r'\1\n<style>{}</style>'.format(css_content), edited_html, count=1, flags=re.DOTALL)

    try:
        root_dir = os.path.dirname(os.path.dirname(__file__))  
        output_dir = os.path.join(root_dir, "output")
        output_path = os.path.join(output_dir, 'cv_output.pdf')
        WeasyHTML(string=edited_html, base_url=app.root_path).write_pdf(output_path)

        return send_file(output_path, as_attachment=True)
    except Exception as e:
        flash(f'Erro ao gerar PDF: {e}')
        return redirect(url_for('form_page'))