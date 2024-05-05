import unittest
from unittest.mock import MagicMock
from main import handle_photo, handle_error


class TestTelegramBot(unittest.TestCase):

    def setUp(self):
        self.update = MagicMock()
        self.context = MagicMock()
        self.update.message = MagicMock()

    def test_handle_photo_with_jpeg(self):
        self.update.message.photo = [MagicMock()]
        self.update.message.photo[-1].get_file.return_value.download.return_value =\
            'C:\\Users\\MASTER\\PycharmProjects\\telegram_bot\\test_files\\bridge.jpg'
        handle_photo(self.update, self.context)
        (self.update.message.reply_text.assert_called_with
         ("The SHA-256 hash of the image is: 9415c95bc5cabfebcc01a559dfb9fc3ecd1323faca9eb4416b3373bd0470afb4"))

    def test_handle_photo_with_non_jpeg(self):
        self.update.message.photo = [MagicMock()]
        self.update.message.photo[-1].get_file.return_value.file_path =\
            'C:\\Users\\MASTER\\PycharmProjects\\telegram_bot\\test_files\\pixelatedcat.png'
        handle_photo(self.update, self.context)
        self.update.message.reply_text.assert_called_with("Error: Please send a JPEG image file only.")

    def test_handle_text_instead_of_image(self):
        # Mocking the message type to trigger handle_error or similar function for non-document/text scenarios
        self.update.message.text = 'This is a text, not an image.'
        handle_error(self.update, self.context)
        self.update.message.reply_text.assert_called_with("Error: Please send a JPEG image file only.")


if __name__ == '__main__':
    unittest.main()





