========================================================
= Instructions to build a Windows installation package =
========================================================

1. You need to be in the directory containing this file ($ELEANA_PROJECT/Windows).

2. Open PowerShell.

3. Navigate to the Windows folder of the Eleana project:

	cd $ELEANA_PROJECT/Windows


4. Check if Python is installed:

	python --version

	You should see Python 3.12.7 or a similar version (not too old, not too new).
	If not install it from python.org.

5. Allow execution of PowerShell scripts:

	Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force


6. Run the build script:

	.\build_package.ps1


	This will create a folder called eleanapy where the executable file is placed.

7. Create the Windows Installer using Inno Setup:

	Install Inno Setup 6 or newer: https://jrsoftware.org/isinfo.php

	Download and install Inno Setup.

8. Open eleana.iss in the Inno Setup Compiler.

	Run Build → Compile.

9. The installation package will be created in the ..\Output\EleanaPy_Installer.exe folder.

10. Install Eleana and enjoy!