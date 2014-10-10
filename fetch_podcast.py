#!/usr/bin/python2
#Copyright (C) 2014  Gris Ge <cnfourt@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import feedparser
import re
import os
import signal
import sys
import heapq

_AUDIO_PODCAST_FOLDER="%s/Podcast" % os.getenv('HOME')
_VIDEO_PODCAST_FOLDER="%s/Videocast" % os.getenv('HOME')

pod_list = [
    {
        'folder':  "Global_News",
        'url':  "http://downloads.bbc.co.uk/podcasts/" +
                "worldservice/globalnews/rss.xml",
        'max_count' :  2,
    },
    {
        'folder': "Drama_of_the_Week",
        'url': "http://downloads.bbc.co.uk/podcasts/" +
               "radio4/radioplay/rss.xml",
        'max_count': 5,
    },
    {
        'folder': "Joel_Osteen_Video",
        'url': "http://www.joelosteen.com/_layouts/JOMHelper.asmx/" +
               "GetPodcastVideo",
        'max_count': 5,
    },
    {
        'folder': "NBC_Nightly_News_Video",
        'url': "http://podcastfeeds.nbcnews.com" +
               "/audio/podcast/MSNBC-NN-NETCAST-M4V.xml",
        'max_count': 5,
    },
    {
        'folder': "NBC_Nightly_News_Audio",
        'url': "http://podcastfeeds.nbcnews.com" +
               "/audio/podcast/MSNBC-Nightly.xml",
        'max_count': 2,
    },
    {
        'folder': "NBC_Meet_The_Press_Video",
        'url': "http://podcastfeeds.nbcnews.com" +
               "/audio/podcast/MSNBC-MTP-NETCAST-M4V.xml",
        'max_count': 5,
    },
    {
        'folder': "TED Video HD",
        'url': "http://feeds.feedburner.com/TedtalksHD?format=xml",
        'max_count': 5,
    },
    {
        'folder': "TED Audio",
        'url': "http://feeds.feedburner.com/tedtalks_audio",
        'max_count': 5,
    },
]

_CTRL_C_ERROR_CODE=2
_TMP_EXTENTION='.tmp'
_DL_CMD='wget --continue '
_AUDIO_FILE_EXTENTION='.mp3'
_VIDEO_FILE_EXTENTION='.m4v'

def signal_handler(signal, frame):
    print
    sys.exit(_CTRL_C_ERROR_CODE)

signal.signal(signal.SIGINT, signal_handler)

def download_url(url, file_name, folder, time_stamp, file_ext):
    if not os.path.isdir(folder):
        os.system("mkdir -p '%s'" % folder)
    file_name += "_%s" % time_stamp
    file_name += file_ext
    file_path = "%s/%s" % (folder, file_name)
    if os.path.exists(file_path):
        return None
    cmd = "%s '%s' -O '%s%s'" % (_DL_CMD, url, file_path, _TMP_EXTENTION)
    print "INFO: Downloading %s" % file_name
    err_no = os.system(cmd)
    if err_no == 0:
        if os.system("mv '%s.tmp' '%s'" % (file_path, file_path)) == 0:
            return file_path
    elif err_no == _CTRL_C_ERROR_CODE:
        print
        exit(_CTRL_C_ERROR_CODE)
    else:
        return None

def time_stamp_of_pod_entry(pod_entry):
    time_struct = pod_entry['published_parsed']
    return "%04d%02d%02d%02d%02d" % (
        time_struct.tm_year, time_struct.tm_mon,
        time_struct.tm_mday, time_struct.tm_hour, time_struct.tm_min)

def remove_old_pod(folder, max_count):
    file_list = os.listdir(folder)
    file_2_time_dict = {}
    for file_name in file_list:
        file_path = "%s/%s" % (folder, file_name)
        # Remove tmp file
        (file_basename, file_ext) = os.path.splitext(file_name)
        if file_ext == _TMP_EXTENTION:
            print "INFO: Removing tmp file: %s" % file_path
            os.system("rm '%s'" % file_path)

        file_2_time_dict[file_name] = int(file_basename[-12:])

    top_files = heapq.nlargest(
        max_count, file_2_time_dict, key=file_2_time_dict.get)

    for file_name in file_list:
        file_path = "%s/%s" % (folder, file_name)
        if file_name not in top_files:
            print "INFO: Removing old podcast file: %s" % file_path
            os.system("rm '%s'" % file_path)

for pod in pod_list:
    print "INFO: Fetching '%s'" % pod['folder']
    downloaded_file_paths = []
    parser = feedparser.parse(pod['url'])
    folder_name = None
    counter = 0
    for pod_entry in parser['entries']:
        if counter >= pod['max_count']:
            break
        file_name = pod_entry['title']
        file_name = re.sub(' ', '_', file_name)
        file_name = re.sub('[^a-zA-Z0-9_]', '', file_name)
        file_name = re.sub('_+$', '', file_name)
        time_stamp = time_stamp_of_pod_entry(pod_entry)
        file_ext = None
        for pod_link in pod_entry['links']:
            url = pod_link['href']

            if pod_link['type'][0:5].lower()  == 'audio':
                folder_name = "%s/%s" %(_AUDIO_PODCAST_FOLDER, pod['folder'])
                file_ext = _AUDIO_FILE_EXTENTION
            elif pod_link['type'][0:5].lower()  == 'video':
                folder_name = "%s/%s" %(_VIDEO_PODCAST_FOLDER, pod['folder'])
                file_ext = _VIDEO_FILE_EXTENTION
            else:
                continue

            pod_file_path = download_url(
                pod_link['href'], file_name, folder_name, time_stamp,
                file_ext)
            counter += 1
            if pod_file_path:
                downloaded_file_paths.append(pod_file_path)
                break

    print "INFO: Downloaded %d new podcast for '%s'" % \
        (len(downloaded_file_paths), pod['folder'])
    if downloaded_file_paths:
        print "\n".join(downloaded_file_paths)
        # Remove old podcast files.
    remove_old_pod(folder_name, pod['max_count'])
