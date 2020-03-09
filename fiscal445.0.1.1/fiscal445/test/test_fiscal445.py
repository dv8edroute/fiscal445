import fiscal445 as fc5
import pandas as pd
import unittest
import datetime

# load csv to dataframe here for testing test_df

fc5.cal = fc5.set_445_cal('2020-02-02','sat')
fc5.current = '2020-03-07'
test_df = pd.read_excel('test/test_df.xlsx')

class TestFiscal445(unittest.TestCase):
    
    def test_check_dataframe(self):
        pd.testing.assert_frame_equal(fc5.cal, test_df)
        
    def test_week_of_month(self):
        self.assertEqual(fc5.week_of_month(),1)

    def test_cur_fiscal_week_of_year(self):
            self.assertEqual(fc5.cur_fiscal_week_of_year(),5) 
   
    def test_cur_fiscal_month(self):
        self.assertEqual(fc5.cur_fiscal_month(),'March')

    def test_month_to_date(self):
        self.assertEqual(fc5.month_to_date(),('2020-03-01', '2020-03-07'))
   
    def test_month_to_date_completed(self):
        self.assertEqual(fc5.month_to_date_completed(),('Not available yet!'))
        
    def test_year_to_date(self):
        self.assertEqual(fc5.year_to_date(),('2020-02-02', '2020-03-07'))
   
    def test_year_to_date_completed(self):
        self.assertEqual(fc5.year_to_date_completed(),('2020-02-02', '2020-02-29'))

    def test_quarter_completed(self):
        self.assertEqual(fc5.quarter_completed(1), ('2020-02-02', '2020-05-02'))
        self.assertEqual(fc5.quarter_completed(2), ('2020-05-03', '2020-08-01'))
        self.assertEqual(fc5.quarter_completed(3), ('2020-08-02', '2020-10-31'))
        self.assertEqual(fc5.quarter_completed(4), ('2020-11-01', '2021-01-30'))
        
    def test_quarter_completed_2(self):
        fc5.current = '2020-03-07'
        self.assertEqual(fc5.quarter_to_date(1), ('2020-02-02', '2020-03-07'))
        fc5.current = '2020-06-07'
        self.assertEqual(fc5.quarter_to_date(2), ('2020-05-03', '2020-06-07'))
        fc5.current = '2020-10-21'
        self.assertEqual(fc5.quarter_to_date(3), ('2020-08-02', '2020-10-21'))
        fc5.current = '2021-01-18'
        self.assertEqual(fc5.quarter_to_date(4), ('2020-11-01', '2021-01-18'))
        fc5.current = '2020-03-07'
    
    def test_quarter_completed(self):
        self.assertEqual(fc5.quarter_to_date(2), 'Quarter available yet!')   
        

if __name__ == '__main__':
    unittest.main()

