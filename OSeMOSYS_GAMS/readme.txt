* OSEMOSYS 2011.07.07 conversion to GAMS by Ken Noble, Noble-Soft Systems - August 2012

Files required are:
osemosys.gms
osemosys_dec.gms
utopia_data.txt
osemosys_equ.gms

To run this GAMS version of OSeMOSYS on your PC:
1. YOU MUST HAVE GAMS VERSION 22.7 OR HIGHER INSTALLED.
   This is because OSeMOSYS has some parameter, variable and equation names
   that exceed 31 characters in length, and GAMS versions prior to 22.7 have
   a limit of 31 characters on the length of such names.
2. Ensure that your PATH contains the GAMS Home Folder.
3. Place all 4 of the above files in a convenient folder,
   open a Command Prompt window in this folder, and enter:
   gams osemosys.gms
4. You should find that you get an optimal value of 26630.2254.
5. Some results are created in file SelResults.CSV that you can view in Excel.