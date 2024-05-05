import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackContext, Filters
import hashlib

# Url to chat with the bot: https://t.me/qa_ha_bot


def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Send me a JPEG image(!! do not send as a compressed image !!)"
                              " and I'll calculate its hash.\n"
                              "Note: if you do send your image as a compressed image,"
                              " I will detect it as a jpg automatically even if its not. ")


def handle_photo(update: Update, context: CallbackContext) -> None:
    photo_file = update.message.photo[-1].get_file()
    photo_file_path = photo_file.file_path
    if photo_file_path.endswith('.jpg') or photo_file_path.endswith('.jpeg'):
        handle_image_file(photo_file, update)
    else:
        update.message.reply_text("Error: Please send a JPEG image file only.")


def handle_document(update: Update, context: CallbackContext) -> None:
    document = update.message.document
    if document.mime_type == 'image/jpeg':
        photo_file = document.get_file()
        handle_image_file(photo_file, update)


def handle_image_file(photo_file, update: Update) -> None:
    photo_path = photo_file.download()
    try:
        with open(photo_path, 'rb') as image_file:
            image_data = image_file.read()
            hash_result = hashlib.sha256(image_data).hexdigest()
            update.message.reply_text(f"The SHA-256 hash of the image is: {hash_result}")
    finally:
        # Ensure image is not one of the test images
        if "test_files" not in str(photo_path):
            os.remove(photo_path)
        pass


def handle_error(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Error: Please send a JPEG image file only.")


def main() -> None:
    updater = Updater("6992973033:AAFLnQjfwWPFYKEJaB85zHI8y4-3rHPz7Ew")

    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.photo, handle_photo))
    dispatcher.add_handler(MessageHandler(Filters.document.mime_type("image/jpeg"), handle_document))
    dispatcher.add_handler(
        MessageHandler(Filters.all & ~Filters.photo & ~Filters.document.mime_type("image/jpeg"), handle_error))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()

