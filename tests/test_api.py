import unittest
from website import views



def test_test():
    assert views.api_trip(33, 'San Diego,Ca', 'Las Vegas,Nv')