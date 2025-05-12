import unittest
from unittest.mock import MagicMock, patch
from email.message import EmailMessage
from transcriber_service.infrastructure.services.email_service import EmailService


class TestEmailService(unittest.TestCase):
    def setUp(self):
        self.smtp_server = "smtp.example.com"
        self.smtp_port = 587
        self.sender_email = "sender@example.com"
        self.sender_password = "password123"
        self.service = EmailService(
            smtp_server=self.smtp_server,
            smtp_port=self.smtp_port,
            sender_email=self.sender_email,
            sender_password=self.sender_password,
        )

    def test_init(self):
        self.assertEqual(self.service.smtp_server, self.smtp_server)
        self.assertEqual(self.service.smtp_port, self.smtp_port)
        self.assertEqual(self.service.sender_email, self.sender_email)
        self.assertEqual(self.service.sender_password, self.sender_password)

    @patch("smtplib.SMTP")
    def test_send_recovery_email_port_587(self, mock_smtp):
        target_email = "recipient@example.com"
        temp_password = "TempPass123!"

        mock_server = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_server

        self.service.send_recovery_email(target_email, temp_password)

        mock_smtp.assert_called_once_with(self.smtp_server, self.smtp_port)
        mock_server.ehlo.assert_called_once()
        mock_server.starttls.assert_called_once()
        mock_server.login.assert_called_once_with(
            self.sender_email, self.sender_password
        )
        mock_server.send_message.assert_called_once()

        sent_message = mock_server.send_message.call_args[0][0]
        self.assertIsInstance(sent_message, EmailMessage)
        self.assertEqual(sent_message["Subject"], "Password Recovery")
        self.assertEqual(sent_message["From"], self.sender_email)
        self.assertEqual(sent_message["To"], target_email)
        self.assertIn(temp_password, sent_message.get_content())
        self.assertIn("Support Team", sent_message.get_content())
        self.assertIn(
            "Служба поддержки проекта Text Transcriber", sent_message.get_content()
        )

    @patch("smtplib.SMTP")
    def test_send_recovery_email_port_465(self, mock_smtp):
        self.service.smtp_port = 465
        target_email = "recipient@example.com"
        temp_password = "TempPass123!"

        mock_server = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_server

        self.service.send_recovery_email(target_email, temp_password)

        mock_smtp.assert_called_once_with(self.smtp_server, 465)
        mock_server.ehlo.assert_called_once()
        mock_server.starttls.assert_not_called()
        mock_server.login.assert_called_once_with(
            self.sender_email, self.sender_password
        )
        mock_server.send_message.assert_called_once()

    @patch("smtplib.SMTP")
    def test_send_recovery_email_smtp_error(self, mock_smtp):
        target_email = "recipient@example.com"
        temp_password = "TempPass123!"

        mock_server = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_server
        mock_server.login.side_effect = Exception("SMTP error")

        with self.assertRaises(Exception) as cm:
            self.service.send_recovery_email(target_email, temp_password)

        mock_smtp.assert_called_once_with(self.smtp_server, self.smtp_port)
        mock_server.ehlo.assert_called_once()
        mock_server.starttls.assert_called_once()
        mock_server.login.assert_called_once_with(
            self.sender_email, self.sender_password
        )
        self.assertEqual(str(cm.exception), "SMTP error")


if __name__ == "__main__":
    unittest.main()
