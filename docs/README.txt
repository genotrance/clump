What is Clump
-------------

Clump is a simple Gui Tail. It also allows capture of output from 
commands on the console. The output captured can then be saved to 
a file for further analysis if needed.

Clump is written in Python and uses wxPython. For Windows, it is 
packaged using Py2Exe and installed using NSIS.

Installation
------------

The Windows installer copies the executable files, source code and 
the README to a directory of your choice. It then creates a link 
in the "Send To" folder and a batch file in the Windows directory.

The installer does not create any start menu shortcuts since Clump 
is typically invoked on the console or using "Send To".

For *Nix, refer to the *Nix tips section further below.

Usage
-----

To capture the output of a command on the console, pipe the output 
to Clump.

	c:\> dir | clump
	
To capture stderr, redirect it to stdout using 2>&1.

	c:\> nmake -f make.mak 2>&1 | clump
	
To tail a file in the console, specify it as an argument.

	c:\> clump filename.log

To tail a file in Windows Explorer, use the "Send To" shortcut - 
right click on the file, select "Send To" and then select Clump.

Uninstallation
--------------

Clump for Windows can be uninstalled from "Add or Remove Programs" 
in the Control Panel.

*Nix tips
---------

The following should have Clump running in *Nix.

- Install Python if it is not already present
- Install the wxPython toolkit
- Download and extract the Clump source to a directory of your choice
- Setup an alias for Clump as follows
  
  # alias clump python /path/to/clump.py

Once this is done, the above console examples should work.

I haven't tried Clump on *Nix yet so if you have, do share your 
experiences!

License
-------

Clump is being released under the GPL. The source code is included 
in the installer.

Contact
-------

Contact genosha@genotrance.com for any questions regarding this 
program. 

Links
-----

Clump website
http://www.genotrance.com/pmwiki.php/Programming/Clump

Python
http://www.python.org

wxPython
http://www.wxpython.org

Py2Exe
http://www.py2exe.org

NSIS
http://nsis.sf.net