#!/usr/bin/env python
import subprocess
import time
import sys
import os

PATH_TO_GNUPLOT_WIN = r"C:\Program Files\gnuplot\bin\gnuplot.exe"

PATH_TO_GNUPLOT_LINUX = "gnuplot"

PATH_TO_GNUPLOT = "gnuplot"

if sys.platform == "win32":
	if not os.path.exists( PATH_TO_GNUPLOT_WIN ):
		PATH_TO_GNUPLOT_WIN = r"C:\Program Files (x86)\gnuplot\bin\gnuplot.exe"

	PATH_TO_GNUPLOT = PATH_TO_GNUPLOT_WIN


class Gnuplot( object ):
	def __init__( self ):
		self.gnuplot = subprocess.Popen( PATH_TO_GNUPLOT, stdin = subprocess.PIPE, universal_newlines = True )
		
		self._plotstyle = "linespoints"
	
	def __call__( self, content ):
		self.gnuplot.stdin.write( content + "\n" )
		self.gnuplot.stdin.flush()
	
	def load( self, fname ):
		self.gnuplot.stdin.write( "load '%s'" % fname + "\n" )
		self.gnuplot.stdin.flush()
			

	def xlabel( self, content ):
		self.gnuplot.stdin.write( 'set xlabel "%s"\n' % content )
		self.gnuplot.stdin.flush()
		
	def ylabel( self, content ):
		self.gnuplot.stdin.write( 'set ylabel "%s"\n' % content )
		self.gnuplot.stdin.flush()

	def title( self, content ):
		self.gnuplot.stdin.write( 'set title "%s"\n' % content )
		self.gnuplot.stdin.flush()
	
	def key( self, visible ):
		if visible:
			self.gnuplot.stdin.write( "set key\n")
		else:
			self.gnuplot.stdin.write( "unset key\n")
		self.gnuplot.stdin.flush()
	
	def grid( self, visible ):
		if visible:
			self.gnuplot.stdin.write( "set grid\n")
		else:
			self.gnuplot.stdin.write( "unset grid\n")
		self.gnuplot.stdin.flush()
	
	def plotstyle( self, content ):
		self._plotstyle = content
	
	def save_as_png( self, fn ):
		self.gnuplot.stdin.write( "set term png\n" )
		self.gnuplot.stdin.write( 'set output "%s"\n' % fn )
		self.gnuplot.stdin.write( "replot\n" )
		self.gnuplot.stdin.write( "set term wxt	\n" )
		
	
	def plot( self, *args ):
		plots = []
		pos = 0
		while pos < len(args):
			if isinstance( args[pos], list ):
				plots.append( {"x": args[pos], "y": args[pos+1]})
				pos += 2
		
		parts = []
		for plt in plots:
			if len( parts ) > 0:
				parts.append( '"-" using 1:2 with %s' % self._plotstyle )
			else:
				parts.append( 'plot "-" using 1:2 with %s' % self._plotstyle )
		self.gnuplot.stdin.write( ",".join(parts) + "\n" )
		
		for plt in plots:
			for i in range( len(plt["x"]) ):
				self.gnuplot.stdin.write( "%f %f\n" % (plt["x"][i], plt["y"][i] ) )
			self.gnuplot.stdin.write( "e\n" )
		
		self.gnuplot.stdin.flush()
	

