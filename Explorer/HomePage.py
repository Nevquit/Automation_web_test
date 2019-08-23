import unittest
from selenium import webdriver
import time
import HtmlTestRunner
from selenium.webdriver.common.keys import Keys
import sys

'''
from pyvirtualdisplay import Display  #for linux only
display = Display(visible=0, size=(800, 800)) #for linux only
display.start() #for linux only
'''
url = 'https://www.wanscan.org'
#url = sys.argv[1]

class HomePage(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(30)
        self.driver.maximize_window()
        try:
            #self.driver.get(url)
            self.driver.get(url)
        except Exception as e:
            print('The website can not be opened due to {}'.format(str(e)))
    def tearDown(self):
        self.driver.quit()

    def itemCheck(self,item,location_xpath,time_xpath):
        value = self.driver.find_element_by_xpath(location_xpath).text
        print('The {} number is : {}'.format(item,value))
        query_time = self.driver.find_element_by_xpath(time_xpath).text #example '5 secs ago'
        print('The {} query time is : {}'.format(item,query_time))
        time_check = query_time.split(' ')
        self.assertTrue(int(time_check[0]) < 60) #Failed if it's not updated more than 1 min
        self.assertIn(time_check[1],['sec','secs'])

    def top_items(self,module_name,items_name):
        items_value = list()
        items = self.driver.find_elements_by_css_selector(module_name)
        item_length = len(items)
        for member in items:
            items_value.append(member.find_element_by_css_selector(items_name).text)
        return item_length,items_value

    def test_01_blk_vld(self):
        '''Check basic block and validator information'''
        time.sleep(3)
        #1.Check the block update time
        self.itemCheck('block',location_xpath='/html/body/div[2]/div/div/div[1]/div[2]/span',time_xpath='/html/body/div[2]/div/div/div[1]/div[1]/span[2]')
        #2.Check the validators update time
        self.itemCheck('Validator',location_xpath='/html/body/div[2]/div/div/div[2]/div[2]/span',time_xpath='/html/body/div[2]/div/div/div[2]/div[1]/span[2]')

    def test_02_Top_10_vlds(self):
        '''Check top 10 list'''
        item_length,TopVldNames = self.top_items('div.validatorTable_tr','a.validatorName')
        print('The Top10 validators are {}'.format(TopVldNames))
        self.assertEqual(item_length,10)

    def test_03_Statistics_Chart(self):
        '''Check the Statistics Chart which should be visible'''
        name = self.driver.find_element_by_xpath('//*[@id="EarningCurve"]/div[1]/span').text
        chart_picture = self.driver.find_element_by_xpath('//*[@id="myChart"]/div[1]/canvas')
        self.assertTrue(chart_picture)
        self.assertTrue(name)
        self.driver.save_screenshot(name+'.png')

    def test_04_Latest_Transactions(self):
        '''Check the latest tranactions'''
        item_length, transactions = self.top_items('div.latestTransTable_item', 'span.trHashText')
        print('The latest transactions are {}'.format(transactions))
        self.assertEqual(item_length,3)

    def test_05_Latest_blocks(self):
        '''Check the latest blocks'''
        item_length, block_times = self.top_items('div.blockTable_item', 'span.fromNow')
        print('The latest {} blocks generation time are {}'.format(item_length,block_times))
        self.assertEqual(item_length,5,'It always display 5 blocks before ......')




if __name__ == '__main__':
    #unittest.main
    suite = unittest.TestSuite()
    suite.addTest(HomePage('test_01_blk_vld'))
    suite.addTest(HomePage('test_02_Top_10_vlds'))
    suite.addTest(HomePage('test_03_Statistics_Chart'))
    suite.addTest(HomePage('test_04_Latest_Transactions'))
    suite.addTest(HomePage('test_05_Latest_blocks'))
    runner = HtmlTestRunner.HTMLTestRunner(report_title='Test_Report',descriptions='iWAN website regression test',verbosity=3,report_name='explorer_homepage')
    runner.run(suite)