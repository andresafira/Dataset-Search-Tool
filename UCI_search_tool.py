from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from typing import *


def search_UCI_dataset(name: str, driver) -> Union[str, None]:
    ''' Auxiliary function that searchs a dataset in the UCI repository given its title and
    opens the driver in the specified page.
    It returns None if no errors occurred, or the error message
    '''
    UCI_URL = 'https://archive.ics.uci.edu/datasets'
    XPATH_BUTTON = '/html/body/div/div[1]/div[1]/main/div/div[2]/div[2]/div[1]/div/div[2]/h2/a'
    driver.get(UCI_URL)

    try:
        search_bar = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.NAME, 'search'))
        )
        search_bar.send_keys(name)
        search_bar.send_keys(Keys.RETURN)
    except:
        return 'Search bar not found'

    try:
        link_search = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, XPATH_BUTTON))
        )
        link_search.click()

    except Exception as e:
        return 'No dataset found in search results'
    return None


def get_UCI_description_and_link(link: Union[str, None] = None,
                                 name: Union[str, None] = None,
                                 minimize: bool = False) -> Union[str, Tuple[str, str]]:
    '''Function that search a dataset by its name or url, and returns the dataset
    description and the url (as a tuple), if no errors occurred, or the error message.
    '''
    driver = webdriver.Chrome()
    XPATH_TEXT_BLOCK = '/html/body/div/div/div/main/div/div'
    XPATH_VARIABLE_INFO = '/html/body/div/div[1]/div[1]/main/div/div[1]/div[5]/div[2]/div/div/div[1]/div/p'
    XPATH_CREATORS = '/html/body/div/div[1]/div[1]/main/div/div[2]/div[7]/div/div[2]'
    
    if minimize:
        driver.minimize_window()

    if link is not None:
        driver.get(link)
    elif name is not None:
        sud_response = search_UCI_dataset(name, driver)
        if sud_response is not None:
            driver.quit()
            return sud_response
    else:
        driver.quit()
        return 'No option given'

    original_url = driver.current_url
    response = ''


    try:
        text_block = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.XPATH, XPATH_TEXT_BLOCK))
        )
        divs = text_block.find_elements(By.CLASS_NAME, 'shadow')
        descriptions = divs[0].text.split('\n')
        response += descriptions[0] + '\n'
        for i in range(1, len(descriptions) - 1, 2):
           response += f"{descriptions[i]}: {'ERROR: List index out of range' if (i + 1) >= len(descriptions) else descriptions[i + 1]}\n"
        response += divs[1].text.replace('Dataset Information\n', '')
    except Exception as e:
        driver.quit()
        return 'Failed to get dataset description'

    try:
        additional_info = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.XPATH, XPATH_VARIABLE_INFO))
        )
        response += '\n' + additional_info.text
    except:
        pass

    author_txt = '**Author**: '

    achieved = False
    count = 7
    while not achieved and count > 4:
        try:
            authors = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.XPATH, XPATH_CREATORS))
            )
            authors = authors.find_elements(By.CLASS_NAME, 'font-semibold')
            for author in authors:
                author_txt += f'{author.text}, '
            if len(authors) > 0:
                author_txt = author_txt[:-2]
            else:
                raise
            achieved = True
        except:
            XPATH_CREATORS = XPATH_CREATORS.replace(str(count), str(count - 1))
            count -= 1
            pass

    if not achieved:
        author_txt += 'Unknown'

    author_txt += '\n'
    response = author_txt + \
            f'**Source**: [UCI] ({original_url})\n**Please Cite**: [UCI] (https://archive.ics.uci.edu/citation)\n' + \
            response

    driver.quit()
    return response, original_url


def get_UCI_possible_errors() -> dict[str, str]:
    '''Function that returns the possible error messages.
    '''
    return {'Search bar not found': 'The link provided possibly is not working as intended (it is wrong or outdated), since the program could not find the dataset search bar',
            'No dataset found in search results': 'No dataset was found, when trying to search the name given in the UCI dataset list',
            'No option given': 'You must specify an option "link" or "name" in order to use this search tool',
            'Failed to get dataset description': 'The dataset, although exists in the repository, does not have a description option (this error should be rare to occur, since almost all datasets have the description block, even though it can be empty)'}


if __name__ == '__main__':
    dataset_name = 'brazil'
    print(get_UCI_description_and_link(name=dataset_name))
