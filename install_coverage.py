import os

package = "coverage"

try:
    __import__package
except:
    os.system("pip install "+ package)