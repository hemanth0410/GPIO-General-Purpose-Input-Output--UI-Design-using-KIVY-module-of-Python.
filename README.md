
Required libraries 

urllib3
`pip import urllib3`

To work with UI we need kivy module; to install the same follow the below commands. 

1. Ensure you have the latest pip and wheel:

`python -m pip install --upgrade pip wheel setuptools`

2. Install the dependencies (skip gstreamer (~120MB) if not needed, see Kivy’s dependencies):

`python -m pip install docutils pygments pypiwin32 kivy.deps.sdl2 kivy.deps.glew`
`python -m pip install kivy.deps.gstreamer`

    For Python 3.5+, you can also use the angle backend instead of glew. This can be installed with:

`python -m pip install kivy.deps.angle`

3. Install kivy:

`python -m pip install kivy`


