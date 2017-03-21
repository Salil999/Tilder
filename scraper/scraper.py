import time
# import requests
# from bs4 import BeautifulSoup
# from urllib.request import urlopen
from more_itertools import unique_everseen
from splinter import Browser


def main_content(str_list, min_val):
    '''
    Filters the main contents of a list of strings based on their length.
    This is typically called right after get_all_content().

    Parameters
    ----------
    str_list: A list of strings
    min_val: An integer

    Returns
    -------
    A filtered list
    '''
    return list(filter(lambda x: len(x) > min_val, str_list))


def main_urls(links_list):
    '''
    Filters the URLs that we will navigate to. This is typically called right
    after get_all_urls().

    Parameters
    ----------
    links_list: A list of URLs

    Returns
    -------
    A filtered list
    '''
    # apparently, the last 6 links are just links to "about" all_content
    # so we return everything except those
    return links_list[:len(links_list) - 6]


def get_all_urls(brwsr):
    '''
    Returns all the URLs on a webpage passed that's passed in.

    Parameters
    ----------
    brwsr: A browser object

    Returns
    -------
    A list links
    '''
    all_links = brwsr.find_by_tag('a')
    links_list = list()
    for i in all_links:
        links_list.append(i.value)
    links_list = list(filter(None, links_list))
    return links_list


def get_all_content(brwsr, elem):
    '''
    Grabs every "elem" element there is on the page.

    Parameters
    ----------
    brwsr: A browser object
    elem: An HTML DOM element

    Returns
    -------
    A list of all the "elem" elements that are present on the page
    '''
    all_divs = brwsr.find_by_tag(elem)
    all_divs_strings = list()
    ret_list = list()
    # for some super weird reason, this throws an error - one which I dont get
    # simple fix is to wrap it in try catch
    try:
        for i in all_divs:
            # appends the actual value of the element
            all_divs_strings.append(i.value)
    except:
        pass
    # removes all "falsey" values - fastest method too
    str_list = list(filter(None, all_divs_strings))
    # removes the weird '\n' characters by splitting it
    for i in str_list:
        ret_list.append(i.split('\n'))
    # flattens the list from "split"
    ret_list = [item for sublist in ret_list for item in sublist]
    # removes duplicates while preserving order
    ret_list = list(unique_everseen(ret_list))
    return ret_list


def main():
    '''
    Main function that's called.
    '''
    browser = Browser('phantomjs')
    # this is URL link
    url = 'https://www.coursera.org/learn/text-mining/lecture/7zA4L/\
    1-1-overview-text-mining-and-analytics-part-1'
    browser.visit(url)
    # odd fix, but needed since coursera takes years to load their dynamic HTML
    time.sleep(10)
    all_content = get_all_content(browser, 'div')
    important_shit = main_content(all_content, 150)
    all_urls = get_all_urls(browser)
    important_urls = main_urls(all_urls)
    print(important_urls)
    # print(important_shit)


# loads the URL and visits the specified URL
main()
