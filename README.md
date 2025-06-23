
# مدیریت فایل‌های JSON با Flask | JSON File Manager with Flask

ساخته شده توسط: علیرضا لباف (Alireza Labbaf)  
پروژه‌ای برای مدیریت فایل‌های JSON   با امکاناتی مثل آپلود، نمایش، دانلود، حذف و تبدیل به اکسل و نمایش به صورت جدولی.

Built by: Alireza Labbaf  
A project for managing JSON files with features like upload, view, download, delete, and export to Excel and show as table.

---

## ✨ ویژگی‌ها | Features

- ✅ آپلود فایل JSON از سیستم
- 🌐 بارگذاری فایل JSON از URL خارجی
- 📊 نمایش فایل به صورت جدول (DataTables)
- 🧾 نمایش ساختار JSON به صورت فرمت‌شده
- 🗑️ حذف فایل
- 📥 دانلود فایل JSON و خروجی Excel
- 🖨️ صفحه چاپ از فایل JSON

---

## ⚙️ پیش‌نیازها | Requirements

- Python 3.8 یا بالاتر  
- نصب کتابخانه‌های زیر (در فایل `requirements.txt` قرار دهید):  
  ```
  Flask
  requests
  pandas
  openpyxl
  ```

---

## 🖥️ راه‌اندازی در ویندوز | Windows Setup Guide

### 1. نصب Python

ابتدا مطمئن شوید Python روی سیستم شما نصب است.  
دانلود از [python.org](https://www.python.org/downloads/)

هنگام نصب، تیک **Add Python to PATH** را فعال کنید.

---

### 2. کلون کردن پروژه

```bash
git clone https://github.com/alirezalabbaf/json-flask-manager.git
cd json-flask-manager
```

یا فایل پروژه را به صورت ZIP دانلود و استخراج کنید.

---

### 3. ساخت محیط مجازی (Virtual Environment)

```bash
python -m venv venv
venv\Scripts\activate
```

---

### 4. نصب کتابخانه‌ها

```bash
pip install -r requirements.txt
```

---

### 5. اجرای پروژه

```bash
python app.py
```

---

### 6. ورود به برنامه

مرورگر را باز کرده و وارد آدرس زیر شوید:

```
http://127.0.0.1:5000/
```

---

## 🗂️ ساختار پروژه | Project Structure

```
/uploads           # ذخیره‌ فایل‌های آپلود شده
/templates         # فایل‌های HTML
app.py             # فایل اصلی Flask
requirements.txt   # لیست پکیج‌ها
README.md          # توضیحات پروژه
```

---

## 📜 مجوز | License

این پروژه تحت مجوز MIT منتشر شده است — استفاده آزاد با ذکر منبع.

---

## 📩 ارتباط با من | Contact Me

- GitHub: [github.com/alirezalabbaf](https://github.com/alirezalabbaf)
- ایمیل: [alirezalabbaf.dev@gmail.com](mailto:alirezalabbaf.dev@gmail.com)

---

> ❤️ ممنون از استفاده شما از این پروژه!  
> 💡 Pull Request و Issueهای شما باعث بهبود پروژه می‌شود.
