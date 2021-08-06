import csv
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException


def get_olympic_medals(driver):
    """
    This function scrapes the 2018 Olympics medal table from Wikipedia. If this table changes at all, this function
    will not work :)

    Also, you screenshotted the entire table--including the totals row--I am excluding this row intentionally. My SQL
    queries would be messed up!

    :param driver: Chrome web driver instance. Use the right version of the chromedriver.exe that matches your installed
    version of Google Chrome
    :return: Returns True or False representing successful or unsuccessful completion
    """

    url = 'https://en.wikipedia.org/wiki/2018_Winter_Olympics_medal_table'

    driver.get(url)
    medal_table_xpath = '//*[@id="mw-content-text"]/div[1]/table[2]'

    try:
        medal_table = driver.find_element_by_xpath(medal_table_xpath)
    except NoSuchElementException as e:
        print(e)
        print('Failure! Cannot find the table... something must have changed!')
        return False

    table_rows = medal_table.find_elements_by_tag_name('tr')

    tie_rank = 0  # The countries that came in ties do not each have their own tag containing the rank. Only the first
    # row in the table has the <td> tag containing the rank.

    for i, tr in enumerate(table_rows):

        # Skip the table header row
        if i == 0:
            continue

        row_data = tr.find_elements_by_tag_name('td')  # All data containing numerical figures
        country_name = tr.find_element_by_tag_name('th').text  # Country name is stored with the <th> tag within a <tr>
        country_name = str(country_name).strip()  # There is some unwanted spacing when scraped from web element. Strip!

        # Skip the total summary row
        if 'Totals' in country_name:
            continue

        # As mentioned above, in the event of a tie, the rank is excluded for rows following the first row at that rank
        if len(row_data) == 5:
            rank = row_data[0].text
            gold = row_data[1].text
            silver = row_data[2].text
            bronze = row_data[3].text
            total = row_data[4].text

            tie_rank = row_data[0].text  # Store the rank so, in the event of a tie, the next row can access its rank

        else:
            rank = tie_rank  # This is a country tied, so we must use the previously stored rank from the row prior
            gold = row_data[0].text
            silver = row_data[1].text
            bronze = row_data[2].text
            total = row_data[3].text


        save_olympic_data(rank, country_name, gold, silver, bronze, total, 'olympics.csv')

    return True


def save_olympic_data(rank, noc, gold, silver, bronze, total, output_dir):
    """
    Function to store table data. Separation of concerns!
    :param rank: The country's rank
    :param noc: The "National Olympic Committee" or more simply, the country
    :param gold: The number of gold medals a country won
    :param silver: The number of silver medals a country won
    :param bronze: The number of bronze medals a country won
    :param total: The total number of medals a country won
    :param output_dir: The directory we wish to append data to
    :return: Returns nothing at this time!
    """
    writer = csv.writer(open(output_dir, 'a', newline=''))
    writer.writerow([rank, noc, gold, silver, bronze, total])


if __name__ == "__main__":
    driver = webdriver.Chrome()
    get_olympic_medals(driver)
