import os
import io
import json
import requests
import uuid
from flask import (
    Flask, flash, render_template, request, redirect,
    url_for, jsonify, send_from_directory, make_response
)
from werkzeug.utils import secure_filename
import pandas as pd
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'json'}

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# اطمینان از وجود پوشه آپلود
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# بررسی فرمت فایل مجاز


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# دریافت لیست فایل‌های آپلود شده


def get_uploaded_files():
    return sorted(
        [f for f in os.listdir(UPLOAD_FOLDER) if allowed_file(f)],
        key=lambda x: os.path.getmtime(os.path.join(UPLOAD_FOLDER, x))
    )

# صفحه اصلی: لیست فایل‌ها


@app.route('/')
def index():
    files = get_uploaded_files()
    return render_template('index.html', files=files)

# نمایش جدول از آخرین فایل آپلود شده


@app.route('/table/<filename>')
def table_view(filename):
    files = get_uploaded_files()
    if not files:
        flash("هیچ فایلی یافت نشد.")
        return redirect(url_for('index'))

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            raw_data = json.load(f)

        # تبدیل به لیست اگر ساختار دیکشنری باشد
        if isinstance(raw_data, dict):
            data_list = [raw_data]
        elif isinstance(raw_data, list):
            data_list = raw_data
        else:
            data_list = []

        # استخراج هدرهای داینامیک با حفظ ترتیب
        headers = []
        seen = set()
        for item in data_list:
            if isinstance(item, dict):
                for key in item.keys():
                    if key not in seen:
                        headers.append(key)
                        seen.add(key)

        # تولید رشته JSON فرمت‌شده برای هر ردیف
        pretty_json_list = [json.dumps(
            item, ensure_ascii=False, indent=2) for item in data_list]

        return render_template(
            'table.html',
            data=data_list,
            headers=headers,
            pretty_json_list=pretty_json_list,
            uploaded_files=files
        )

    except Exception as e:
        return render_template('table.html', error=f"خطا در پردازش فایل: {str(e)}")

# آپلود فایل از URL


@app.route('/upload_url', methods=['POST'])
def upload_url():
    url = request.form.get('url')
    if not url:
        flash("آدرس URL معتبر نیست.")
        return redirect(url_for('index'))   

    try:
        response = requests.get(url)
        response.raise_for_status()
        raw_data = response.json()

        # اطمینان از اینکه داده‌ها لیست هستند
        if isinstance(raw_data, dict):
            data = [raw_data]
        elif isinstance(raw_data, list):
            data = raw_data
        else:
            data = []

        # ذخیره فایل به صورت لیستی
        filename = secure_filename(f"url_{uuid.uuid4().hex}.json")
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        flash("لینک با موفقیت آپلود شد.")
        return redirect(url_for('table_view', filename=filename))
    except Exception as e:
        flash(f"خطا در دریافت فایل از URL: {e}")

    return redirect(url_for('index'))

# آپلود فایل محلی


@app.route('/upload_file', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash("هیچ فایلی انتخاب نشده است.")
        return redirect(url_for('index'))

    file = request.files['file']

    if file and allowed_file(file.filename):
        filename = secure_filename(f"upload_{uuid.uuid4().hex}.json")
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        flash("فایل با موفقیت آپلود شد.")
        return redirect(url_for('table_view', filename=filename))

    else:
        flash("فرمت فایل مجاز نیست.")

    return redirect(url_for('index'))

# مشاهده محتوای فایل به صورت فرمت‌شده


@app.route('/view/<filename>')
def view_file(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        content = json.dumps(data, ensure_ascii=False, indent=2)
        return render_template('view.html', filename=filename, content=content)
    except Exception as e:
        return f"خطا در خواندن فایل: {e}"

# API برای دریافت داده JSON (برای DataTables)


@app.route('/data/<filename>')
def get_data(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        if isinstance(data, dict):
            data = [data]
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# حذف فایل


@app.route('/delete/<filename>', methods=['POST'])
def delete_file(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(filepath):
        os.remove(filepath)
        flash("فایل با موفقیت حذف شد.")
    else:
        flash("فایل یافت نشد.")
    return redirect(url_for('index'))

# ارائه فایل برای دانلود


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


# خروجی اکسل
@app.route('/export_excel/<filename>')
def export_excel(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        if isinstance(data, dict):
            data = [data]

        df = pd.json_normalize(data)

        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False)
        output.seek(0)

        response = make_response(output.read())
        response.headers['Content-Disposition'] = f'attachment; filename={filename}.xlsx'
        response.headers['Content-Type'] = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        return response

    except Exception as e:
        flash(f"خطا در تولید فایل اکسل: {e}")
        return redirect(url_for('index'))


# صفحه چاپ ساده (نمایش محتویات JSON با استایل قابل چاپ)
@app.route('/print_view/<filename>')
def print_view(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        content = json.dumps(data, ensure_ascii=False, indent=2)
        return render_template('print_view.html', filename=filename, content=content)
    except Exception as e:
        flash(f"خطا در بارگذاری صفحه چاپ: {e}")
        return redirect(url_for('index'))


# اجرای برنامه
if __name__ == '__main__':
    app.run(debug=True)
