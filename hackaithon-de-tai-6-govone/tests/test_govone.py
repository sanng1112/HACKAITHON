import os, sys, unittest
from docx import Document

SCRIPT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(SCRIPT_DIR, 'scripts'))

class TestGovOne(unittest.TestCase):
    def setUp(self):
        self.project_dir = SCRIPT_DIR
        self.assets_dir = os.path.join(self.project_dir, 'assets')

    def test_assets_directory_exists(self):
        self.assertTrue(os.path.isdir(self.assets_dir))

    def test_logo_generated(self):
        logo_path = os.path.join(self.assets_dir, 'logo-govone.png')
        self.assertTrue(os.path.isfile(logo_path))
        from PIL import Image
        img = Image.open(logo_path)
        self.assertEqual(img.size, (400, 400))
        self.assertEqual(img.mode, 'RGBA')

if __name__ == '__main__':
    unittest.main()
