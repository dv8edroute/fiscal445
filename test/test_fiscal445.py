import fiscal445 as fc5
import unittest
import datetime

class TestFiscal445(unittest.TestCase):
    
    def test_month_lookup(self):
        self.assertEquals(fc5.month_lookup(10),'March')
        self.assertEquals(fc5.month_lookup(10,3),'Mar')
        
    def test_week_lookup(self):
        self.assertEquals(fc5.week_lookup(9),'Wk1')
        self.assertEquals(fc5.week_lookup(10),'Wk2')
        self.assertEquals(fc5.week_lookup(11),'Wk3')
        self.assertEquals(fc5.week_lookup(12),'Wk4')
        self.assertEquals(fc5.week_lookup(13),'Wk5')
    
    def test_week_current(self):
        current = datetime.datetime.now().isocalendar()[1]
        self.assertEquals(fc5.week_current(),current)
        


if __name__ == '__main__':
    unittest.main()

