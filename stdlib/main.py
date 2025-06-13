from subprocess import *
import time
from random import randint
from apscheduler.schedulers.blocking import BlockingScheduler
import sender
import email
import imaplib
import ctypes
import datetime
import time
import logging
import os
today = datetime.datetime.now()
ctypes.windll.kernel32.SetConsoleTitleW("RRR Main")

def logger(script_name):
    """This Function is used to Setup logging"""
    path=f"BACKUP//{script_name}//" #Check path exist
    if not os.path.exists(path):os.makedirs(path)
    LOG_FILENAME = path + '{}'.format(script_name,) + today.strftime('%H_%M_%S_%d_%m_%Y.log')
    logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG,  format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger().addHandler(logging.StreamHandler())
    logging.getLogger("PIL.PngImagePlugin").setLevel(logging.WARNING)
logger('CaptchaMain')  
  
logging.info(today)
def cron_process1():
    p = Popen('python captchaharvest.py')
    logging.info('process 1 is running............................')
    time.sleep(1500)
    p=p.terminate()

def cron_process2():
    p = Popen('python captchaharvest.py')
    logging.info('process 2 is running.............................')
    time.sleep(1500)
    p=p.terminate()

def cron_process3():
    p = Popen('python captchaharvest.py')
    logging.info('process 3 is running............................')
    time.sleep(1500)
    p=p.terminate()

def cron_process4():
    p = Popen('python captchaharvest.py')
    logging.info('process 4 is running............................')
    time.sleep(1500)
    p=p.terminate()

def cron_process5():
    p = Popen('python captchaharvest.py')
    logging.info('process 5 is running............................')
    time.sleep(1500)
    p=p.terminate()

def cron_process6():
    p = Popen('python captchaharvest.py')
    logging.info('process 6 is running.............................')
    time.sleep(1500)
    p=p.terminate()
  
def cron_process7():
    p = Popen('python captchaharvest.py')
    logging.info('process 7 is running............................')
    time.sleep(1500)
    p=p.terminate()
  
def cron_process8():
    p = Popen('python captchaharvest.py')
    logging.info('process 8 is running.............................')
    time.sleep(1500)
    p=p.terminate()

def cron_process9():
    p = Popen('python captchaharvest.py')
    logging.info('process 9 is running............................')
    time.sleep(1500)
    p=p.terminate()

def cron_process10():
    p = Popen('python captchaharvest.py')
    logging.info('process 10 is running.............................')
    time.sleep(1500)
    p=p.terminate()
                            
scheduler = BlockingScheduler()

scheduler.add_job(cron_process1, 'cron', day_of_week = 'mon-sun', hour='08', minute='29', second='00')
scheduler.add_job(cron_process2, 'cron', day_of_week = 'mon-sun', hour='08', minute='29', second='05')
scheduler.add_job(cron_process3, 'cron', day_of_week = 'mon-sun', hour='08', minute='29', second='10')
scheduler.add_job(cron_process4, 'cron', day_of_week = 'mon-sun', hour='08', minute='29', second='15')
scheduler.add_job(cron_process5, 'cron', day_of_week = 'mon-sun', hour='08', minute='29', second='20')
scheduler.add_job(cron_process6, 'cron', day_of_week = 'mon-sun', hour='08', minute='29', second='25')
scheduler.add_job(cron_process7, 'cron', day_of_week = 'mon-sun', hour='08', minute='29', second='30')
scheduler.add_job(cron_process8, 'cron', day_of_week = 'mon-sun', hour='08', minute='29', second='40')
scheduler.add_job(cron_process9, 'cron', day_of_week = 'mon-sun', hour='08', minute='29', second='45')
scheduler.add_job(cron_process10, 'cron', day_of_week = 'mon-sun', hour='08', minute='29', second='50')

scheduler.add_job(cron_process1, 'cron', day_of_week = 'mon-sun', hour='09', minute='29', second='00')
scheduler.add_job(cron_process2, 'cron', day_of_week = 'mon-sun', hour='09', minute='29', second='05')
scheduler.add_job(cron_process3, 'cron', day_of_week = 'mon-sun', hour='09', minute='29', second='10')
scheduler.add_job(cron_process4, 'cron', day_of_week = 'mon-sun', hour='09', minute='29', second='15')
scheduler.add_job(cron_process5, 'cron', day_of_week = 'mon-sun', hour='09', minute='29', second='20')
scheduler.add_job(cron_process6, 'cron', day_of_week = 'mon-sun', hour='09', minute='29', second='25')
scheduler.add_job(cron_process7, 'cron', day_of_week = 'mon-sun', hour='09', minute='29', second='30')
scheduler.add_job(cron_process8, 'cron', day_of_week = 'mon-sun', hour='09', minute='29', second='40')
scheduler.add_job(cron_process9, 'cron', day_of_week = 'mon-sun', hour='09', minute='29', second='45')
scheduler.add_job(cron_process10, 'cron', day_of_week = 'mon-sun', hour='09', minute='29', second='50')

scheduler.add_job(cron_process1, 'cron', day_of_week = 'mon-sun', hour='10', minute='29', second='00')
scheduler.add_job(cron_process2, 'cron', day_of_week = 'mon-sun', hour='10', minute='29', second='05')
scheduler.add_job(cron_process3, 'cron', day_of_week = 'mon-sun', hour='10', minute='29', second='10')
scheduler.add_job(cron_process4, 'cron', day_of_week = 'mon-sun', hour='10', minute='29', second='15')
scheduler.add_job(cron_process5, 'cron', day_of_week = 'mon-sun', hour='10', minute='29', second='20')
scheduler.add_job(cron_process6, 'cron', day_of_week = 'mon-sun', hour='10', minute='29', second='25')
scheduler.add_job(cron_process7, 'cron', day_of_week = 'mon-sun', hour='10', minute='29', second='30')
scheduler.add_job(cron_process8, 'cron', day_of_week = 'mon-sun', hour='10', minute='29', second='40')
scheduler.add_job(cron_process9, 'cron', day_of_week = 'mon-sun', hour='10', minute='29', second='45')
scheduler.add_job(cron_process10, 'cron', day_of_week = 'mon-sun', hour='10', minute='29', second='50')

scheduler.add_job(cron_process1, 'cron', day_of_week = 'mon-sun', hour='11', minute='29', second='00')
scheduler.add_job(cron_process2, 'cron', day_of_week = 'mon-sun', hour='11', minute='29', second='05')
scheduler.add_job(cron_process3, 'cron', day_of_week = 'mon-sun', hour='11', minute='29', second='10')
scheduler.add_job(cron_process4, 'cron', day_of_week = 'mon-sun', hour='11', minute='29', second='15')
scheduler.add_job(cron_process5, 'cron', day_of_week = 'mon-sun', hour='11', minute='29', second='20')
scheduler.add_job(cron_process6, 'cron', day_of_week = 'mon-sun', hour='11', minute='29', second='25')
scheduler.add_job(cron_process7, 'cron', day_of_week = 'mon-sun', hour='11', minute='29', second='30')
scheduler.add_job(cron_process8, 'cron', day_of_week = 'mon-sun', hour='11', minute='29', second='40')
scheduler.add_job(cron_process9, 'cron', day_of_week = 'mon-sun', hour='11', minute='29', second='45')
scheduler.add_job(cron_process10, 'cron', day_of_week = 'mon-sun', hour='11', minute='29', second='50')

scheduler.add_job(cron_process1, 'cron', day_of_week = 'mon-sun', hour='12', minute='29', second='00')
scheduler.add_job(cron_process2, 'cron', day_of_week = 'mon-sun', hour='12', minute='29', second='05')
scheduler.add_job(cron_process3, 'cron', day_of_week = 'mon-sun', hour='12', minute='29', second='10')
scheduler.add_job(cron_process4, 'cron', day_of_week = 'mon-sun', hour='12', minute='29', second='15')
scheduler.add_job(cron_process5, 'cron', day_of_week = 'mon-sun', hour='12', minute='29', second='20')
scheduler.add_job(cron_process6, 'cron', day_of_week = 'mon-sun', hour='12', minute='29', second='25')
scheduler.add_job(cron_process7, 'cron', day_of_week = 'mon-sun', hour='12', minute='29', second='30')
scheduler.add_job(cron_process8, 'cron', day_of_week = 'mon-sun', hour='12', minute='29', second='40')
scheduler.add_job(cron_process9, 'cron', day_of_week = 'mon-sun', hour='12', minute='29', second='45')
scheduler.add_job(cron_process10, 'cron', day_of_week = 'mon-sun', hour='12', minute='29', second='50')

scheduler.add_job(cron_process1, 'cron', day_of_week = 'mon-sun', hour='13', minute='29', second='00')
scheduler.add_job(cron_process2, 'cron', day_of_week = 'mon-sun', hour='13', minute='29', second='05')
scheduler.add_job(cron_process3, 'cron', day_of_week = 'mon-sun', hour='13', minute='29', second='10')

scheduler.add_job(cron_process1, 'cron', day_of_week = 'mon-sun', hour='14', minute='29', second='00')
scheduler.add_job(cron_process2, 'cron', day_of_week = 'mon-sun', hour='14', minute='29', second='05')
scheduler.add_job(cron_process3, 'cron', day_of_week = 'mon-sun', hour='14', minute='29', second='10')

scheduler.add_job(cron_process1, 'cron', day_of_week = 'mon-sun', hour='15', minute='29', second='00')
scheduler.add_job(cron_process2, 'cron', day_of_week = 'mon-sun', hour='15', minute='29', second='05')
scheduler.add_job(cron_process3, 'cron', day_of_week = 'mon-sun', hour='15', minute='29', second='10')

scheduler.add_job(cron_process1, 'cron', day_of_week = 'mon-sun', hour='16', minute='29', second='00')
scheduler.add_job(cron_process2, 'cron', day_of_week = 'mon-sun', hour='16', minute='29', second='05')
scheduler.add_job(cron_process3, 'cron', day_of_week = 'mon-sun', hour='16', minute='29', second='10')

scheduler.start()

