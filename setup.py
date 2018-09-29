from setuptools import setup

setup(name='pyautospell',
      version='0.1',
      description='A Python library that automatically corrects English text by re-ranking corrections with an ngram model.',
      url='https://github.com/adam-faulkner/PyAutoSpell.git',
      author='Adam Faulkner',
      author_email='adamflkr@gmail.com',
      license='MIT',
      packages=['pyautospell'],
	classifiers=[
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OSX",
    ],
      zip_safe=False)
