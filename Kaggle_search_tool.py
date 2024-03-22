from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from typing import *


def search_kaggle_dataset(name: str, driver) -> Union[str, None]:
    '''Auxiliary function that searchs a dataset in the Kaggle dataset repository given its title and
    opens the driver in the specified page.
    It returns None if no errors occurred, or the error message
    '''
    KAGGLE_URL = 'https://www.kaggle.com/datasets'
    XPATH_SEARCH_BAR = '/html/body/main/div[1]/div/div[5]/div[2]/div[4]/div/div/div[1]/div/input'
    XPATH_BUTTON = '/html/body/main/div[1]/div/div[5]/div[2]/div[5]/div/div/div/ul/li[1]/div[1]/a'
    driver.get(KAGGLE_URL)
    try:
        search_bar = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.XPATH, XPATH_SEARCH_BAR))
        )
        search_bar.send_keys(name)
        search_bar.send_keys(Keys.RETURN)
    except:
        return 'Search bar not found'

    try:
        link_search = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.XPATH, XPATH_BUTTON))
        )
        link_search.click()

    except:
        return 'No dataset found'

    return None


def search_kaggle_competitions(name: str, driver) -> Union[None, str]:
    '''Auxiliary function that searchs a dataset originated of a competition in the Kaggle platform
    given its title and opens the driver in the specified page.
    It returns None if no errors occurred, or the error message
    '''
    KAGGLE_URL = 'https://www.kaggle.com/competitions'
    XPATH_SEARCH_BAR = '/html/body/main/div[1]/div/div[5]/div[2]/div/div[4]/div/div[1]/div/input'
    XPATH_BUTTON = '/html/body/main/div[1]/div/div[5]/div[2]/div/div[5]/div/div/div/ul/li[1]/div[1]/a'

    driver.get(KAGGLE_URL)
    try:
        search_bar = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.XPATH, XPATH_SEARCH_BAR))
        )
        search_bar.send_keys(name)
        search_bar.send_keys(Keys.RETURN)
    except:
        return 'Search bar not found'

    try:
        link_search = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.XPATH, XPATH_BUTTON))
        )
        link_search.click()
    except:
        return 'No competition found'
    return None


def get_authors_dataset(driver) -> str:
    '''Function that get the authors of a dataset that is already available
    in the driver page.
    Returns the authors.
    '''
    XPATH_TO_AUTHOR_BUTTON = '/html/body/main/div[1]/div/div[5]/div[2]/div/div[2]/div/div[5]/div[5]/div[2]/div[2]/div/button'
    XPATH_TO_AUTHOR = '/html/body/main/div[1]/div/div[5]/div[2]/div/div[2]/div/div[5]/div[5]/div[2]/div[2]/div[2]/div'
    response = '**Author**: '
    try:
        author_button = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.XPATH, XPATH_TO_AUTHOR_BUTTON))
        )
        driver.execute_script('arguments[0].click()', author_button)

        author_block = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.XPATH, XPATH_TO_AUTHOR))
        )

        authors = WebDriverWait(author_block, 3).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'author-name'))
        )

        for author in authors:
            temp = author.text.split('\n')[-1].lower().title() + ', '
            if temp == '-, ':
                raise
            response += temp
        response = response[:-2] + '\n'
    except Exception as e:
        response += 'Unknown\n'
    return response


def get_description_dataset(driver) -> Union[str, None]:
    '''Function that get the description of a dataset that is already available
    in the driver page.
    Returns the authors.
    '''
    XPATH_TO_DESCRIPTION = '/html/body/main/div[1]/div/div[5]/div[2]/div/div[2]/div/div[5]/div[1]/div[1]/div[2]/div/div/div'
    XPATH_TO_ABOUT = '/html/body/main/div[1]/div/div[5]/div[2]/div/div[2]/div/div[5]/div[4]/div/div/div[1]/div/div[3]/div[1]/div[2]/div/p[1]'
    original_link = driver.current_url
    response = ''

    try:
        element = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.XPATH, XPATH_TO_DESCRIPTION))
        )
        response += element.text + '\n'
    except:
        return None

    try:
        about = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.XPATH, XPATH_TO_ABOUT))
        )
        response += about.text
    except:
        pass

    return response


def get_authors_competition(driver) -> str:
    '''Function that get the authors of a dataset from a competition that is already available
    in the driver page.
    Returns the authors.
    '''
    XPATH_COMPETITION_HOST = '/html/body/main/div[1]/div/div[5]/div[2]/div/div/div[6]/div[4]/div/div[1]/div[1]/p'

    response = '**Author**: '

    try:
        author_block = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.XPATH, XPATH_COMPETITION_HOST))
        )
        response += author_block.text + '\n'
    except:
        response += 'Unknown\n'

    return response


def get_description_competition(driver) -> Union[str, None]:
    '''Function that get the description of a dataset from a competition that is already available
    in the driver page.
    Returns the description or None (if no description found).
    '''
    XPATH_OVERVIEW = '/html/body/main/div[1]/div/div[5]/div[2]/div/div/div[4]/div[1]/div/div[2]/div/button[1]'
    try:
        overview = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.XPATH, XPATH_OVERVIEW))
        )
        overview.click()
    except:
        return None

    try:
        description = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.ID, 'description'))
        )
        return description.text.replace('link\n', '').replace('keyboard_arrow_up\n', '')
    except:
        return None


def get_cite(driver, competition: bool) -> str:
    '''Funcion that returns the citation of a specific dataset.
    If it is from a competition, there already is a block of text related to that;
    otherwise, just put the dataset link as a citation.
    Returns the citation.
    '''
    XPATH_CITE = '/html/body/main/div[1]/div/div[5]/div[2]/div/div/div[6]/div[2]/div[3]/div/div[2]/div'
    try:
        if not competition:
            raise
        cite = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.XPATH, XPATH_CITE))
        )
        return '**Please Cite**: ' + cite.text + '\n'
    except:
        return '**Please Cite**: ' + driver.current_url + '\n'


def get_kaggle_description_and_link(link: Union[str, None] = None,
                           name: Union[str, None] = None,
                           search_competitions: bool = False,
                           minimize: bool = False) -> Union[str, Tuple[str, str]]:
    '''Function that search a dataset by its name or url, and returns the dataset
    description and the url (as a tuple), if no errors occurred, or the error message.
    '''
    driver = webdriver.Chrome()
    if minimize:
        driver.minimize_window()

    if link is not None:
        driver.get(link)
    elif name is not None:
        if search_competitions:
            skd_response = search_kaggle_competitions(name, driver)
        else:
            skd_response = search_kaggle_dataset(name, driver)

        if skd_response is not None:
            driver.quit()
            return skd_response
    else:
        driver.quit()
        return 'No option was given'

    if search_competitions:
        author_ex = get_authors_competition
        desc_ex = get_description_competition
    else:
        author_ex = get_authors_dataset
        desc_ex = get_description_dataset

    response = author_ex(driver)
    original_link = driver.current_url
    response += f'**Source**: [Kaggle] ({original_link})\n'
    response += get_cite(driver, search_competitions)

    temp = desc_ex(driver)
    if temp is None:
        driver.quit()
        return 'Failed to get competition description'
    response += temp

    driver.quit()
    return response, original_link


def get_kaggle_possible_errors():
    '''Function that returns the possible error messages.
    '''
    return {'Search bar not found': 'The link provided possibly is not working as intended (it is wrong or outdated), since the program could not find the dataset search bar',
            'No dataset found': 'No dataset was found, when trying to search the name given in the kaggle dataset list',
            'No competition found': 'No dataset was found, when trying to search the name given in the kaggle dataset list',
            'No option given': 'You must specify an option "link" or "name" in order to use this search tool',
            'Failed to get dataset description': 'The dataset, although exists in the repository, does not have a description option (this error should be rare to occur, since almost all datasets have the description block, even though it can be empty)',
            'Failed to get competition description': 'The competition, although exists in the repository, does not have a description option (this error should be rare to occur, since almost all datasets have the description block, even though it can be empty)'}


if __name__ == '__main__':
    print(get_kaggle_description_and_link(name='brazil', search_competitions=False))
