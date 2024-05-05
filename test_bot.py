import unittest
from telegram import Bot


class TestTelegramBot(unittest.TestCase):
    def setUp(self):
        self.bot_token = '6992973033:AAFLnQjfwWPFYKEJaB85zHI8y4-3rHPz7Ew'
        self.bot = Bot(token=self.bot_token)
        self.chat_id = '-4274807511'

    def send_image_and_check_response(self, file_path, expected_response):
        with open(file_path, 'rb') as image:
            message = self.bot.send_photo(chat_id=self.chat_id, photo=image)
        updates = self.bot.get_updates(offset=message.message_id)
        if updates:
            response = updates[-1].message.text
            self.assertIn(expected_response, response)

    def test_send_jpeg_image(self):
        self.send_image_and_check_response(
            'C:\\Users\\MASTER\\PycharmProjects\\telegram_bot\\test_files\\bridge.jpg',
            'SHA-256 hash of the image is:')

    def test_send_text_instead_of_image(self):
        message = self.bot.send_message(chat_id=self.chat_id, text="This is a text message.")
        updates = self.bot.get_updates(offset=message.message_id)
        if updates:
            response = updates[-1].message.text
            self.assertIn("Error: Please send a JPEG image file only.", response)

    def test_send_non_jpeg_image(self):
        self.send_image_and_check_response(
            'C:\\Users\\MASTER\\PycharmProjects\\telegram_bot\\test_files\\pixelatedcat.png',
            "Error: Please send a JPEG image file only.")


if __name__ == '__main__':
    unittest.main()






