#!/usr/bin/env python3
#
# This script parses information about the composition of the german "Bundestag"
# It uses the page http://www.wahlen-in-deutschland.de/bBundestagFraktionen.htm, that has compounded open available statistical information.
#
# CAUTION: It generates a really big output list! Using stream redirection to put the STDOUT to a file could be helpful!
#
# Author: Dan Häberlein
# Page crawled at: 04-22-2014 09.40 PM
#
from lxml import etree
import re

def get_b_tags_from_dom(dom):
    return dom.xpath('//b')

def iterate_over_td_and_get_text(tr_tag):
    td_tags = tr_tag.getchildren()
    for td_tag in td_tags:
        yield td_tag.text

def process_tr_elements(tr_tags):
    result_elec = []
    header_array = []
    for i, cur_tr in enumerate(tr_tags):
        if i == 0:
            header_array = list(iterate_over_td_and_get_text(cur_tr))
        else: 
            cur_dict = {}
            for i, td_content in enumerate(iterate_over_td_and_get_text(cur_tr)):
                cur_dict[header_array[i]] = td_content
                result_elec.append(cur_dict)
    return result_elec


dom = etree.parse('http://www.wahlen-in-deutschland.de/bBundestagFraktionen.htm', parser= etree.HTMLParser())
result_dicts = []
for btag in get_b_tags_from_dom(dom):
    cur_elec_period = btag.text
    starts_with_roman_letter = re.match('^[IVX]', cur_elec_period)
    if starts_with_roman_letter:
        current_table_tag = btag.xpath('./following-sibling::div[1]/table')[0] # this xpagh expression gets the next table element,
                                                                               # which is a child of the direct folowing sibling div element
        #print(cur_elec_period) 
        tr_tags = current_table_tag.xpath(".//tr[not(@style='display:none')]") # extracting all tr elements which contains data
        #print(len(tr_tags))
        result_dicts.append(process_tr_elements(tr_tags))

print(result_dicts)
