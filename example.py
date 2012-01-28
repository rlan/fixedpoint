"""
Copyright (c) 2011, Rick Lan
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
    * Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer in the
      documentation and/or other materials provided with the distribution.
    * Neither the name of the Organization nor the
      names of its contributors may be used to endorse or promote products
      derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER BE LIABLE FOR ANY
DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""


"""
This test bench exercises fixedpoint.py.
There isn't an automated test yet. A visual inspection is needed.
"""

import fixedpoint

def visual_inspection():
    print "[visual_inspection]"

    x = fixedpoint.prop(5, 5, False)
    print "x:", x.format()
    y = fixedpoint.prop(4, 4, False)
    print "y:", y.format()
    
    s1 = x + y
    print "s1 = x + y:", s1.format()
    
    s2 = x - y
    print "s2 = x - y:", s2.format()
    
    nx = -x
    print "nx = -x:", nx.format()
    ny = -y
    print "ny = -y:", ny.format()
    nnx = -nx
    print "nnx = -nx:", nnx.format()
    nny = -ny
    print "nny = -ny:", nny.format()
    
    m1 = x * y
    print "m1 = x * y:", m1.format()
    
    m2 = x * x
    print "m2 = x * x:", m2.format()
    
    sqr_x = x.sqr()
    print "sqr_x = x^2:", sqr_x.format()
    
    sqr_nx = nx.sqr()
    print "sqr_nx = nx^2:", sqr_nx.format()
    
    
    
    a = fixedpoint.prop(4, 3, True)
    print "a:", a.format(), "max", a.max(), "min", a.min(), "smallest", a.smallest()
    b = fixedpoint.prop(3, 0, True)
    print "b:", b.format(), "max", b.max(), "min", b.min(), "smallest", b.smallest()
    c = fixedpoint.prop(3, 0, False)
    print "c:", c.format(), "max", c.max(), "min", c.min(), "smallest", c.smallest()
    
    ab = a + b
    print "ab = a + b:", ab.format()
    print "ab:", ab.format(), "max", ab.max(), "min", ab.min()
    
    ac = a + c
    print "ac = a + b:", ac.format()
    print "ac:", ac.format(), "max", ac.max(), "min", ac.min()


def example_magnitude():
    print "[example_magnitude] cx.real^2 + cx.imag^2"
    
    cx = fixedpoint.prop(10, 9, True)
    print "complex value:", cx.format()
    cx_sqr = cx.sqr()
    print "squared:", cx_sqr.format()
    cx_sum_sqr = cx_sqr + cx_sqr
    print "sum of squares:", cx_sum_sqr.format()

def example_complex_multiply():
    print "[example_complex_multiply] cx1*cx2"
    
    cx1 = fixedpoint.prop(5, 4, True)
    print "cx1:", cx1.format()
    cx2 = fixedpoint.prop(10, 9, True)
    print "cx2:", cx2.format()
    
    """
    cx1 = a+bi
    cx2 = c+di
    cx1*cx2 = (ac-bd)+(bc+ad)i
    """
    mult = cx1*cx2
    print "mult:", mult.format()
    sum = mult + mult
    print "sum:", sum.format()
    


visual_inspection()
example_magnitude()
example_complex_multiply()
