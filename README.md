# V2Ray Telegram Subscription Generator 🚀

یک سیستم خودکار برای دریافت و ساخت **لینک سابسکریپشن V2Ray** از کانال تلگرام `@NamazVPN` بدون نیاز به کپی دستی کانفیگ‌ها.

## 🔗 لینک‌های سابسکریپشن فعال شما

پس از قرار گرفتن این ریپازیتوری در گیت‌هاب، لینک سابسکریپشن خودکار شما این خواهد بود:

- **لینک اصلی (Base64 استاندارد برای v2rayNG / v2rayN / Shadowrocket / Sing-box):**
  ```text
  https://raw.githubusercontent.com/ArashRepo/worker/main/sub.txt
  ```

- **لینک متنی (Plain Text):**
  ```text
  https://raw.githubusercontent.com/ArashRepo/worker/main/sub_raw.txt
  ```

---

## ⚡ امکانات

1. **بروزرسانی خودکار ساعت به ساعت (GitHub Actions):** بدون نیاز به سرور یا روشن بودن سیستم، گیت‌هاب هر ۱ ساعت کانال را بررسی کرده و فایل `sub.txt` را آپدیت می‌کند.
2. **کد Cloudflare Worker آماده (`worker.js`):** در صورت تمایل می‌توانید کدهای این فایل را در کلودفلیر بنشانید.
3. **سرور محلی پایتون (`server.py`):** برای تست و اجرای محلی روی سیستم خودتان.

---

## 📲 نحوه استفاده در نرم‌افزارها

### v2rayNG (موبایل اندروید)
1. منوی سمت چپ ➔ **Subscription group**
2. علامت `+` بالا ➔ وارد کردن نام `NamazVPN` و لینک سابسکریپشن `https://raw.githubusercontent.com/ArashRepo/worker/main/sub.txt`
3. ذخیره ➔ سه نقطه بالا ➔ **Update subscription**

### v2rayN (ویندوز)
1. منوی **Subscription setting** ➔ افزودن (Add)
2. وارد کردن نام و URL بالا
3. منوی **Subscription update** ➔ **Update subscription without proxy**

---

## 🛠 تنظیمات GitHub Actions

برای اینکه گیت‌هاب بتواند فایل‌های سابسکریپشن را به صورت خودکار تغییر دهد:
1. در ریپازیتوری خود به مسیر **Settings ➔ Actions ➔ General** بروید.
2. در بخش **Workflow permissions** گزینه **Read and write permissions** را تیک بزنید و **Save** کنید.
