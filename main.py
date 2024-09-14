import os
import exifread
import simplekml

def _convert_to_degress(value):
   d = float(value.values[0].num) / float(value.values[0].den)
   m = float(value.values[1].num) / float(value.values[1].den)
   s = float(value.values[2].num) / float(value.values[2].den)
   return d + (m / 60.0) + (s / 3600.0)


i = 0
j = 0
kml = simplekml.Kml()
folder = "C:\\Users\\A43X\\Pictures\\Шелякин_Компьютер"

for root, dirs, files in os.walk(folder):
   for file in files:
      if file.endswith(".jpg") or file.endswith(".jpeg"):
         print(os.path.join(root, file))
         i=i+1

         # Open image file for reading (binary mode)
         path_name = os.path.join(root, file)
         f = open(path_name, 'rb')

         # Return Exif tags
         tags = exifread.process_file(f)

         #for tag in tags.keys():
            #if tag not in ('JPEGThumbnail', 'TIFFThumbnail', 'Filename', 'EXIF MakerNote'):
               #print(str(tag) + ' =  ' + str(tags[tag]))
         try:
            latitude = tags.get('GPS GPSLatitude')
            latitude_ref = tags.get('GPS GPSLatitudeRef')
            longitude = tags.get('GPS GPSLongitude')
            longitude_ref = tags.get('GPS GPSLongitudeRef')
         except:
            latitude = None
            latitude_ref = None
            longitude = None
            longitude_ref = None


         if latitude==None or longitude==None:
            j=j+0
         else:
            j=j+1

            print(str(latitude) + str(latitude_ref))
            print(str(longitude) + str(longitude_ref))

            if latitude:
               lat_value = _convert_to_degress(latitude)
               if latitude_ref.values != 'N':
                  lat_value = -lat_value

            if longitude:
               lon_value = _convert_to_degress(longitude)
               if longitude_ref.values != 'E':
                  lon_value = -lon_value
            print(lat_value)
            print(lon_value)
            kml.newpoint(name=str(file), coords=[(lon_value, lat_value)])

print ('-------------------------------------------')
print ('Общее кол-во файлов *.jpg/*.jpeg, найденных в папке: '+str(i))
print ('Кол-во файлов c координатами в EXIF: '+str(j))
kml.save("photo.kml")

