from app.adapters.exceptions import ExternalError
from app.ports.otp_sender import OtpSender


class ConsoleOtpSender(OtpSender):
    """
    This class is an implementation of the OTP Sender interface to pretend to send an email
    but it just print the code in console
    """

    async def send(self, email: str, code: str) -> bool:
        try:
            print(f"code {code} has been sent to {email}")
            return True
        except Exception as e:
            raise ExternalError(e)
