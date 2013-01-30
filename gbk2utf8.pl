#!/usr/bin/perl -w
use strict;
use Encode qw/decode encode/;

die "FATAL: Please specified file to decode as parameters\n" unless @ARGV;
foreach my $orig_file_name (@ARGV) {
    my $file_name =
      encode( 'utf8', decode( 'gbk', decode( 'utf8', $orig_file_name ) ) );
    next if $file_name eq $orig_file_name;
    system("mv $orig_file_name $file_name -v");
}

