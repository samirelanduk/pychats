from distutils.core import setup

setup(name="pychats",
      version="1.0.0",
      description="Conversation analytics",
      long_description="Tools for accessing conversation backups from various sources, and analysing said conversations.",
      url="https://github.com/samirelanduk/pychats",
      author="Sam Ireland",
      author_email="sam.ireland.uk@gmail.com",
      classifiers=["Development Status :: 4 - Beta",
                   "Programming Language :: Python :: 3"],
      packages=["pychats"],
      install_requires=["beautifulsoup4"])