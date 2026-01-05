"""
Fake implementation class of the OtpSender Interface to use in unit tests
"""

from app.ports.otp_sender import OtpSender


class FakeOtpSender(OtpSender):
    def __init__(self):
        self.sent = []

    async def send(self, email: str, code: str) -> None:
        self.sent.append((email, code))
