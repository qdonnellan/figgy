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

    book_id = detect_book_id(book_element)
    book, created = Book.objects.get_or_create(pk=book_id)
    book.title = book_element.findtext('title')
    book.description = book_element.findtext('description')
    book.version = detect_book_version(book_element)

    for alias in book_element.xpath('aliases/alias'):
        scheme = alias.get('scheme')
        value = alias.get('value')
        try:
            book.aliases.get_or_create(scheme=scheme, value=value)
        except:
            pass
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

def detect_book_id(book_element):
    """
    return the correct book_id of the book_element passed

    may have to conform the id to the standard "book-N"
    """
    book_id = book_element.get('id')
    if not 'book-' in book_id:
        if detect_book_version(book_element) == '1.0':
            # if the current version is 1.0
            current_book_count = Book.objects.count()
            book_id = 'book-%d' % (current_book_count + 1)
        else:
            # if the current version is anything other than 1.0
            # then we need to find it's parent book id!
            value = None
            for alias in book_element.xpath('aliases/alias'):
                if alias.get('scheme') == 'ISBN-10':
                    # right now, it looks like ISBN-10 is the most stable
                    value = alias.get('value')
            if value:
                book_id = find_book_by_ISBN('ISBN-10', value)
    return book_id

def find_book_by_ISBN(scheme, value):
    """
    return the book id of the book associated with the ISBN scheme and value

    current supports ISBN-10 scheme only
    """
    book_id = None
    if scheme == 'ISBN-10':
        for book in Book.objects.all():
            for alias in book.aliases.all():
                if alias.value == value:
                    book_id = book.id
    return book_id
