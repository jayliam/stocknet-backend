###############################################################################
#
# Tests for XlsxWriter.
#
# Copyright (c), 2013-2020, John McNamara, jmcnamara@cpan.org
#

from ..excel_comparison_test import ExcelComparisonTest
from ...workbook import Workbook


class TestCompareXLSXFiles(ExcelComparisonTest):
    """
    Test file created by XlsxWriter against a file created by Excel.

    """

    def setUp(self):

        self.set_filename('comment02.xlsx')

    def test_create_file(self):
        """Test the creation of a simple XlsxWriter file with comments."""

        workbook = Workbook(self.got_filename)

        worksheet = workbook.add_worksheet()

        worksheet.write('A1', 'Foo')
        worksheet.write_comment('B2', 'Some text')
        worksheet.write_comment('D17', 'More text')

        # Set the author to match the target XLSX file.
        worksheet.set_comments_author('John')

        workbook.close()

        self.assertExcelEqual()
