import os

class FileTail:
    def __init__(self, file):
	self.stop = False
        if os.path.isfile(file):
            self.file = open(file, "r");
            self.file_path = file;
            if not self.file:
                raise Exception("Unable to open file %s" % file)
        else:
            raise Exception("%s is not a file " % file)


    def watch (self, callback=None):
        last_size = 0
        last_position = 0
        while not self.stop:

            if last_size != self.getFileSize():
                last_size = self.getFileSize()
                linenumber = 0;
                self.file.seek(last_position, 0)
                for line in self.file.readlines():
                    if linenumber > last_position:
                        last_position = linenumber
                        if callback is None:
                                self.defaultCallback(line)
                        else:
                                callback(line)
                    linenumber+=1
	print "Break from watch"

    def tailfrom (self, line, callback=None):
        self.file.seek(line, 0)
        for line in self.file.readlines():
            if callback is None:
                self.defaultCallback(line)
            else:
                callback(line)

    def getFileSize(self):
        return os.path.getsize(self.file_path);

    def defaultCallback(self, text):
        print text.strip()


