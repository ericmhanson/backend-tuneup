#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tuneup assignment"""

__author__ = 'ericmhanson'

import cProfile
import pstats
from functools import wraps
import timeit
from collections import Counter


def profile(func):
    """A function that can be used as a decorator to measure performance"""
    # You need to understand how decorators are constructed and used.
    # Be sure to review the lesson material on decorators, they are used
    # extensively in Django and Flask.
    @wraps(func)
    def inner_wrapper(*args, **kwargs):
        profile = cProfile.Profile()
        profile.enable()
        value = func(*args, **kwargs)
        profile.disable()
        ps = pstats.Stats(profile).strip_dirs().sort_stats('cumulative')
        ps.print_stats(5)
        return value
    return inner_wrapper


def read_movies(src):
    """Returns a list of movie titles"""
    print('Reading file: {}'.format(src))
    with open(src, 'r') as f:
        return f.read().splitlines()


def is_duplicate(title, movies):
    """returns True if title is within movies list"""
    if title in movies:
        return True
    return False


@profile
def find_duplicate_movies(src):
    """Returns a list of duplicate movies from a src list"""
    movies = read_movies(src)
    movie_counter = Counter(movies)
    duplicates = [movie for movie, count in movie_counter.items() if count > 1]
    return duplicates


def timeit_helper():
    """Part A:  Obtain some profiling measurements using timeit"""
    t = timeit.Timer(stmt="find_duplicate_movies('movies.txt')", setup='from\
    main import find_duplicate_movies')
    result = t.repeat(repeat=7, number=5)
    average = min(result)/float(5)
    print('Best time across 7 repeats of 5 runs per repeat:\
          {} sec'.format(average))


def main():
    """Computes a list of duplicate movie entries"""
    result = find_duplicate_movies('movies.txt')
    print('Found {} duplicate movies:'.format(len(result)))
    print('\n'.join(result))
    # timeit_helper()


if __name__ == '__main__':
    main()
