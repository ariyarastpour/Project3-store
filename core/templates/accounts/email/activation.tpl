{% extends "mail_templated/base.tpl" %}

{% block subject %}
فعال‌سازی حساب کاربری
{% endblock %}

{% block html %}
<div style="font-family: Tahoma, sans-serif; direction: rtl; text-align: right;">
    <h2>سلام {{ email }} عزیز</h2>

    <p>از ثبت‌نام شما سپاسگزاریم. برای فعال‌سازی حساب کاربری روی لینک زیر کلیک کنید:</p>

    <p style="text-align: center; margin: 20px 0;">
        <a href="{{ link }}"
           style="background: #2563eb; color: white; padding: 12px 24px;
                  text-decoration: none; border-radius: 6px; display: inline-block;">
            فعال‌سازی حساب
        </a>
    </p>

    <hr style="margin: 20px 0; border: none; border-top: 1px solid #eee;">

    <p>یا کد زیر را در صفحه فعال‌سازی وارد کنید:</p>

    <p style="text-align: center; font-size: 32px; letter-spacing: 8px;
              font-weight: bold; color: #2563eb; direction: ltr;">
        {{ code }}
    </p>

    <p style="color: #888; font-size: 13px;">
        این لینک و کد تا {{ expires_hours|default:24 }} ساعت معتبر هستند.
    </p>

    <p style="color: #888; font-size: 13px;">
        اگر شما این درخواست را نداده‌اید، این ایمیل را نادیده بگیرید.
    </p>
</div>
{% endblock %}