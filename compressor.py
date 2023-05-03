import time

start = time.time()
txt = open("quijote_clean.txt").read()
end = time.time()

print(txt)
print("Temps compressió: ", end - start)