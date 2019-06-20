=================================
Code versions
=================================

Currently the OSeMOSYS code is available in two versions:

- The *“long code”*, which includes a full version of equations, and

- The *“short code”*, which was developed by merging equations from the long version, in order to reduce the computational time.

The long version is easier to read and understand, as it includes more simple, user-friendly equations. The way the shorter version was developed instead, allows for eliminating the need to calculate and store intermediate values and results in faster calculation times. Key outputs remains the same. 

The long version computes more variables, which help the user in understanding what the model really does. The long version is therefore particularly helpful also to test modifications and enhancements to the main code. Therefore, the use of the long version is recommended unless the calculation times get prohibitively long.

Problems which cannot be solved with the long code, due to time or RAM constraints, can be solved with the short code. To check if the RAM is a limiting constraint, during the computation it is sufficient to open the system task manager (for Windows-based machines, you can use the command Ctrl+Alt+Delete) and check if the RAM use is close to saturation. The RAM and time constraints may become binding when the model gets too complex. This may happen, e.g., when a multi-regional model is set up, with many technologies and time slices. In such cases, the shorter version of the code is recommended. 

The reduction in the number of equations in the short code translates into the generation of a smaller matrix of results to be solved. This significantly reduces the memory usage and the processing time, by 10 times (10x) and 5 times (5x) respectively. 

The short version of the OSeMOSYS code contains only the essential equations required for running the model. However, all the previous equations have been left as before, and "commented out" to better understand the methodology followed to shorten the code. It is important to note that the shortening of the code does not change any aspect of the functionality of OSeMOSYS. Furthermore, there are no special formatting requirements for the data file necessary to run the short code instead of the long one. Both the long and the short versions of OSeMOSYS code are developed and released as parallel versions simultaneously, every time a change is made or a functionality is added. 

The latest versions of the OSeMOSYS code were released on the 8th of November 2017, both for the long and the short code, and are `available for download on the related website <http://www.osemosys.org/get-started.html>`_.
