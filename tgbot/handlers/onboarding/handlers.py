import datetime

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, ConversationHandler

from tgbot.models import Deposit, Expense
from tgbot.handlers.onboarding import keyboards
from tgbot.handlers.onboarding import static_text
from tgbot.models import User

DEPOSIT_QUESTION, DEPOSIT_PRICE, EXPENSE_QUESTION, EXPENSE_PRICE, REPORT, REPORT_TODAY, REPORT_TOTAL, DEPOSIT_DETAIL, \
DEPOSIT_DELETE_EDIT, DEPOSIT_EDIT, EXPENSE_DETAIL, EXPENSE_DELETE_EDIT, EXPENSE_EDIT = range(13)


def command_start(update: Update, context: CallbackContext):
    u, created = User.get_user_and_created(update, context)

    if created:
        text = static_text.start_created.format(first_name=u.first_name)
    else:
        text = static_text.start_not_created.format(first_name=u.first_name)

    update.message.reply_text(text=text,
                              reply_markup=keyboards.make_keyboard_for_start_command())
    return ConversationHandler.END


def deposit_comment_question(update: Update, context: CallbackContext):
    update.message.reply_text(text="Depozit manbasini kiriting: ")
    return DEPOSIT_QUESTION


def expense_comment_question(update: Update, context: CallbackContext):
    update.message.reply_text(text="Xarajat uchun izoh kiriting: ")
    return EXPENSE_QUESTION


def deposit_comment(update: Update, context: CallbackContext):
    comment = update.message.text
    Deposit.objects.create(comment=comment, user_id=update.message.chat_id)
    update.message.reply_text(text="Summani kiriting (UZS): ")

    return DEPOSIT_PRICE


def expense_comment(update: Update, context: CallbackContext):
    comment = update.message.text
    Expense.objects.create(comment=comment, user_id=update.message.chat_id)
    update.message.reply_text(text="Summani kiriting (UZS): ")
    return EXPENSE_PRICE


def deposit_price(update: Update, context: CallbackContext):
    price = update.message.text
    try:
        price = int(price)
    except ValueError:
        update.message.reply_text("Summa xato kiritildi! Iltimos, tekshirib, qaytadan kiriting:")
        update.message.reply_text(text="Summani kiriting (UZS): ")
        return DEPOSIT_PRICE
    deposit = Deposit.objects.filter(user_id=update.message.chat_id).last()
    deposit.price = price
    deposit.save()
    update.message.reply_text(text="Depozit saqlandi. Davom etamizmi?!",
                              reply_markup=keyboards.make_keyboard_for_start_command())


def expense_price(update: Update, context: CallbackContext):
    price = update.message.text
    try:
        price = float(price)
    except ValueError:
        update.message.reply_text("Summa xato kiritildi! Iltimos, tekshirib, qaytadan kiriting:")
        update.message.reply_text(text="Summani kiriting (UZS): ")
        return EXPENSE_PRICE

    expense = Expense.objects.filter(user_id=update.message.chat_id).last()
    expense.price = price
    expense.save()
    update.message.reply_text(text="Xarajat saqlandi. Davom etamizmi?!",
                              reply_markup=keyboards.make_keyboard_for_start_command())


def report_today(update: Update, context: CallbackContext):
    update.message.reply_text(text="Bo'limni tanlang:",
                              reply_markup=keyboards.make_keyboard_for_xisobot_command())
    return REPORT_TODAY


def report_total(update: Update, context: CallbackContext):
    update.message.reply_text(text="Bo'limni tanlang:",
                              reply_markup=keyboards.make_keyboard_for_xisobot_command())
    return REPORT_TOTAL


def deposit_report_total(update: Update, context: CallbackContext):
    deposits = Deposit.objects.filter(user_id=update.message.chat_id)
    price = 0
    keyboard = []
    n = 1
    text = "Umumiy depozitlar: \n\n"
    for deposit in deposits:
        if deposit.price != 0:
            text += f"{n}. {str(deposit.comment).capitalize()} - {deposit.price} so'm\n"
            price += deposit.price
            keyboard.append([InlineKeyboardButton(str(n), callback_data=deposit.id)])
            n += 1
    text += f"\n\nUmumiy summa: {price} so'm"
    if price == 0:
        text = 'Sizda depozitlar mavjud emas'
        update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))
        return REPORT_TOTAL
    update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))
    return DEPOSIT_DETAIL


def expense_report_total(update: Update, context: CallbackContext):
    expenses = Expense.objects.filter(user_id=update.message.chat_id)
    price = 0
    keyboard = []
    n = 1
    text = "Umumiy xarajatlar: \n\n"
    for expense in expenses:
        if expense.price != 0:
            text += f"{n}. {str(expense.comment).capitalize()} - {expense.price} so'm\n"
            price += expense.price
            keyboard.append([InlineKeyboardButton(str(n), callback_data=expense.id)])
    text += f"\n\nUmumiy summa: {price} so'm"
    if price == 0:
        text = "Sizda xarajatlar mavjud emas"
        update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))
        return REPORT_TOTAL
    update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))
    return EXPENSE_DETAIL


def deposit_report_today(update: Update, context: CallbackContext):
    deposits = Expense.objects.filter(user_id=update.message.chat_id, date=datetime.date.today())
    price = 0
    text = "Bugungi depozitlar: \n\n"
    for deposit in deposits:
        if deposit.price != 0:
            text += f"{str(deposit.comment).capitalize()} - {deposit.price} so'm |{deposit.created_at.time().strftime('%H:%M:%S')}\n"
            price += deposit.price

    text += f"\n\nUmumiy summa: {price} so'm"
    if price == 0:
        text = 'Sizda bugungi kun uchun depozitlar mavjud emas'
        update.message.reply_text(text)
        return REPORT_TODAY
    update.message.reply_text(text)


def expense_report_today(update: Update, context: CallbackContext):
    expenses = Expense.objects.filter(user_id=update.message.chat_id, date=datetime.date.today())
    price = 0
    text = "Bugungi xarajatlar: \n\n"
    for expense in expenses:
        if price != 0:
            text += f"{str(expense.comment).capitalize()} - {expense.price} so'm | {expense.created_at.time().strftime('%H:%M:%S')}\n"
            price += expense.price

    text += f"\n\nUmumiy summa: {price} so'm"
    if price == 0:
        text = 'Sizda bugungi kun uchun xarajatlar mavjud emas'
        update.message.reply_text(text)
        return REPORT_TODAY
    update.message.reply_text(text)


def back_to_main(update: Update, context: CallbackContext):
    update.message.reply_text(text="Hisob-kitob ishlarini davom ettiramizmi?",
                              reply_markup=keyboards.make_keyboard_for_start_command())


def report_choice(update: Update, context: CallbackContext):
    update.message.reply_text(text="Bo'limni tanlang:", reply_markup=keyboards.make_keyboard_for_xisobot_command2())
    return REPORT


def report_choice_today(update: Update, context: CallbackContext):
    update.message.reply_text(text="Bo'limni tanlang:", reply_markup=keyboards.make_keyboard_for_xisobot_command())


def report_choice_total(update: Update, context: CallbackContext):
    update.message.reply_text(text="Bo'limni tanlang:", reply_markup=keyboards.make_keyboard_for_xisobot_command())


def deposit_detail(update: Update, context: CallbackContext):
    query = update.callback_query
    deposit = Deposit.objects.get(id=query.data)
    text = f"Depozit manbasi: {str(deposit.comment).capitalize()}\nSumma: {deposit.price}\nDepozit vaqti: {deposit.created_at.date()} yil {deposit.created_at.time().strftime('%H:%M:%S')}"

    query.answer()
    print(text)
    query.edit_message_text(text)
    keyboard = [
        [InlineKeyboardButton("O'chirish", callback_data=f'delete-{query.data}')],
    ]
    query.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(keyboard))
    # context.bot.send_message(text=text, chat_id=update.effective_user.id)
    return DEPOSIT_DELETE_EDIT


def deposit_delete_edit(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    action = query.data.split("-")[0]
    id = query.data.split("-")[1]
    deposit = Deposit.objects.get(id=id)
    print(action)
    if action == "delete":
        print(1)
        deposit.delete()
        query.edit_message_text('Depozit muvaffaqiyatli o\'chirildi!')
        return REPORT_TOTAL
    return ConversationHandler.END


def expense_detail(update: Update, context: CallbackContext):
    query = update.callback_query
    expense = Expense.objects.get(id=query.data)
    text = f"Xarajat manbasi: {str(expense.comment).capitalize()}\nSumma: {expense.price}\nXarajat vaqti: {expense.created_at.date()} yil {expense.created_at.time().strftime('%H:%M:%S')}"

    query.answer()
    print(text)
    query.edit_message_text(text)
    keyboard = [
        [InlineKeyboardButton("O'chirish", callback_data=f'delete-{query.data}')]
    ]
    query.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(keyboard))
    # context.bot.send_message(text=text, chat_id=update.effective_user.id)
    return EXPENSE_DELETE_EDIT


def expense_delete_edit(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    action = query.data.split("-")[0]
    id = query.data.split("-")[1]
    expense = Expense.objects.get(id=id)
    print(action)
    if action == "delete":
        expense.delete()
        query.edit_message_text('Xarajat muvaffaqiyatli o\'chirildi!')
        return REPORT_TOTAL
    return ConversationHandler.END
