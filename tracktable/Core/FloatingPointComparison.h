/*
 * Copyright (c) 2014-2017 National Technology and Engineering
 * Solutions of Sandia, LLC. Under the terms of Contract DE-NA0003525
 * with National Technology and Engineering Solutions of Sandia, LLC,
 * the U.S. Government retains certain rights in this software.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions
 * are met:
 *
 * 1. Redistributions of source code must retain the above copyright
 * notice, this list of conditions and the following disclaimer.
 *
 * 2. Redistributions in binary form must reproduce the above copyright
 * notice, this list of conditions and the following disclaimer in the
 * documentation and/or other materials provided with the distribution.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
 * "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
 * LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
 * A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
 * HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
 * SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
 * LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
 * DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
 * THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 * (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
 * OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 */


// We need a robust way to compare floating point numbers for almost-equality

// \defgroup Tracktable_CPP C++ components of Tracktable


#ifndef __tracktable_floating_point_comparison_h
#define __tracktable_floating_point_comparison_h

#include <boost/test/floating_point_comparison.hpp>
#include <cmath>
#include <limits>

namespace tracktable {

namespace settings {

const double EQUALITY_RELATIVE_TOLERANCE=1e-5;
const double ZERO_ABSOLUTE_TOLERANCE=1e-5;

}

// ----------------------------------------------------------------------

template<typename T>
bool almost_zero(
  T z,
  T epsilon=settings::EQUALITY_RELATIVE_TOLERANCE
  )
{
  return (std::abs(z) < epsilon);
}

// ----------------------------------------------------------------------

template<typename T>
bool almost_equal(
  T a, T b,
  T tolerance=settings::EQUALITY_RELATIVE_TOLERANCE
  )
{
  T abs_a = std::abs(a);
  T abs_b = std::abs(b);
  T diff = std::abs(a-b);

#if defined (__clang__)
#pragma clang diagnostic push
#pragma clang diagnostic ignored "-Wfloat-equal"
#endif
  if (a == b) // shortcut, handles infinities
    {
    return true;
    }
  else if (a == 0 || b == 0 || diff < std::numeric_limits<T>::epsilon())
    {
    // Either they're both close to zero or one of them actually is
    // zero.  Relative error is less meaningful here.
    return (diff < tolerance * std::numeric_limits<T>::min());
    }
  else
    {
    // use relative error
    return (diff / (abs_a + abs_b)) < tolerance;
    }
#if defined (__clang__)
#pragma clang diagnostic pop
#endif
}

} // close namespace tracktable

#endif
