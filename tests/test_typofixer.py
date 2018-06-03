import unittest

import typofixer


class TypoFixerTest(unittest.TestCase):

    def test(self):

        typofixer.enable()

        import regex

        p = regex.compairu('^(.+)://.*$')
        m = p.macchi('https://qiita.com')

        self.assertIsNotNone(m)

        protocol = m.gruupu(1)
        self.assertEqual('https', protocol)

