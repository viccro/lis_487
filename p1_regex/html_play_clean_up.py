#!/usr/local/bin/python3

import sys
import re

def main(html_path):
    with open(html_path) as html_file:
        play = html_file.read()

    play = strip_preamble(play)
    play = format_act_headers(play)             # write over old play with new formatted value for each substitution
    play = format_scene_headers(play)
    play = format_stage_directions(play)
    play = format_voices(play)
    play = format_lines(play)
    play = strip_tag_and_contents(play, "table")
    play = strip_tags(play)

    print(play)

def strip_preamble(play):
    return re.sub("<!DOCTYPE[ \w\"\-\/\.\:]+>[\n]", #Pull whole contents of <!DOCTYPE > tag
                  "",                           #and delete it
                  play)

def format_act_headers(play):
    return re.sub("<h3>(ACT [A-Za-z]+)</h3>",   #Match everything between h3 tags that contains "ACT " and some more characters
                  "== \g<1> ==",                   #In its place, put that "ACT whatever" string between double equals
                  play)

def format_scene_headers(play):
    return re.sub("<h3>(SCENE [IV]+). ([\w .\-\']+)</h3>",   #Match everything between h3 tags that contains "SCENE " and some more characters
                  "= \g<1> =\n{\g<2>}",                      #In its place, put that "SCENE ##" string between equals and the details on the next line between brackets. This also strips the ". " from between those two strings.
                  play)

def format_stage_directions(play):
    return re.sub("<i>(.+)</i>",            #Find anything between italics tags
                  "[\g<1>]",                #Put them instead between square brackets
                  play)

def format_voices(play):
    return re.sub("<a name=\"\w+\"><b>([\w ]+)</b></a>",    #Grab all <a name="some string"><b>some string</b></a>
                  "\g<1>:",                                 #Put that second 'some string' before a colon
                  play)

def format_lines(play):
    return re.sub("<a name=\"[\d.]+\">(.+)</a><br>",
                    "\t\g<1>",
                  play)

def strip_tags(play):                                       #strip anything remaining between < and >
    return re.sub("<\/?[\w]+( .+)*>\n?",
                  "",
                  play)

def strip_tag_and_contents(play, tag):
    return re.sub("<"+tag+" ?.*>[\w\= \"\/\:\.\|\s\<\>]+</"+tag+">",                      #entirely remove the tag contents
                  "",
                  play)


if __name__ == "__main__":
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        print("Be sure you include the relative path to the csv input")