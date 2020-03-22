#!/usr/bin/python3

# dependencies graphicsmagick-imagemagick-compat, autotrace

import argparse, os, random, re, shutil

print ("vectory.py v1.0 last update 19.03.2020")
print ("\\\\ Animated SVG glitch 4 videoz")
print (" ")
print ("glitch tool made with love for the glitch art community <3")
print ("if you have any questions, would like to contact me")
print ("or even hire me for performance / research / education")
print ("you can shoot me an email at kaspar.ravel@gmail.com")
print ("___________________________________")
print (" ")
print ("wb. https://www.kaspar.wtf ")
print ("fb. https://www.facebook.com/kaspar.wtf ")
print ("ig. https://www.instagram.com/kaspar.wtf ")
print ("___________________________________")
print (" ")

#parse arguments
parser = argparse.ArgumentParser(add_help=True)
parser.add_argument("-i", "--input", help="input file")
parser.add_argument("-s", "--size", dest='size', help="size", default="1")

args = parser.parse_args()

filein = args.input
size = int(args.size)

#define temp directory and files
temp_nb = random.randint(10000, 99999)
temp_dir = "temp-" + str(temp_nb)
temp_sub_frames = temp_dir + '/frames'
temp_sub_pnm = temp_dir + '/pnm'
temp_sub_svg = temp_dir + '/svg'
temp_sub_gsvg = temp_dir + '/gsvg'
temp_sub_png = temp_dir + '/png'

os.mkdir(temp_dir)
os.mkdir(temp_sub_frames)
os.mkdir(temp_sub_pnm)
os.mkdir(temp_sub_svg)
os.mkdir(temp_sub_gsvg)
os.mkdir(temp_sub_png)

#convert video to frames
os.system('ffmpeg -i ' + filein + ' ' + temp_sub_frames + '/%06d.png')

#convert to pnm
print("> converting to pnm")
for file in os.listdir(temp_sub_frames):
	os.system('convert ' + temp_sub_frames + '/' + file + ' ' + temp_sub_pnm + '/' + file[:-4] + '.pnm')

#convert to svg
print("> converting to svg")
for file in os.listdir(temp_sub_pnm):
	os.system('autotrace ' + temp_sub_pnm + '/' + file + ' -color-count 256 -output-file ' + temp_sub_svg + '/' + file[:-4] + '.svg')

#glitch shit
print("> glitching svg files")
for file in os.listdir(temp_sub_svg):
	f1 = open(temp_sub_svg + '/' + file, 'r')
	f2 = open(temp_sub_gsvg + '/' + file, 'w')
	i = 0
	for line in f1:
		i = i + 1
		if i > 2:
			#r1 = str(random.randint(0, 9))
			r1 = str(random.randint(0, 9))
			r2 = str(random.randint(0, 9))

			if size == 1:
				line = re.sub(r"" + re.escape(r1) + "(?=\s)", r2, line)
			elif size == 2:
				line = re.sub(r"" + re.escape(r1) + "(?=\s)", r2, line)
				line = re.sub(r"" + re.escape(r1) + "(?=\d\s)", r2, line)
			elif size == 3:
				line = re.sub(r"" + re.escape(r1) + "(?=\s)", r2, line)
				line = re.sub(r"" + re.escape(r1) + "(?=\d\s)", r2, line)
				line = re.sub(r"" + re.escape(r1) + "(?=\d\d\s)", r2, line)
			elif size == 4:
				line = re.sub(r"" + re.escape(r1) + "(?=\s)", r2, line)
				line = re.sub(r"" + re.escape(r1) + "(?=\d\s)", r2, line)
				line = re.sub(r"" + re.escape(r1) + "(?=\d\d\s)", r2, line)
				line = re.sub(r"" + re.escape(r1) + "(?=\d\d\d\s)", r2, line)
			else :
				line = re.sub(r"" + re.escape(r1) + "(?=\s)", r2, line)

			f2.write(line)

		else:
			f2.write(line)
	f1.close()
	f2.close()

#putting back together
print("> converting to png")
for file in os.listdir(temp_sub_gsvg):
	os.system('convert -background none ' + temp_sub_gsvg + '/' + file + ' ' + temp_sub_png + '/' + file[:-4] + '.png')

#overlaying with old video
print("> reconstructing video file")

final_name = filein[:-4] + "-s-" + str(size) + ".mp4"

os.system("ffmpeg \
	-i " + temp_sub_frames + "/%06d.png \
	-i " + temp_sub_png + "/%06d.png \
	-filter_complex '\
	[0:v]setsar=sar=1/1,format=rgba[glitch];\
	[1:v]setsar=sar=1/1,format=rgba[background];\
	[background][glitch]blend=all_mode=\'normal\'[out];\
	[out]format=rgba' \
	-c:v libx264 " + final_name)

os.system("ffmpeg -i " + final_name + " test" + str(size) + ".png")

shutil.rmtree(temp_dir) 
print("> done")
