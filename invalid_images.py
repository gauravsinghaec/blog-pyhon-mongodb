import pymongo
from datetime import datetime
import sys

connection_string = "mongodb://devUser:12345@localhost:27017/photosharing"
connection = pymongo.MongoClient(connection_string)
print connection
database = connection.photosharing
albums = database.albums
images = database.images

def get_orphan_images():
	image_cursor = images.find().sort('_id', direction=1)
	orphan_images = []
	print "Start : " + str(datetime.utcnow())
	for img in image_cursor:
		result = albums.find_one({"images": img['_id']})
		if not result:
			orphan_images.append(img['_id'])
	if len(orphan_images):
		try:
			response = images.delete_many({"_id":{"$in": orphan_images}})
		except:
			print "Could not delete from the collection, error"
			print "Unexpected error:", sys.exc_info()[0]
			return len(orphan_images)
	print "End : " + str(datetime.utcnow())
	return len(orphan_images),response.deleted_count

orphan_count,deleted_count = get_orphan_images()
print orphan_count,deleted_count