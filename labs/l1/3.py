import numpy as np
import matplotlib.pyplot as plt

frecv = 2000

print("Intervalul de timp dintre doua esantioane este de", 1 / frecv, "s")

mem = 2*  frecv * 3600

print("O ora de achizitie vor ocupa", mem, "bytes")