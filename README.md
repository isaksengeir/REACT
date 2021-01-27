# REACT
Development of a GUI for setting up and analysing DFT reaction (free) energies.

<strong>General dependencies</strong>
<ul>
  <li>Python3.9 (<code>brew install python@3.9 </code>) </li>
  <li>PyQt5 (<code>python -m pip install pyqt5 </code>) </li>
  <li>Matplotlib (<code>python -m pip install matplotlib </code>)</li>
  <li>Numpy (<code>python -m pip install numpy </code>)</li>
  <li>OpenGL (<code>python -m pip install pyOpenGL </code>)</li>
  
</ul>

<strong> Making installer with fbs pyinstaller </strong>
Install fbs pyinstaller (<code>python -m pip install fbs</code>)
<li>Prepare fbs file structure (a one time thing) (<code>fbs startproject </code>) </li>
<li>Run code through fbs (<code>fbs run </code>) </li>
<li>Prepare for installer generate (<code>fbs freeze </code>) </li>
<li>Make installer (<code>fbs installer </code>) </li>
</ul>
For more details on fbs, see <a href="https://www.learnpyqt.com/tutorials/packaging-pyqt5-apps-fbs/">Packaging PyQt5 apps with fbs</a>
