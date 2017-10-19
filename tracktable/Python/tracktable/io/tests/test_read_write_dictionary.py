# Copyright (c) 2017, National Technology & Engineering Solutions of
#   Sandia, LLC (NTESS).
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

# Author: Ben Newton
# Date:   October, 19, 2017

import sys

from tracktable.io.read_write_dictionary import traj_from_dictionary
from tracktable.io.read_write_dictionary import dictionary_from_traj
from tracktable.core import Timestamp
import importlib

domains = ['terrestrial', 'cartesian2d', 'cartesian3d']

def gen_dictionary_and_traj(domainString):
    domain = importlib.import_module("tracktable.domain."+domainString.lower())

    # Manually set up a dictionary which contains trajectory info
    dictionary = {'dimension'     : domain.DIMENSION,
                  'domain'        : domainString,
                  'numProperties' : 3,
                  'propertyNames' : ['altitude', 'heading', 'speed'],
                  'object_id'     : 'AAA001',
                  'timestamps'    : ['2004-12-07 11:36:18',
                                     '2004-12-07 11:37:56',
                                     '2004-12-07 11:39:18'],
                  'coords0'       : [26.995, 27.0447, 27.1136],
                  'property0'     : [2700, 4200, 6700],
                  'property1'     : [108, 108, 225],
                  'property2'     : [0, -27, -22]}
    if domain.DIMENSION > 1:
        dictionary.update({'coords1' : [-81.9731, -81.9844, -82.0458]})
    if domain.DIMENSION > 2:
        dictionary.update({'coords2' : [-100.0, -101.0, -102.0]})

    # Manually set up a matching Trajectory object
    p1 = domain.TrajectoryPoint()
    p1[0] = 26.995;
    if domain.DIMENSION > 1:
        p1[1] = -81.9731
    if domain.DIMENSION > 2:
        p1[2] = -100.0
    p1.set_property('altitude', 2700)
    p1.set_property('heading', 108)
    p1.set_property('speed', 0)
    #p1.__dict__.update({'altitude': 2700})
    #p1.__dict__.update({'heading': 108})
    #p1.__dict__.update({'speed': 0})
    p1.object_id = 'AAA001'
    p1.timestamp = Timestamp.from_string('2004-12-07 11:36:18')

    p2 = domain.TrajectoryPoint()
    p2[0] = 27.0447;
    if domain.DIMENSION > 1:
        p2[1] = -81.9844
    if domain.DIMENSION > 2:
        p2[2] = -101.0
    p2.set_property('altitude', 4200)
    p2.set_property('heading', 108)
    p2.set_property('speed', -27)
    #p2.__dict__.update({'altitude': 4200})
    #p2.__dict__.update({'heading': 108})
    #p2.__dict__.update({'speed': -27})
    p2.object_id = 'AAA001'
    p2.timestamp = Timestamp.from_string('2004-12-07 11:37:56')

    p3 = domain.TrajectoryPoint()
    p3[0] = 27.1136;
    if domain.DIMENSION > 1:
        p3[1] = -82.0458
    if domain.DIMENSION > 2:
        p3[2] = -102.0
    p3.set_property('altitude', 6700)
    p3.set_property('heading', 225)
    p3.set_property('speed', -22)
    #p3.__dict__.update({'altitude': 6700})
    #p3.__dict__.update({'heading': 225})
    #p3.__dict__.update({'speed': -22})
    p3.object_id = 'AAA001'
    p3.timestamp = Timestamp.from_string('2004-12-07 11:39:18')

    traj = domain.Trajectory.from_position_list([p1,p2,p3])

    return dictionary, traj

def test_traj_from_dictionary(domain):
    print "Testing the conversion of a dictionary to a trajectory in the", domain, "domain."
    dictionary, trajExpected = gen_dictionary_and_traj(domain)

    traj = traj_from_dictionary(dictionary)

    if traj != trajExpected:
        print "Error: The", domain, "trajectory generated from dictionary does not match what was expected"
        return 1
    return 0

def test_dictionary_from_traj(domain):
    print "Testing the conversion of a trajectory to a dictionary in the", domain, "domain."
    dictionaryExpected, traj = gen_dictionary_and_traj(domain)

    dictionary = dictionary_from_traj(traj)

    if dictionary != dictionaryExpected:
        print "Error: The", domain, "dictionary generated from the trajectory does not match what was expected"
        return 1
    return 0

def test_dictionary_to_traj_to_dictionary(domain):
    print "Testing the conversion of a dictionary to a trajectory and back to a dictionary in the", domain, "domain."
    dictionary, trajUnused = gen_dictionary_and_traj(domain)

    dictionaryFinal = dictionary_from_traj(traj_from_dictionary(dictionary))

    if dictionary != dictionaryFinal:
        print "Error: The", domain, "dictionary generated from the trajectory generated from a dictionary does not match what was expected"
        return 1
    return 0

def test_traj_to_dictionary_to_traj(domain):
    print "Testing the conversion of a trajectory to a dictionary and back to a trajectory in the", domain, "domain."
    dictionaryUnused, traj = gen_dictionary_and_traj(domain)

    trajFinal = traj_from_dictionary(dictionary_from_traj(traj))

    if traj != trajFinal:
        print "Error: The", domain, "trajectory generated from the dictionary generated from a trajectory does not match what was expected"
        return 1
    return 0

def test_dictionary():
    error_count = 0
    for domain in domains:
        error_count += test_traj_from_dictionary(domain)
        error_count += test_dictionary_from_traj(domain)
        error_count += test_dictionary_to_traj_to_dictionary(domain)
        error_count += test_traj_to_dictionary_to_traj(domain)
    return error_count

def main():
    return test_dictionary()

if __name__ == '__main__':
    sys.exit(main())
