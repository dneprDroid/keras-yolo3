file = open('trainer/2012_train.txt', 'r+')
content = file.read()
content = content.replace(r'C:/Users/Alexandr/IdeaProjects/keras-yolo3', 'gs://some_test_bucket-12121212')

file.seek(0)
file.write(content)
file.truncate()
file.close()
