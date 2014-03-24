# encoding: utf-8
# Created by David Rideout <drideout@safaribooksonline.com> on 2/7/14 4:58 PM
# Copyright (c) 2013 Safari Books Online, LLC. All rights reserved.

from storage.models import Book


def process_book_element(book_element):
    """
    Process a book element into the database.

    :param book: book element
    :returns:
    """

    book, created = Book.objects.get_or_create(pk=book_element.get('id'))
    book.title = book_element.findtext('title')
    book.description = book_element.findtext('description')

    for alias in book_element.xpath('aliases/alias'):
        scheme = alias.get('scheme')
        value = alias.get('value')

        book.aliases.get_or_create(scheme=scheme, value=value)

    book.save()

def detect_book_version(book_element):
    """
    return the book version of the book_element passed

    attempt to find the book version by implied usage of '2nd edition' in the book's title
    default is 1.0
    """
    book_version = book_element.findtext('version')
    if not book_version:
        if '2nd edition' in book_element.findtext('title').lower():
            book_version = '2.0'
        else:
            book_version = '1.0'
    return book_version
