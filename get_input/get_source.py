# -*- coding: utf-8 -*-

import os, time
from os import path, stat
import datetime
from mimetypes import MimeTypes
from pwd import getpwuid
import textract
#from unidecode import unidecode_expect_nonascii
from unidecode import unidecode
class GetText(object):
    def __init__(self, object):
        self.time_stamp = self.timestamp()
        self.source = object
        self.classification = None
        self.full_text = None
        self.classification = self.type_determination(self.source)
    
    def type_determination(self, source):
        if os.path.isfile(self.source):
            classification = "file"
            self.file_handler(source)
        elif isinstance(self.source, str):
            classification = "plaintext"
        elif isinstance(self.source, unicode):
            classification = "unicode"
        else:
            classification = None
        return classification
    def timestamp(self, fmt='%Y-%m-%d %H:%M'):
        """
        Set the date and time a document was uploaded.

        Record the datetime a document is uploaded or
        a paste is submitted.

        returns:
           Data and Time in US format, separated by space.
        """
        return datetime.datetime.now().strftime(fmt)
    def file_handler(self, source):
        self.abs_path = os.path.abspath(source)
        self.file_size = os.path.getsize(self.source)
        self.filename = os.path.basename(self.source)
        self.mime = MimeTypes()
        self.guessed_file_type = self.mime.guess_type(self.source)
        self.file_type = self.guessed_file_type[0]
        self.last_file_mod = time.ctime(os.path.getctime(self.abs_path))
        self.file_owner = getpwuid(os.stat(self.abs_path).st_uid).pw_name
        self.file_extension = os.path.splitext(self.abs_path)[1]
        self.file_access = os.access(self.abs_path, os.R_OK)
        self.read_file(source)

    def read_file(self, source):
        if self.file_access:
            if self.file_type == \
                        "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                self.raw_text = textract.process(source)
            elif self.file_type == "text/plain":
                self.raw_text = open(self.abs_path).read()
            elif self.file_type == 'application/pdf':
                self.raw_text = textract.process(source)
                #self.raw_text_utf = self.raw_text.decode('utf-8', 'ignore')
            elif self.file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                self.raw_text = textract.process(source)
            else:
                print "unknown filetype"
            if self.raw_text:
                self.clean_text = "".join(x for x in self.raw_text if 31 < ord(x) <127)
    
    
