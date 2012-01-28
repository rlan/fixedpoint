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


import math


class prop:
    """
    A class for propagation math of fixed-point representation.
    
    Instances of this class support following operations:
      * Add/subtract: z = x + y
      * Multiply: z = x * y
      * Square: z = x.sqr()
      * Absolute value: z = x.abs()
      * Negation: z = -x 
    New representations, z, are derived based on full-precision arithmetic.
    """

    def __init__(self, word_length = 1, integer_length = 1, signed = False):
        """
        Default object is one-bit (ie boolean).
        word_length: in bits and includes sign bit.
        integer_length: number of bits to the left of decimal point, but does not include the sign bit.
        """
        
        if word_length < 1:
            raise ValueError("Word length must be >= 1")
        
        self.word_length = word_length
        self.integer_length = integer_length
        self.signed = signed
        
    def format(self):
        """
        Return a human readable string describing this object.
        Example: us<1, 1> or 2s<10, 9>
        """
        
        msg = "<" + str(self.word_length) + ", " + str(self.integer_length) + ">"
        if self.signed:
            return "2s" + msg
        else:
            return "us" + msg
            
    def max(self):
        """Most positive value"""
        
        fractional_length = self.word_length - self.signed - self.integer_length
        x = 2 ** (self.word_length - self.signed) - 1
        return math.ldexp(x, int(-fractional_length))

    def min(self):
        """Most negative value"""
        
        if self.signed:
            return -2 ** self.integer_length
        else:
            return 0

    def smallest(self):
        """Smallest magnitude for this representation"""
        
        fractional_length = self.word_length - self.signed - self.integer_length
        return 2 ** -fractional_length

    def _create_obj(self, max_value, min_value, fractional_length):
        """
        Convert dynamic range and fractional length to an object instance.
        fractional_length: number of bits to the right of the decimal point.
        """
        
        """
        print "_create_obj:", "max", max_value, "min", min_value, "fractional", fractional_length
        """

        if min_value == 0:
            signed = False
        else:
            signed = True

        log2_max_side = math.log(max_value) / math.log(2)
        if math.ceil(log2_max_side)==log2_max_side:
            log2_max_side = log2_max_side + 1  # because max positive value of x bits is only 2^x - 1 
            
        if min_value ==  0:
            log2_min_side = -128 # smaller than any 128-bit integer operation
        else:
            log2_min_side = math.log(-min_value) / math.log(2)
        integer_length = int( math.ceil(max(log2_max_side, log2_min_side)) )

        word_length = signed + integer_length + fractional_length
        
        return prop(word_length, integer_length, signed)
        
    
    def __abs__(self):
        """Return the representation for f(x) = abs(x)"""
        
        if self.signed:
            return prop(self.word_length, self.integer_length+1, False)
        else:
            return self

    def __neg__(self):
        """Return the representation for f(x) = -x"""
        
        if self.signed:
            return prop(self.word_length+1, self.integer_length+1, self.signed)
        else:
            return prop(self.word_length+1, self.integer_length, True)

    def sqr(self):
        """Return the representation for f(x) = x^2"""

        integer_length = 2 * self.integer_length
        if self.signed:
            integer_length = integer_length + 1
        fractional_length = 2 * (self.word_length - self.signed - self.integer_length)
        word_length = integer_length + fractional_length
        return prop(word_length, integer_length, False)

    def __add__(self, other):
        """Return the representation for f(x, y) = x + y"""

        max_value = self.max() + other.max()
        min_value = self.min() + other.min()

        self_fl = self.word_length - self.signed - self.integer_length
        other_fl = other.word_length - other.signed - other.integer_length
        fractional_length = max(self_fl, other_fl)
        
        return self._create_obj(max_value, min_value, fractional_length)
        
    def __sub__(self, other):
        """Return the representation for f(x, y) = x - y"""

        max_value = self.max() - other.min()
        min_value = self.min() - other.max()
        
        self_fl = self.word_length - self.signed - self.integer_length
        other_fl = other.word_length - other.signed - other.integer_length
        fractional_length = max(self_fl, other_fl)
        
        return self._create_obj(max_value, min_value, fractional_length)

    def __mul__(self, other):
        """
        Return the representation for f(x, y) = x * y
        Use the sqr() method for squaring.
        """
        
        max_value = max(self.max() * other.max(), self.min() * other.min())
        min_value = min(self.max() * other.min(), self.min() * other.max())
        
        self_fl = self.word_length - self.signed - self.integer_length
        other_fl = other.word_length - other.signed - other.integer_length
        fractional_length = self_fl + other_fl
        
        return self._create_obj(max_value, min_value, fractional_length)
