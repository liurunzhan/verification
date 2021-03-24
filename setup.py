import setuptools

with open("README.md", "r", encoding="utf-8") as fin:
  long_description = fin.read()

setuptools.setup(
  name = "verification",
  version = "0.0.1",
  author = "liurunzhan",
  author_email = "liurunzhan@sina.com",
  description = "A Verilog Verification Script Library based on Python",
  long_description = long_description,
  long_description_content_type = "text/markdown",
  url = "https://github.com/liurunzhan/verification",
  package_dir = {"" : "src"},
  packages = setuptools.find_packages("src"),
  classifiers = [
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: GNU General Public License v3.0",
    "Operating System :: OS Independent",
  ]
)