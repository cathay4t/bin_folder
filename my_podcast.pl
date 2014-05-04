#!/usr/bin/perl -w
#Copyright (C) 2011  Gris Ge <cnfourt@gmail.com>

#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#any later version.

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.

use strict;
#use lib '/home/fge/MP3-PodcastFetch/lib/';
use MP3::PodcastFetch;

$| = 1;

my @feeds = (
    +{
        name => "Drama of the Week",
        url  => "http://downloads.bbc.co.uk/podcasts/"
          . "radio4/radioplay/rss.xml",
        max => 2,
        artist => 'BBC',
    },
#    +{
#        name => "Global News",
#        url  => "http://downloads.bbc.co.uk/"
#          . "podcasts/worldservice/globalnews/rss.xml",
#        max => 2,
#        artist => 'BBC',
#    },
#    +{
#        name => "In Our Times",
#        url  => "http://downloads.bbc.co.uk/podcasts/radio4/iot/rss.xml",
#        max => 2,
#        artist => 'BBC',
#    },
    +{
        name => "NBC Nightly News Audio",
        url  =>
        "http://podcastfeeds.nbcnews.com/audio/podcast/MSNBC-Nightly.xml",
        max => 2,
        artist => 'NBC',
    },
#    +{
#        name => "NBC Nightly News Video",
#        url  =>
#        "http://podcastfeeds.nbcnews.com/audio/podcast/MSNBC-NN-NETCAST-M4V.xml",
#        max => 2,
#        artist => 'NBC',
#    },
#    +{
#        name => "CNET Updates",
#        url  => "http://feeds.feedburner.com/CnetUpdateHD?format=xml",
#        max => 5,
#        artist => 'CNET',
#    },
    +{
        name => "Joel Osteen Audio",
        url  => "http://www.joelosteen.com/_layouts/JOMHelper.asmx/"
              . "GetPodcastAudio",
        max => 2,
        artist => 'Joel Osteen',
    },
#    +{
#        name => "Joel Osteen Video",
#        url  => "http://www.joelosteen.com/_layouts/JOMHelper.asmx/"
#              . "GetPodcastVideo",
#        max => 1,
#        artist => 'Joel Osteen',
#    },
);

my $st_folder = "/home/fge/Music/podcasts";

sub main() {
    foreach my $ref_feed (@feeds) {
        print "Checking \"$ref_feed->{name}\"\n";
        my $feed = MP3::PodcastFetch->new(
            -base             => $st_folder,
            -rss              => $ref_feed->{url},
            -rewrite_filename => 1,
            -max              => $ref_feed->{max},
            -upgrade_tag      => 'id3v2.3',
            -force_genre      => 'podcast',
            -force_artist     => $ref_feed->{artist},
            -force_album      => $ref_feed->{name},
            -env_proxy        => 1,
        );
        $feed->fetch_pods;
        print "Fetched ", $feed->fetched, " new podcasts\n";
        map { print "$_\n" } ( $feed->fetched_files );
    }
}

main();
