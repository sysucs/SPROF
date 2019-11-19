#!/usr/bin/perl

$pdbdir_local = "/mnt/disk1/yang/pub/PDB/divided"; #"/project/aspen/pub/PDB/divided/";
die "usage: $0 chains(1a0a_)\n" if (@ARGV < 1);
foreach(@ARGV){
	chomp;
	next if -e $_;
	print "$_\n";
	&getchain($_);
}
sub getchain{
	my ($pdbnm) = @_;
	$pdbnm .= "_" if length($pdbnm) == 4;
	if(length($pdbnm) != 5) {
		die "irregular pdbnm (5 chars required): $pdbnm\n";
	}
	$sd = substr($pdbnm, 1, 2); $bn = substr($pdbnm, 0, 4);
	$pn0 = "$pdbdir_local/$sd/pdb$bn.ent.gz";
	if(-e $pn0){
		open(fp, "gunzip -c $pn0|");
	} elsif(-e "$bn.pdb.gz"){
		open(fp, "gunzip -c $bn.pdb.gz|");
	} elsif(-e "$bn.pdb"){
		open(fp, "$bn.pdb");
	} else{
		print "no file: $pn0\n"; return;
	}
	open(fpo, "> $pdbnm");
	$chn = $chn0 = substr($pdbnm, 4, 1);
#	$chn =~ tr/[a-z]/[A-Z]/;
	$na = 0;
	while($line = <fp>){
		last if $line =~ /^ENDMDL/;
		if($line =~ /^HETATM/){
			$line = &replace_het($line);
		}
		next if not $line =~ /^ATOM /;
#
		my $rn = substr($line, 17, 3);
		if($rn eq 'ASX') {substr($line, 17, 3) = 'ASN'}
		if($rn eq 'GLX') {substr($line, 17, 3) = 'GLN'}
# remove H atom
		my $an = substr($line, 12, 2);
		next if $an =~ /^H|^ H/;
#
		next if substr($line, 16, 1) !~ /[ A1]/;
		substr($line, 16, 1) = ' ';
# remove duplicate atoms
		$ct = substr($line, 21, 1);
		$chn = $ct if $chn eq "_";
		die "multiple chains in $pn0: $chn $ct\n" if($chn0 eq "_" and $chn ne $chn);
		next if $chn ne $ct;
		chomp $line;
		print fpo substr($line, 0, 80), "\n";
		$na ++;
	}
	print fpo "TER\n";
#	print "$pdbnm: $na\n";
	close fp; close fpo;
}
my $info_old = "";
sub replace_het{
	my ($str) = @_; my $replace = 0;
	my $str0 = $str;
	if(substr($str, 17, 3) eq "MSE") {
		$replace = 1;
		substr($str, 17, 3) = "MET";
		substr($str, 12, 3) = " SD" if(substr($str, 12, 3) eq "SE ");
	}elsif(substr($str, 17, 3) =~ /CS.|CCS/) {
		$replace = 1;
		substr($str, 17, 3) = "CYS";
	}
	if($replace){
		if($info_old ne substr($str0, 17, 10)){
			$info_old = substr($str0, 17, 10);
#			print "replacing $info_old\n";
		}
		substr($str, 0, 6) = "ATOM  ";
	}
	return $str;
}
