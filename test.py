import unittest
from bunqclient import BunqClient

class TestBunqClient(unittest.TestCase):

	def test_prepare(self):
		bunq = BunqClient()
		self.assertEqual(bunq.prepare(user=1, monetary_account=20), 
			             "https://api.bunq.com/v1/user/1/monetary-account/20")
		self.assertEqual(bunq.prepare(user=1, monetary_account=""),
			             "https://api.bunq.com/v1/user/1/monetary-account")

	def test_request(self):
		bunq = BunqClient()
		self.assertEqual("", "")

	def test_init(self):
		bunq = BunqClient()
		self.assertEqual("", "")

	def test_sign(self):
		bunq = BunqClient()
		self.assertEqual("", "")

if __name__ == "__main__":
	unittest.main()
