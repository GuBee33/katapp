import sys
from io import StringIO
import pandas as pd
from selenium import webdriver
from random import randint
from time import sleep

def message(text_a,text_b,f_name,l_name,company):
    if company != "":
        return text_a.replace('{f_name}',f_name).replace('{l_name}',l_name).replace('{company}',company)
    else: 
        return text_b.replace('{f_name}',f_name).replace('{l_name}',l_name).replace('{company}',company)

def scroll_down(browser,SCROLL_PAUSE_TIME=2,max_iteration=20):

    # Get scroll height
    last_height = browser.execute_script("return document.body.scrollHeight")
    iteration = 0
    while True:
        iteration+=1
        if iteration == max_iteration:
            break
        # Scroll down to bottom
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = browser.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height       

def prepare_data(fbusername,fbpw,fb_url,max_iteration,text_whith_company,text_whithout_company):
    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.default_content_setting_values.notifications" : 2}
    chrome_options.add_experimental_option("prefs",prefs)
    browser = webdriver.Chrome('chromedriver',chrome_options=chrome_options)
    browser.maximize_window()
    browser.get(fb_url)
    browser.find_element_by_id("u_0_h").click()
    browser.execute_script(f"document.getElementById('email').value='{fbusername}'")
    browser.execute_script(f"document.getElementById('pass').value='{fbpw}'")
    browser.find_element_by_id("loginbutton").click()
    scroll_down(browser,1.5,max_iteration) 
    names = browser.find_elements_by_xpath('//*[@class = "oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl oo9gr5id gpro0wi8 lrazzd5p"]')[1:]
    jobs = browser.find_elements_by_xpath('//*[@class = "d2edcug0 hpfvmrgz qv66sw1b c1et5uql rrkovp55 a8c37x1j keod5gw0 nxhoafnm aigsh9s9 d9wwppkn fe6kdd0r mau55g9w c8b282yb mdeji52x sq6gx45u a3bd9o3v knj5qynh pipptul6 hzawbc8m"]')

    fb={}
    for i in range(len(names)):
        tmp = jobs[i].text.replace("Itt dolgozik:","Wokrs, itt:").replace(", itt:"," at").split(" at ")
        job=""
        workplace=""
        other=""
        if len(tmp)==2:
            job,workplace=tmp
            if job=="Works":
                job = ""
        else:
            other=tmp[0]
        name_split = names[i].text.split(" ")
        f_name=""
        l_name=""
        if len(name_split)==2:
            f_name = name_split[0]
            l_name = name_split[1]
        else:
            f_name = " ".join(name_split[:2])
            l_name = " ".join(name_split[2:])

        fb[i]={"name":names[i].text,"f_name":f_name,"l_name":l_name,"workplace":workplace,"job":job,"other":other}
    
    df = pd.DataFrame.from_dict(fb).transpose()
    df.drop_duplicates(inplace=True)
    df["link"]=df.apply(lambda x: f'https://www.linkedin.com/search/results/people/?firstName="{x.f_name}"&lastName="{x.l_name}"&keywords="{x.workplace}"', axis=1)
    df["link2"]=df.apply(lambda x: f'https://www.linkedin.com/search/results/people/?firstName="{x.l_name}"&lastName="{x.f_name}"&keywords="{x.workplace}"', axis=1)
    df["link_wo_comp"]=df.apply(lambda x: f'https://www.linkedin.com/search/results/people/?firstName="{x.f_name}"&lastName="{x.l_name}"', axis=1)
    df["link_wo_comp2"]=df.apply(lambda x: f'https://www.linkedin.com/search/results/people/?firstName="{x.l_name}"&lastName="{x.f_name}"', axis=1)
    df["message"]=df.apply(lambda x: message(text_whith_company,text_whithout_company,x.f_name,x.l_name,x.workplace), axis=1)
    df["message2"]=df.apply(lambda x: message(text_whith_company,text_whithout_company,x.l_name,x.f_name,x.workplace), axis=1)
    df["message_wo_comp"]=df.apply(lambda x: message(text_whith_company,text_whithout_company,x.f_name,x.l_name,""), axis=1)
    df["message_wo_comp2"]=df.apply(lambda x: message(text_whith_company,text_whithout_company,x.l_name,x.f_name,""), axis=1)
    df["result"]=""
    print(df)
    return browser,df

def check_link(browser,df,index,row,col,dryrun,min_wait,max_wait):
    l=row[col]
    browser.execute_script("window.open('"+l+"','_blank');")
    browser.switch_to.window(browser.window_handles[-1])
    sleep(randint(min_wait,max_wait))
    if browser.find_elements_by_class_name('search-no-results'):
        browser.close()
        browser.switch_to.window(browser.window_handles[-1])
        if col == "link":
            check_link(browser,df,index,row,"link2",dryrun,min_wait,max_wait)
        elif col == "link2":
            check_link(browser,df,index,row,"link_wo_comp",dryrun,min_wait,max_wait)
        elif col == "link_wo_comp":
            check_link(browser,df,index,row,"link_wo_comp2",dryrun,min_wait,max_wait)
        elif col == "link_wo_comp2":
            df.loc[index,"result"]="Not Found"
    else:
        m=row[f"message{col[4:]}"]
        connect_buttons =browser.find_elements_by_class_name("search-result__action-button")
        results_total= browser.find_elements_by_class_name("search-results__total")[0]
        if len(connect_buttons)==1 and int(results_total.text.split(" ")[0])==1:
            for con in connect_buttons:
                con.click()
                addnote_buttons =browser.find_elements_by_css_selector("[aria-label='Add a note']")
                addnote_buttons[0].click()
                send_ivites =browser.find_elements_by_css_selector("[aria-label='Send now']")
                message_box=browser.find_element_by_name("message")
                message_box.send_keys(m)
                if dryrun:
                    dismiss_buttons =browser.find_elements_by_css_selector("[aria-label='Dismiss']")
                    dismiss_buttons[0].click()
                    if df.loc[index,"result"]!='':
                        df.loc[index,"result"].append(f"Found with {col} but not sent\n")
                    else:
                        df.loc[index,"result"]=[f"Found with {col} but not sent\n"]
                else:
                    send_ivites[0].click()
                    if df.loc[index,"result"]!='':
                        df.loc[index,"result"].append(f"Found with {col}")
                    else:
                        df.loc[index,"result"]=[f"Found with {col}"]
                sleep(randint(min_wait,max_wait))
        else:
            if df.loc[index,"result"]!='':
                df.loc[index,"result"].append(f"Found with {col} but not contactable\n")
            else:
                df.loc[index,"result"]=[f"Found with {col} but not contactable\n"]



def LinkeDary(fbusername,fbpw,fb_url,max_iteration,liusername,lipw,first_row,last_row,text_whith_company,text_whithout_company,dryrun,min_wait,max_wait):
    browser,df=prepare_data(fbusername,fbpw,fb_url,max_iteration,text_whith_company,text_whithout_company)
    browser.execute_script("window.open('','_blank');")
    browser.switch_to.window(browser.window_handles[-1])
    browser.get('https://www.linkedin.com/')
    browser.execute_script(f"document.getElementById('session_key').value='{liusername}'")
    browser.execute_script(f"document.getElementById('session_password').value='{lipw}'")
    browser.switch_to.window(browser.current_window_handle)
    login_button =browser.find_element_by_class_name("sign-in-form__submit-button")
    login_button.click()
    for index,row in df[first_row:last_row].iterrows():
        check_link(browser,df,index,row,"link",dryrun,min_wait,max_wait)
    result_html  = df[first_row:last_row][["name","result","message"]].to_html()
    result_html += df[first_row:last_row]["result"].apply(lambda x: x if x=="Not Found" else x[0]).value_counts().to_frame().to_html()
    return result_html