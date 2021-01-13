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
		print(content)
		self.gnuplot.stdin.write( content + "\n" )
		self.gnuplot.stdin.flush()
	
	def load( self, fname ):
		self( "load '%s'" % fname)
			

	def xlabel( self, content ):
		self( 'set xlabel "%s"' % content )
		
	def ylabel( self, content ):
		self( 'set ylabel "%s"' % content )
	def title( self, content ):
		self( 'set title "%s"' % content )
	
	def key( self, visible ):
		if visible:
			self( "set key")
		else:
			self( "unset key")
	
	def grid( self, visible ):
		if visible:
			self( "set grid")
		else:
			self( "unset grid")

	def cricle( self, id, x, y, r, colour):
		self( 'set object %s circle at %s,%s size %s' % ( id, x, y, r))

	def ellipse( self, id, x, y, h, w, angle):
		self( 'set object %s ellipse center %s,%s size %s,%s angle %s' % (id, x, y, h, w, angle))

	def rectangle(self, id, x0, y0, x1, y1):
		self( 'set object %s rectangle from %s,%s to %s,%s' % (id, x0, y0, x1, y1))
	
	def plotstyle( self, content ):
		self._plotstyle = content
	
	def save_as_png( self, fn ):
		self( "set term png" )
		self( 'set output "%s"' % fn )
		self( "replot" )
		self( "set term wxt	" )
		
	
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
	

