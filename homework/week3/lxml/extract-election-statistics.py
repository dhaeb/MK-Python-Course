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
from roman import fromRoman
from py2neo import *

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

def get_meta_text_after_table(btag):
    return list(map(lambda s : s.strip(), btag.xpath('.//following-sibling::p[1]')[0].itertext()))

class SessionRange(object):
    def __init__(self, interval):
        self.start = interval[0]
        self.end = interval[2]

class ElecPeriod(object):
    def __init__(self, composition, timerange, meta_info, sessions, sessionrange):
        self.composition = composition
        self.timerange = timerange
        self.meta_info = meta_info
        self.total_sessions = sessions
        self.sessionrange = sessionrange

#dom = etree.parse('http://www.wahlen-in-deutschland.de/bBundestagFraktionen.htm', parser= etree.HTMLParser())
dom = etree.parse('file:///home/dhaeb/Dropbox/Studium/Master/Sem8/digital_philology/dhaeb/project/bundestag_zusammensetzung.html', parser= etree.HTMLParser())
result = {} 
for btag in get_b_tags_from_dom(dom):
    cur_elec_period = btag.text
    starts_with_roman_letter = re.match('^[IVX]', cur_elec_period)
    if starts_with_roman_letter:
        match_groups = re.match('^(.+?)\.\sWahlperiode, (.+)', btag.text)
        current_table_tag = btag.xpath('./following-sibling::div[1]/table')[0] # this xpagh expression gets the next table element,
                                                                               # which is a child of the direct folowing sibling div element
        tr_tags = current_table_tag.xpath(".//tr[not(@style='display:none')]") # extracting all tr elements which contains data
        elec_period_number = fromRoman(match_groups.group(1))
        meta_to_election_period = get_meta_text_after_table(btag)
        hasSessionMax = re.findall(r'^1\.\sSitzung\sam\s(\d?\d\.\d?\d\.\d{4}).*bis\s(\d+)\.\sSitzung.*?\sam\s(\d?\d\.\d?\d\.\d{4})', meta_to_election_period[0])
        if hasSessionMax:
            hasSessionMax = hasSessionMax[0]
        else :
            hasSessionMax = ['22.10.2013', None, None]
        result[elec_period_number] = ElecPeriod(process_tr_elements(tr_tags), match_groups.group(2), " ".join(meta_to_election_period), hasSessionMax[1], SessionRange(hasSessionMax))

neo4j.authenticate('kdi-student.de:7474', 'dhaeb', 'neo4jrocks')
graph_db = neo4j.GraphDatabaseService("http://kdi-student.de:7474/db/data/")
graph_db.clear() # kills the database!!!


for k,v in result.items():
    batch = neo4j.WriteBatch(graph_db)
    election_period_node = node(period=k, 
                                timerange=v.timerange, 
                                meta_info=v.meta_info, 
                                total_session_count=v.total_sessions, 
                                first_session=v.sessionrange.start, 
                                last_session=v.sessionrange.end)
    election_period_node = batch.create(election_period_node)
    batch.add_labels(election_period_node, "Election_Period")
    for composition in v.composition:
        composition_node = batch.create(node(session_count=composition['Sitzung'],
                                            overall_mandates=composition['Insgesamt']))
        batch.add_labels(composition_node, "Composition_of_Bundestag")
        batch.create(rel(election_period_node, ("POSSES", {'until_date': composition['Datum']}), composition_node))
    batch.submit()
    print(k)

