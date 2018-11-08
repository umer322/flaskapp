from flask import Flask,render_template,request
from bs4 import BeautifulSoup
from selenium import webdriver 
from selenium.webdriver.support.ui import Select
import time
from datetime import datetime
import calendar

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
options = webdriver.ChromeOptions()
# options.add_argument('headless')
# options.add_argument('window-size=1200x600')
app=Flask(__name__)

allflightdata=[]

@app.route('/')
def index():
    return render_template('index.html')





@app.route('/home',methods=['POST','GET'])
def home():
    if request.method == 'POST':
        # data={}
        # data['id']=0
        # data['airlinedetail']={}
        # data['airlinedetail']['airlinename']='AI 9832Air India'
        # data['airlinedetail'][0]='ATR TURBOPROP,32A'
        # data['airlinedetail'][1]='Refundable'
        # data['departdetail']='08:15,Wed, 7 Nov \'18IXC ,EIP9I'
        # data['arrivaldetail']='15:15,Wed, 7 Nov \'18MAA ,Terminal 4'
        # data['duration']='07H 00M 1 Stop'
        # data['limitation']='1 Seat(s) left at this price!'
        # data['fare']='Rs.\xa09363'
        # flightdata=[]
        # for i in range(0,5):
        #     flightdata.append(data)

        # return render_template('home.html',data=flightdata)
        roundtrip=False
        triptype=request.form['triptype']
        tripfrom=request.form['tripfrom']
        tripto=request.form['tripto']
        if request.form['departtime']:
            
            if request.form['departtime'] <= datetime.now().strftime('%Y-%m-%d'):
                return render_template('home.html',error='Departure date must be after today') 
            departdate=request.form['departtime'].split('-')[2]
            departmonth=int(request.form['departtime'].split('-')[1])
            departyear=request.form['departtime'].split('-')[0]
        else:
            return render_template('home.html',error='Please enter departure date correctly!')  

        if triptype == 'round' and not request.form['returntime']:
            return render_template('home.html',error='Please enter return date if you want a round trip !')
        elif triptype == 'round' and request.form['returntime']:
            returndate=request.form['returntime'].split('-')[2]
            returnmonth=int(request.form['returntime'].split('-')[1])
            returnyear=request.form['returntime'].split('-')[0]
            roundtrip=True

        if roundtrip and request.form['returntime']<= request.form['departtime']:
            return render_template('home.html',error='Please note that return date must be after the departure date!')

        adults=request.form['adults']
        childs=request.form['childs']
        infants=request.form['infants']
        travelclass=request.form['travelclass']
        airlines=request.form['airlines']
        
        driver = webdriver.Chrome(executable_path='chromedriver.exe',chrome_options=options)
        driver.get('https://exindia.akbartravelsonline.com/MyAccount/Login')
        try:
            driver.find_element_by_xpath('//*[@id="wzrk-cancel"]').click()
        except:
            pass    
        driver.find_element_by_xpath('//*[@id="LoginID"]').send_keys('PMT')
        time.sleep(2)
        driver.find_element_by_xpath('//*[@id="LoginPwd"]').send_keys('samsung123')
        driver.find_element_by_xpath('//*[@id="IDLoginUser"]').click()
        time.sleep(2)
        driver.get('http://exindia.akbartravelsonline.com/Flight')
        
              
        driver.find_element_by_xpath('//*[@id="From"]').send_keys(tripfrom)
        driver.find_element_by_xpath('//*[@id="To"]').send_keys(tripto)
        

        depart_month=calendar.month_abbr[departmonth]

        driver.find_element_by_xpath('//*[@id="DepartureDate"]').click()
        time.sleep(2)
      
        
        while driver.find_element_by_xpath('//*[@id="ui-datepicker-div"]/div[1]/div/div/span[1]').text[0:3] != depart_month or departyear != driver.find_element_by_xpath('//*[@id="ui-datepicker-div"]/div[1]/div/div/span[2]').text:
            driver.find_element_by_xpath('//*[@id="ui-datepicker-div"]/div[2]/div/a/span').click()

        time.sleep(2)
        
        datetable=driver.find_element_by_xpath('//*[@id="ui-datepicker-div"]/div[1]/table/tbody')
        singledate=datetable.find_elements_by_tag_name('td')
        for single in singledate:
            
            if departdate[0:1] == '0':
                departdate=departdate[1:]
            if single.text == departdate:
                single.find_element_by_tag_name('a').click()
                break
           
        if roundtrip:
            driver.find_element_by_xpath('//*[@id="SearchType2"]').click()
            driver.find_element_by_xpath('//*[@id="ReturnDate"]').click()
            time.sleep(2)
            return_month=calendar.month_abbr[returnmonth]
            while driver.find_element_by_xpath('//*[@id="ui-datepicker-div"]/div[1]/div/div/span[1]').text[0:3] != return_month or returnyear != driver.find_element_by_xpath('//*[@id="ui-datepicker-div"]/div[1]/div/div/span[2]').text:
                driver.find_element_by_xpath('//*[@id="ui-datepicker-div"]/div[2]/div/a/span').click()
            time.sleep(2)
            datetable=driver.find_element_by_xpath('//*[@id="ui-datepicker-div"]/div[1]/table/tbody')
            singledate=datetable.find_elements_by_tag_name('td')
            for single in singledate:
                if returndate[0:1] == '0':
                    returndate=returndate[1:]
                if single.text == returndate:
                    single.find_element_by_tag_name('a').click()
                    break    

            select = Select(driver.find_element_by_xpath('//*[@id="Adlt"]'))
            select.select_by_visible_text(adults)
            select = Select(driver.find_element_by_xpath('//*[@id="Chld"]'))
            select.select_by_visible_text(childs)
            select = Select(driver.find_element_by_xpath('//*[@id="Inft"]'))
            select.select_by_visible_text(infants)
            select = Select(driver.find_element_by_xpath('//*[@id="Travel"]'))
            select.select_by_visible_text(travelclass)
            driver.find_element_by_xpath('//*[@id="dvSinglCity"]/div[1]/div[2]/div[3]/div/a').click()
            try:
                driver.find_element_by_xpath('//*[@id="NormalSrch"]/a/span').click()
            except:
                pass    
            time.sleep(10)
            alert=driver.find_element_by_xpath('//*[@id="divNoResult"]/div[2]/div[1]/span').text
            if alert == 'We are sorry, no flight were found that match your criteria':
                return render_template('home.html',error='Please change the search criteria and try again.')
            pagedata=driver.page_source
            soup=BeautifulSoup(pagedata,'html.parser')
            fulldata=soup.find('div',class_='doms-listcont')
            goingdata=[]
            comingdata=[]
            for q,singlediv in enumerate(fulldata.find_all('div',class_='doms-showing-box')):
                
               
                singledepartdata={}
                departfrom=singlediv.find('div',class_='doms-showinghead-text').text
                for singledivdata in singlediv.find_all('div',class_='doms-showing-main'):
                    flightname=singledivdata.find('div',class_='doms-box-twotext').text.split('<br>')[0]
                    flighttime=singledivdata.find('div',class_='doms-box-threetext').text.split('<br>')[0]
                    flightduration=singledivdata.find('div',class_='doms-box-fouetext').text
                    flightarrival=singledivdata.find('div',class_='doms-box-fivetext').text
                    flightfare=singledivdata.find('div',class_='doms-pay-pricesm visFalse').text
                    for w,flightdetails in enumerate(singledivdata.find('div',class_='doms-airlinedet').find_all('div')):
                        singledepartdata[w]=flightdetails.find('a').get('title')

                      
                    singledepartdata['flightname']=flightname
                    singledepartdata['flighttime']=flighttime
                    singledepartdata['flightduration']=flightduration
                    singledepartdata['flightarrival']=flightarrival
                    singledepartdata['flightfare']=flightfare
                    singledepartdata['departfrom']=departfrom

                    if q==0:
                        goingdata.append(singledepartdata)
                    elif q==1:
                        comingdata.append(singledepartdata)

            return render_template('home.html',goingdata=goingdata,comingdata=comingdata)


        select = Select(driver.find_element_by_xpath('//*[@id="Adlt"]'))
        select.select_by_visible_text(adults)
        select = Select(driver.find_element_by_xpath('//*[@id="Chld"]'))
        select.select_by_visible_text(childs)
        select = Select(driver.find_element_by_xpath('//*[@id="Inft"]'))
        select.select_by_visible_text(infants)
        select = Select(driver.find_element_by_xpath('//*[@id="Travel"]'))
        select.select_by_visible_text(travelclass)
        driver.find_element_by_xpath('//*[@id="dvSinglCity"]/div[1]/div[2]/div[3]/div/a').click()
        time.sleep(10)
        alert=driver.find_element_by_xpath('//*[@id="divNoResult"]/div[2]/div[1]/span').text
        if alert == 'We are sorry, no flight were found that match your criteria':
            return render_template('home.html',error='We are sorry, no flight were found that match your criteria <br> Please change the search criteria and try again.')
        pagedata=driver.page_source
        soup=BeautifulSoup(pagedata,'html.parser')
        alldata=soup.find('div',class_='flightdisplayarea')
        
        eachdata=alldata.find_all('div',class_='flightdispcon')
        for k,singlelist in enumerate(eachdata):
            singleflightdata={}
            singleflightdata['id']=k
            singleflightdata['airlinedetail']={}
            for i,onediv in enumerate(singlelist.find_all('div',class_='airlinedet')):
                
                if i == 0:
                    continue
                elif i == 1:
                    singleflightdata['airlinedetail']['airlinename']=onediv.text
                    text=onediv.text
                    if 'IndiGo' in text:

                        singleflightdata['airlinedetail']['src']='/static/img/6E.gif'
                        singleflightdata['flightname']='IndiGo'
                        singleflightdata['flight']=text.replace('IndiGo','')
                    elif 'SpiceJet' in text:
                        singleflightdata['airlinedetail']['src']='/static/img/SpiceG.gif'
                        singleflightdata['flightname']='SpiceJet'
                        singleflightdata['flight']=text.replace('SpiceJet','')
                    elif 'Air Asia' in text:
                        singleflightdata['airlinedetail']['src']='/static/img/AirA.gif' 
                        singleflightdata['flightname']='Air Asia' 
                        singleflightdata['flight']=text.replace('Air Asia','') 
                    elif 'Jet Airways' in text:
                        singleflightdata['airlinedetail']['src']='/static/img/JetA.gif'  
                        singleflightdata['flightname']='Jet Airways'
                        singleflightdata['flight']=text.replace('Jet Airways','')
                    elif 'Air India' in text:
                        singleflightdata['airlinedetail']['src']='/static/img/airv.gif'
                        singleflightdata['flightname']='Air India'
                        singleflightdata['flight']=text.replace('Air India','')
                    elif 'Air Vistara' in text:
                        singleflightdata['airlinedetail']['src']='/static/img/AirI.gif'
                        singleflightdata['flightname']='Air Vistara'
                        singleflightdata['flight']=text.replace('Air Vistara','')          
                    elif 'Go Air' in text:
                        singleflightdata['airlinedetail']['src']='/static/img/GoAir.gif'
                        singleflightdata['flightname']='Go Air' 
                        singleflightdata['flight']=text.replace('Go Air','')  
                    elif 'TruJet' in text:
                        singleflightdata['airlinedetail']['src']='/static/img/TruJ.gif'
                        singleflightdata['flightname']='TruJet' 
                        singleflightdata['flight']=text.replace('TruJet','')      

                elif i == 2:
                    for j,singledetail in enumerate(onediv.find_all('div',class_='typeitemcontainer')):
                       
                        if singledetail.find('a'):
                            singleflightdata['airlinedetail'][j]=singledetail.find('a').get('title')

                        else:
                            continue
                    
            departdetail=singlelist.find_all('div',class_='tltip depart')
            for k,departingdetail in enumerate(departdetail):
                if k == 0:
                    singleflightdata['departdate']=departingdetail.text[:21]
                    singleflightdata['departdetail']=departingdetail.text[21:]
                elif k ==1:
                    singleflightdata['arrivaldate']=departingdetail.text[:21]
                    singleflightdata['arrivaldetail']=departingdetail.text[21:]

            duration=singlelist.find('div',class_='duration').text 
            singleflightdata['duration']=duration
            try:
                limitation=singlelist.find('div',class_='offerseat-text').text   
                singleflightdata['limitation']=limitation
            except:
                pass    
            fare=singlelist.find('div',class_='mainfare').text
            singleflightdata['fare']=fare   
            allflightdata.append(singleflightdata)
            

        # driver.close()
        return render_template('home.html',data=allflightdata)

    return render_template('home.html')


@app.route('/home/<int:id>')
def singlepage(id):

  
    return render_template('singlepage.html',id=id)


if __name__=='__main__':
    app.run(debug=True)    