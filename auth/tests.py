# from flask.ext.testing import TestCase
# from app import app, db
# import unittest
# from io import StringIO

# class MyTest(TestCase):
# 	def create_app(self):
# 		app.config.from_pyfile('testconfig.py')
# 		return app

# 	def setUp(self):
# 		db.create_all()

# 	def tearDown(self):
# 		db.session.remove();
# 		db.drop_all()

# 	def test_things(self):
# 		self.assertEqual(2, 2)

# def run():
# 	output = StringIO()
# 	suite = unittest.TestLoader().loadTestsFromTestCase(MyTest)
# 	unittest.TextTestRunner(verbosity=2, stream=output).run(suite)
# 	return output.getvalue()