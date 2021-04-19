import os

fileNumToDelete = []

makeup_images = []
makeup_segs = []
non_images = []
non_segs = []
makeup_land = []
non_land = []

count = 0
for filename in os.listdir('./data/images/makeup'):
	if count % 2 == 0:
		imagesPath = os.path.join('./data/images/makeup', filename)
		makeup_images.append(imagesPath)
		nonPath = os.path.join('./data/segs/makeup', filename)
		makeup_segs.append(nonPath)
		landPath = os.path.join('./data/landmarks/makeup', filename)
		makeup_land.append(landPath)

	count += 1

count = 0
for filename in os.listdir('./data/images/non-makeup'):
	if count % 2 == 0:
		imagesPath2 = os.path.join('./data/images/non-makeup', filename)
		non_images.append(imagesPath2)
		nonPath2 = os.path.join('./data/segs/non-makeup', filename)
		non_segs.append(nonPath2)
		landPath2 = os.path.join('./data/landmarks/non-makeup', filename)
		non_land.append(landPath2)

	count += 1



print(makeup_images)
for item in makeup_images:
	os.remove(item)

for item in makeup_segs:
	os.remove(item)

for item in non_images:
	os.remove(item)
	
for item in non_segs:
	os.remove(item)

for item in makeup_land:
	os.remove(item)

for item in non_land:
	os.remove(item)