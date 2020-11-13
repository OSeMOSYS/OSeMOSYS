=================================
Introduction to OSeMOSYS
=================================

At present there is a useful, but limited set of open, free and accessible energy system modeling tools.
These tools often require significant investment in terms of human resources,
training and software purchases in order to apply or further develop them.
The Open Source energy MOdelling SYStem (OSeMOSYS) is specifically designed as a tool to inform the development of local,
national and multi-regional energy strategies and support them with capacity building activities.
Unlike other long established energy systems (partial equilibrium) modeling frameworks (i.e. MARKAL/TIMES [#markal]_ ,
MESSAGE [#message]_ , PRIMES [#primes]_ , EFOM [#efom]_ and POLES [#poles]_ ),
it potentially requires a less significant learning curve.
Additionally, by not using proprietary software or commercial programming languages and solvers,
OSeMOSYS requires no upfront financial investment. This feature increases its affordability,
particularly in developing countries.

It was developed in collaboration with a range of institutions, including the International Atomic Energy Agency (IAEA),
the United Nations Industrial Development Organisation (UNIDO), KTH Royal Institute of Technology, Stanford University,
University College London (UCL), University of Cape Town (UCT), Paul Scherrer Institute (PSI),
Stockholm Environment Institute (SEI), and North Carolina State University.
The first version of OSeMOSYS was made available in 2008, while the first peer-reviewed publication describing its ethos
and structure was available in 2011 [#note1]_ .

OSeMOSYS computes the energy supply mix (in terms of generation capacity and energy delivery)
which meets the energy services demands every year and in every time step of the case under study,
minimising (in its most common form) the total discounted costs.
It can cover all or individual energy sectors, including heat,
electricity and transport and has a user-defined spatial and temporal domain and scale.
The energy demands can be met through a range of technologies which have certain techno-economic characteristics
and draw on a set of resources, defined by certain potentials and costs.
On top of this, policy scenarios may impose certain technical constraints, economic realities or environmental targets.
As in most long-term optimisation modeling tools, OSeMOSYS in its standard configuration assumes a unique decision-maker,
perfect foresight and competitive markets.

In mathematical terms, it is a deterministic, linear optimisation, long-term modeling framework.
Mixed-integer linear programming may be applied for certain functions,
like the optimisation of discrete power plant capacity expansions.

One of its main characteristics is the wide and flexible definition of technology and energy vector.
A technology represents any asset operating energy conversion processes,
from resource extraction and processing to electricity supply, transmission and distribution and end-use appliances.
It could therefore refer to, for example, an oil refinery, a hydropower plant or a heating system.
Each technology is characterised by a transfer function defined by numerous economic,
technical and environmental parameters (e.g. investment and operating costs, efficiency, availability, emission factors,
capacity factor, minimum load, etc.).

The original OSeMOSYS code is written in GNU MathProg, a high level mathematical programming language,
yet straightforward enough to be understandable by all kinds of users, expert or not in linear programming.
In its full version, the code consists of 700 text lines, highly resembling algebraic expressions.
Further parallel versions of the code have been written in GAMS and Python,
for better connection to the respective families of users and coders.
The open source solver GLPK may be used for translating the models in matrices,
finding the optimal solution and printing the numerical outputs.

OSeMOSYS applications can be created and run without interface.
Still, several user interfaces have been developed and are largely employed in teaching and capacity building activities.
The Model Management Infrastructure (MoManI) is an open source, free interface for creating models and visualising results,
available both in online and desktop version.
In addition, OSeMOSYS is integrated into LEAP as module for computing supply capacity expansion planning.

OSeMOSYS is available for download at http://www.osemosys.org/.

The OpTIMUS Community
--------------------------------------------------------------------
OSeMOSYS is part of the OpTIMUS Community, Practice 3: Open Software, together with other world class,
peer reviewed open source tools and data.

OpTIMUS aims at promoting quantitative analysis to inform sustainable development policy,
through the coordination of networks to advance open source software, knowledge development and capacity building.
It is organized in three practices -modeling and capacity building for policy support, expert review and quality control,
and software development.
For more information on the OpTIMUS Community, please visit the related website: http://www.optimus.community/.


.. rubric::
.. [#markal] Energy Technology Systems Analysis Program (IEA-ETSAP), 2015. IEA-ETSAP Energy Systems Analysis Tools. [Online]. Available at: https://iea-etsap.org/index.php/etsap-tools
.. [#message] International Atomic Energy Agency (IAEA), 2015. Planning & Economic Studies Section (PESS): Capacity Building for Sustainable Energy Development. [Online] Available at: https://www.iaea.org/OurWork/ST/NE/Pess/PESSenergymodels.html
.. [#primes] National Technical University of Athens (NTUA), 2015. The PRIMES Energy. [Online] Available at: http://www.e3mlab.ntua.gr/manuals/PRIMES_Brussels_November_2007.pdf
.. [#efom] Van der Voort, E., 1982. The EFOM 12C energy supply model within the EC modelling system. *Omega*, 10 (5), pp. 507–523.
.. [#poles] Enerdata, 2017. POLES: Prospective Outlook on Long-term Energy Systems. [Online] Available at: https://www.enerdata.net/solutions/poles-model.html
.. [#note1] Howells et al., 2011. OSeMOSYS: The Open Source Energy Modeling System: An introduction to its ethos, structure and development. *Energy Policy*, 39 (10), pp. 5850-5870.
