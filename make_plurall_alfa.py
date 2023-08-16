from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time, random, math
from ai_to_answer_questions import ArtificialInteligence 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

users = [['gk003379@cfjl.com.br', 'charles030617'], ['lb004730', 'plurall123']]#['ep006003', 'erikkgpedo'], ['gk005886', 'gabi0109'][['cm006499@cfjl.com.br', 'ZXXKNM44B'], ['vh003827@cfjl.com.br', 'vrh383940']] #['eb004111', 'cfjl2022'], ['hr003597', 'Hugo2005w']]# ['hr003597', 'Hugo2005w'], ['ds003627@cfjl.com.br', 'zecaurubu'], ['gk003379@cfjl.com.br', 'charles030617'], ['nb006456', 'cfjl2020'], ['gd006738', 'Gustavokd99#']] #["db005156@cfjl.com.br", "derek123"]]#[['hr003597', 'Hugo2005w'], ['vh003827@cfjl.com.br', 'vrh383940']]#, ['bb006144@cfjl.com.br', 'bgb040406'], ['lb004730', 'plurall123']]

def open_plurall():
    browser = webdriver.Firefox()
    browser.set_page_load_timeout(40)

    browser.get('https://conta.plurall.net/')

    return browser

def send_user_passwd(browser, user, passwd):
    inputs = browser.find_elements_by_tag_name("input")

    user_input = inputs[0]
    senha_input = inputs[1]

    user_input.send_keys(user)
    senha_input.send_keys(passwd)
    senha_input.send_keys(Keys.ENTER)

    time.sleep(2)

def get_task(browser, link):
    browser.get(link)

    time.sleep(1)

def close_spam(browser):
    time.sleep(3)
    buttons = browser.find_elements_by_tag_name('button')
    for button in buttons:
        try:
            button.click()
        except Exception:
            pass

def get_task_link(browser):
    for _ in range(2):
        try:
            tarefa = browser.find_elements_by_tag_name("section > a")[0]

            link = tarefa.get_attribute('href')

            return link
        except Exception: #Caso não exita tarefa
            time.sleep(5)
    return None

def open_link(browser, link, time_v=2):
    browser.get(link)

    time.sleep(time_v)

def book_is_opened(livro):
    opened_tags = livro.find_elements_by_tag_name(".MediaTask_task-status-holder__3zAVl")
    style = opened_tags[0].get_attribute("style")
    if style == "background: var(--color-mint30);":
        return True
    return False

def open_book(browser, link):
    global first_book
    #livros = browser.find_elements_by_tag_name(".MediaTask_media-task-with-video__2f4FB")
    livros = browser.find_elements_by_tag_name(".MediaTask_subtask-title__2gDwd")

    if not len(livros):
        return
    
    for livro in livros:
        if book_is_opened(livro):
            continue
        livro.click()
        if first_book:
            time.sleep(15)
            first_book = False
        else:
            time.sleep(5) #5

        open_link(browser, link)

        time.sleep(2) #3

def load_options(browser):
    for _ in range(100):
        time.sleep(0.5)
        options = browser.find_elements_by_class_name("option")
        if len(options) > 1: #!=1
            return options
    else:
        raise Exception

def get_correct_alternative(browser, options):
    correct_alternative = None
    #time.sleep(0.5)
    if len(browser.find_elements_by_class_name("Option_correct__33fLM")):
        for i, option in enumerate(options):
            correct_child = option.find_elements_by_class_name("Option_correct__33fLM")
            if len(correct_child):
                correct_alternative = i

    return correct_alternative

def get_wrong_alternatives(options):
    incorrect_alternatives = []
    for i, option in enumerate(options):
        incorrect_child = option.find_elements_by_class_name("Option_wrong__2FQn_")
        if len(incorrect_child):
            incorrect_alternatives.append(i)

    return incorrect_alternatives

def get_all_possible_alternatives(browsers):

    options = load_options(browsers[0])
    possibles = [_ for _ in range(len(options))]

    for browser in browsers:
        options = load_options(browser)
        wrong_alternatives = get_wrong_alternatives(options)
        correct_alternative = get_correct_alternative(browser, options)

        if correct_alternative != None:
            return [correct_alternative]

        possibles = [possible for possible in possibles if possible not in wrong_alternatives]
    
    return possibles

def click_in_alternative(options, possible_alternatives):
    next_alternative = possible_alternatives[math.floor(random.randint(0, len(possible_alternatives) - 1))]
    try:
        options[next_alternative].find_element_by_class_name("undefined").click()
    except Exception:
        pass

    time.sleep(1)

def go_back(browser):
    browser.back()
    
    time.sleep(2)

def verify_type_question(browser):
    for _ in range(100):
        text_area = bool(len(browser.find_elements_by_tag_name("textarea")))
        options = bool(browser.find_elements_by_class_name("option"))
        send_file = bool(browser.find_elements_by_class_name("css-1o1jo9h"))
        if text_area == True and options == False:
            return 'write'
        elif text_area == False and options == True:
            return 'alternative'
        elif send_file == True:
            return 'send_file'
        else:
            time.sleep(0.5)
    else:
        raise Exception

def get_question_text(browser):
    texts = browser.find_elements_by_tag_name('.Question_question-text__3kSQa > p')
    final_text = ""

    for paragraph in texts:
        text_content = paragraph.text
        final_text = f"{final_text}\n{text_content}"
    
    return final_text

def get_last_response(browsers):
    #time.sleep(0.5)
    response = None
    for browser in browsers:
        last_response = browser.find_elements_by_tag_name(".Answer_feedback__VV2bM")
        if len(last_response):
            response = last_response[0].text
            break
    
    return response

def answer_write_question(browsers):
    #text = get_question_text(browsers[0])

    #response = get_last_response(browsers)

    #if not response:
        #response = AI.make_question(text)
        #response = "<html><html><html><html></html></html></html></html>"#"Error loading the response..."

    #if len(response) <= 20:
    #    response = response*20

    response = "<html><html><html><html></html></html></html></html>"

    for browser in browsers:
        textareas = browser.find_elements_by_tag_name("textarea")

        last_response = browser.find_elements_by_class_name("Answer_answer-container__1wulo")

        if len(textareas) >= 1 and len(last_response) == 0:
            textarea = textareas[0]
            textarea.send_keys(response)

            time.sleep(0.2)

            buttons = browser.find_elements_by_tag_name(".OpenResponse_button__aKV8P > .css-1q446aw")
            buttons[0].click()

            time.sleep(1.5) #1

            browser.find_elements_by_tag_name(".css-1n079h > .css-xj06ml")[0].click() #Envia a resposta

            time.sleep(1.5) #n existe

def answer_question(browsers):
    type_question = verify_type_question(browsers[0])
    if type_question == 'write':
        answer_write_question(browsers)

    elif type_question == 'alternative':
        answer_mark_question(browsers)
    
    elif type_question == 'send_file':
        answer_send_file(browsers)

def answer_send_file(browsers):
    #browsers[0].find_elements_by_class_name('css-q0jh1q')[0].send_keys(r"C:\Users\TEMP\nevermind.jpg")

    response = r"C:\Users\TEMP\nevermind.jpg"

    for browser in browsers:
        image_area = browser.find_elements_by_class_name('css-q0jh1q')

        last_response = browser.find_elements_by_class_name("Answer_answer-container__1wulo")

        if len(image_area) >= 1 and len(last_response) == 0:
            textarea = image_area[0]
            textarea.send_keys(response)

            time.sleep(0.2)

            buttons = browser.find_elements_by_tag_name(".OpenResponse_button__aKV8P > .css-1q446aw")
            buttons[0].click()

            time.sleep(1.5) #1

            browser.find_elements_by_tag_name(".css-1n079h > .css-xj06ml")[0].click() #Envia a resposta

    time.sleep(1.5) #n existe

def answer_mark_question(browsers):
    possibles = get_all_possible_alternatives(browsers)

    point_of_correct = None

    while True:
        for i, browser in enumerate(browsers):
            if point_of_correct == i:
                return
            options = load_options(browser)

            click_in_alternative(options, possibles)

            options = load_options(browser)

            correct_alternative = get_correct_alternative(browser, options)
                
            if correct_alternative != None:
                possibles = [correct_alternative]
                if point_of_correct == None:
                    point_of_correct = i
                    continue
                else:
                    continue
            
            wrong_alternatives = get_wrong_alternatives(options)

            last_possibles = possibles
            possibles =  [possible for possible in possibles if possible not in wrong_alternatives]
            for _ in range(100):
                if last_possibles == possibles and len(possibles) > 1:
                    possibles = get_all_possible_alternatives(browsers)
                else:
                    break
                time.sleep(0.4) #0.7
            else:
                raise Exception


def make_activities_from_task(browsers):
    browser_admin = browsers[0]
    atividades = browser_admin.find_elements_by_class_name("ExerciseCard_exercise-card__29skG")
    n_atividades = len(atividades)

    for activitie_n in range(n_atividades):

        atividade = browser_admin.find_elements_by_class_name("ExerciseCard_exercise-card__29skG")[activitie_n]
        if 'undefined' in atividade.get_attribute("class"):
            link_atividade = atividade.find_element_by_xpath('..').get_attribute('href')
            for browser in browsers:
                open_link(browser, link_atividade, 1.5/len(browsers))
            
            answer_question(browsers)

            go_back(browser_admin)

def init_browser(user, passwd):
    browser = open_plurall()

    send_user_passwd(browser, user, passwd)

    return browser

if __name__ == "__main__":
    #AI = ArtificialInteligence()
    for _ in range(len(users)):
        while True:
            while True:
                first_book = True
                try:
                    browsers = []
                    for user in users:
                        browsers.append(init_browser(user[0], user[1]))

                    browser_admin = browsers[0]

                    links = [
                            "https://atividades.plurall.net/material/10366533/?only_available_todo=true"
                            ]

                    for browser in browsers:
                        get_task(browser, links[0])

                        close_spam(browser)
                    
                    for link in links:
                        get_task(browser_admin, link)
                        
                        while True:
                            task_link = get_task_link(browser_admin)
                            if task_link:
                                open_link(browser_admin, task_link)

                                open_book(browser_admin, task_link)

                                make_activities_from_task(browsers)

                                get_task(browser_admin, link)
                            else:
                                break
                            #time.sleep(10)
                except Exception as e:
                    print(e)
                    for browser in browsers:
                        try:
                            browser.close()
                        except:
                            pass
                    time.sleep(5)
                    continue
                    #break
                break
            end_of_task = bool(len(browser_admin.find_elements_by_class_name("ErrorMessage_no-results__3albA")))
            for browser in browsers:
                try:
                    browser.close()
                except:
                    pass
            if end_of_task:
                break
            time.sleep(5)
        users = [users[-1]] + users[0:-1]

print('ok')

import os

os.system("shutdown -s -t 100")
