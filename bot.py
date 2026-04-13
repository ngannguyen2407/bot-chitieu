from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import os
import json
TOKEN = os.environ["8732865907:AAGpdEXIw3To_YBW3r-tEm2ZF8U3os02v3U"]

scope = ["https://spreadsheets.google.com/feeds",
         "https://www.googleapis.com/auth/drive"]
import os
import json
creds_dict = json.loads(os.environ["GOOGLE_CREDENTIALS"])
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)
client = gspread.authorize(creds)
sheet = client.open("CHI_TIEU").sheet1

categories = ["an_uong", "xang", "sinh_hoat", "kinh_doanh"]

def save_data(loai, tien, note, category):
    time = datetime.now().strftime("%d/%m/%Y %H:%M")
    sheet.append_row([time, loai, int(tien), note, category])

def get_data():
    return sheet.get_all_values()[1:]

# ================== BUTTON ==================

async def chon_loai(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = context.user_data
    category = query.data

    save_data(data["loai"], data["tien"], data["note"], category)

    await query.edit_message_text(f"Đã lưu {data['loai']} - {category}")

# ================== CHI ==================

async def chi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        tien = context.args[0]
        note = " ".join(context.args[1:])

        context.user_data["loai"] = "Chi"
        context.user_data["tien"] = tien
        context.user_data["note"] = note

        keyboard = [[InlineKeyboardButton(cat, callback_data=cat)] for cat in categories]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text("Chọn hạng mục:", reply_markup=reply_markup)

    except:
        await update.message.reply_text("Cú pháp: /chi 200000 ăn sáng")

# ================== THU ==================

async def thu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        tien = context.args[0]
        note = " ".join(context.args[1:])

        context.user_data["loai"] = "Thu"
        context.user_data["tien"] = tien
        context.user_data["note"] = note

        keyboard = [[InlineKeyboardButton(cat, callback_data=cat)] for cat in categories]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text("Chọn hạng mục:", reply_markup=reply_markup)

    except:
        await update.message.reply_text("Cú pháp: /thu 500000 lương")

# ================== TỔNG ==================

async def tong(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = get_data()
    thu = sum(int(r[2]) for r in data if r[1] == "Thu")
    chi = sum(int(r[2]) for r in data if r[1] == "Chi")
    await update.message.reply_text(f"Thu: {thu}\nChi: {chi}\nDư: {thu-chi}")

# ================== TỔNG THEO LOẠI ==================

async def tong_loai(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = get_data()
    result = {}

    for r in data:
        if r[1] == "Chi":
            cat = r[4]
            result[cat] = result.get(cat, 0) + int(r[2])

    msg = "\n".join([f"{k}: {v}" for k, v in result.items()])
    await update.message.reply_text(msg or "Chưa có dữ liệu")

# ================== THEO THÁNG ==================

async def thang(update: Update, context: ContextTypes.DEFAULT_TYPE):
    now = datetime.now().strftime("%m/%Y")
    data = get_data()

    thu = 0
    chi = 0

    for r in data:
        if now in r[0]:
            if r[1] == "Thu":
                thu += int(r[2])
            else:
                chi += int(r[2])

    await update.message.reply_text(f"Tháng {now}\nThu: {thu}\nChi: {chi}\nDư: {thu-chi}")

# ================== RUN ==================

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("thu", thu))
app.add_handler(CommandHandler("chi", chi))
app.add_handler(CommandHandler("tong", tong))
app.add_handler(CommandHandler("tong_loai", tong_loai))
app.add_handler(CommandHandler("thang", thang))
app.add_handler(CallbackQueryHandler(chon_loai))

app.run_polling()
import threading
from flask import Flask

app_web = Flask(__name__)

@app_web.route("/")
def home():
    return "Bot đang chạy!"

def run_web():
    app_web.run(host="0.0.0.0", port=10000)

# chạy web song song bot
threading.Thread(target=run_web).start()