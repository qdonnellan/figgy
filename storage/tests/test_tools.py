# encoding: utf-8
# Created by David Rideout <drideout@safaribooksonline.com> on 2/7/14 5:01 PM
# Copyright (c) 2013 Safari Books Online, LLC. All rights reserved.

from django.test import TestCase
from lxml import etree
from storage.models import Book, Alias
import storage.tools


class TestTools(TestCase):
    def setUp(self):
        pass

    def test_storage_tools_process_book_element_db(self):
        '''process_book_element should put the book in the database.'''

        xml_str = '''
        <book id="12345">
            <title>A title</title>
            <aliases>
                <alias scheme="ISBN-10" value="0158757819"/>
                <alias scheme="ISBN-13" value="0000000000123"/>
            </aliases>
        </book>
        '''

        xml = etree.fromstring(xml_str)
        storage.tools.process_book_element(xml)

        self.assertEqual(Book.objects.count(), 1)
        book = Book.objects.get(pk='12345')

        self.assertEqual(book.title, 'A title')
        self.assertEqual(book.aliases.count(), 2)
        self.assertEqual(Alias.objects.get(scheme='ISBN-10').value, '0158757819')
        self.assertEqual(Alias.objects.get(scheme='ISBN-13').value, '0000000000123')

    def test_detect_book_id_function_with_good_input(self):
        """
        detect_book_id(book_element) should return "book-N" where N is an integer
        """
        book_data = "<book id='book-1'><title>A title</title></book>"
        book_xml = etree.fromstring(book_data)
        book_id = storage.tools.detect_book_id(book_xml)
        self.assertEqual(book_id, 'book-1')
    def test_detect_book_id_function_with_bad_book_id_and_no_reference(self):
        """
        pass a book with no book id and no reference to any other books in the database

        (in this case, there is no other book in the database), the book id should be "book-1"
        """
        book_data = "<book id='FOOFOOSAFARIBOOKS'><title>A title</title></book>"
        book_xml = etree.fromstring(book_data)
        book_id = storage.tools.detect_book_id(book_xml)
        self.assertEqual(book_id, 'book-1')
