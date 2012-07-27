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


class prop(object):
    """
    A class for propagation math of fixed-point representation.
    
    Instances of this class support following operations:
      * Add/subtract: z = x + y
      * Multiply: z = x * y
      * Square: z = x.sqr()
      * Absolute value: z = x.abs()
      * Negation: z = -x 
    New representations, z, are derived based on full-precision arithmetic.
    
    Example: magnitude squared of a complex number, i.e., cx.real^2 + cx.imag^2
    >>> import fixedpoint
    >>> cx = fixedpoint.prop(10, 9, True)
    >>> cx_sqr = cx.sqr()
    >>> cx_sqr.format()
    'us<19, 19>'
    >>> cx_sum_sqr = cx_sqr + cx_sqr
    >>> cx_sum_sqr.format()
    'us<20, 20>'

    Example: complex multiplication.
    cx = a+bi
    cy = c+di
    cx*cy = (ac-bd)+(bc+ad)i
    
    >>> import fixedpoint
    >>> cx = fixedpoint.prop(5, 4, True)
    >>> cy = fixedpoint.prop(10, 9, True)
    >>> mult = cx*cy
    >>> mult.format()
    '2s<15, 14>'
    >>> result = mult + mult
    >>> result.format()
    '2s<16, 15>'
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
        @return: a human readable string describing this object.

        >>> import fixedpoint
        >>> fixedpoint.prop(4, 3, True).format()
        '2s<4, 3>'
        >>> fixedpoint.prop(3, 0, False).format()
        'us<3, 0>'
        """
        
        msg = "<" + str(self.word_length) + ", " + str(self.integer_length) + ">"
        if self.signed:
            return "2s" + msg
        else:
            return "us" + msg
        
    def max(self):
        """
        @return: the most positive value.
        
        >>> import fixedpoint
        >>> fixedpoint.prop(4,3,True).max()
        7.0
        >>> fixedpoint.prop(3,0,True).max()
        0.75
        >>> fixedpoint.prop(3,0,False).max()
        0.875
        """
        
        fractional_length = self.word_length - self.signed - self.integer_length
        x = 2 ** (self.word_length - self.signed) - 1
        return math.ldexp(x, int(-fractional_length))

    def min(self):
        """
        @return: the most negative value or zero if unsigned.

        >>> import fixedpoint
        >>> fixedpoint.prop(4,3,True).min()
        -8
        >>> fixedpoint.prop(3,0,True).min()
        -1
        >>> fixedpoint.prop(3,0,False).min()
        0
        """
        
        if self.signed:
            return -2 ** self.integer_length
        else:
            return 0

    def smallest(self):
        """
        @return: the smallest magnitude for this representation.

        >>> import fixedpoint 
        >>> fixedpoint.prop(4,3,True).smallest()
        1
        >>> fixedpoint.prop(3,0,True).smallest()
        0.25
        >>> fixedpoint.prop(3,0,False).smallest()
        0.125
        """
        
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
        """
        @return: the representation for f(x) = abs(x)
        
        todo doctest
        """
        
        if self.signed:
            return prop(self.word_length, self.integer_length+1, False)
        else:
            return self

    def __neg__(self):
        """
        @return: the representation for f(x) = -x

        >>> import fixedpoint 
        >>> x = fixedpoint.prop(5, 5, False)
        >>> x.format()
        'us<5, 5>'
        >>> nx = -x
        >>> nx.format()
        '2s<6, 5>'
        >>> y = fixedpoint.prop(4, 4, True)
        >>> y.format()
        '2s<4, 4>'
        >>> ny = -y
        >>> ny.format()
        '2s<5, 5>'
        """
        
        if self.signed:
            return prop(self.word_length+1, self.integer_length+1, self.signed)
        else:
            return prop(self.word_length+1, self.integer_length, True)

    def sqr(self):
        """
        @return: the representation for f(x) = x^2
        
        >>> import fixedpoint
        >>> x = fixedpoint.prop(5, 5, False)
        >>> sqr_x = x.sqr()
        >>> sqr_x.format()
        'us<10, 10>'
        >>> nx = -x
        >>> sqr_nx = nx.sqr()
        >>> sqr_nx.format()
        'us<11, 11>'

        todo overload the "**" operator
        """

        integer_length = 2 * self.integer_length
        if self.signed:
            integer_length = integer_length + 1
        fractional_length = 2 * (self.word_length - self.signed - self.integer_length)
        word_length = integer_length + fractional_length
        return prop(word_length, integer_length, False)

    def __add__(self, other):
        """
        @return: the representation for f(x, y) = x + y
        
        >>> import fixedpoint 
        >>> x = fixedpoint.prop(5, 5, False)
        >>> y = fixedpoint.prop(4, 4, False)
        >>> z = x + y
        >>> z.format()
        'us<6, 6>'
        >>> a = fixedpoint.prop(4, 3, True)
        >>> b = fixedpoint.prop(3, 0, True)
        >>> c = a + b
        >>> c.format()
        '2s<7, 4>'
        """

        max_value = self.max() + other.max()
        min_value = self.min() + other.min()

        self_fl = self.word_length - self.signed - self.integer_length
        other_fl = other.word_length - other.signed - other.integer_length
        fractional_length = max(self_fl, other_fl)
        
        return self._create_obj(max_value, min_value, fractional_length)
        
    def __sub__(self, other):
        """
        @return: the representation for f(x, y) = x - y
        
        >>> import fixedpoint 
        >>> x = fixedpoint.prop(5, 5, False)
        >>> y = fixedpoint.prop(4, 4, False)
        >>> z = x - y
        >>> z.format()
        '2s<6, 5>'
        >>> a = fixedpoint.prop(4, 3, True)
        >>> b = fixedpoint.prop(3, 0, True)
        >>> c = a - b
        >>> c.format()
        '2s<7, 4>'
        """

        max_value = self.max() - other.min()
        min_value = self.min() - other.max()
        
        self_fl = self.word_length - self.signed - self.integer_length
        other_fl = other.word_length - other.signed - other.integer_length
        fractional_length = max(self_fl, other_fl)
        
        return self._create_obj(max_value, min_value, fractional_length)

    def __mul__(self, other):
        """
        @return: the representation for f(x, y) = x * y.
        @note: Use the sqr() method for squaring.
        
        >>> import fixedpoint
        >>> x = fixedpoint.prop(5, 5, False)
        >>> y = fixedpoint.prop(4, 4, False)
        >>> m = x * y
        >>> m.format()
        'us<9, 9>'
        >>> a = fixedpoint.prop(4, 3, True)
        >>> b = fixedpoint.prop(3, 0, True)
        >>> c = a * b
        >>> c.format()
        '2s<7, 4>'
        """
        max_value = max(self.max() * other.max(), self.min() * other.min())
        min_value = min(self.max() * other.min(), self.min() * other.max())
        
        self_fl = self.word_length - self.signed - self.integer_length
        other_fl = other.word_length - other.signed - other.integer_length
        fractional_length = self_fl + other_fl
        
        return self._create_obj(max_value, min_value, fractional_length)


class q(object):
    """
    A fixed-point quantizer.
    
    Convert unsigned integer to floating-point by using the fixed-point format
    given. See examples in float()
    """
    
    def __init__(self, word_length = 1, integer_length = 1, signed = False):
        """
        Default object is one-bit (ie boolean).
        @param word_length: in bits and includes sign bit.
        @param integer_length: number of bits to the left of decimal point, but does not include the sign bit.
        @param signed: False (default) if unsigned number system. True of signed.
        """
        
        if word_length < 1:
            raise ValueError("Word length must be >= 1")
        
        self.word_length = word_length
        self.integer_length = integer_length
        self.signed = signed

    def float(self, uint_val):
        """
        Converts unsigned integer (raw) to floating-point value using fixed-point format of the current object.
        @param uint_val: Unsigned int to convert.
        @return: A floating-point value.

        Examples:
        >>> import fixedpoint
        >>> q=fixedpoint.q(4,2,False)
        >>> for i in range(0,16): print(i, q.float(i))
        0 0.0
        1 0.25
        2 0.5
        3 0.75
        4 1.0
        5 1.25
        6 1.5
        7 1.75
        8 2.0
        9 2.25
        10 2.5
        11 2.75
        12 3.0
        13 3.25
        14 3.5
        15 3.75
        
        >>> import fixedpoint
        >>> q=fixedpoint.q(4,2,True)
        >>> for i in range(0,16): print(i, q.float(i))
        0 0.0
        1 0.5
        2 1.0
        3 1.5
        4 2.0
        5 2.5
        6 3.0
        7 3.5
        8 -4.0
        9 -3.5
        10 -3.0
        11 -2.5
        12 -2.0
        13 -1.5
        14 -1.0
        15 -0.5
        """
        
        if uint_val < 0:
            raise ValueError("Value must be non-negative!")
        if uint_val > 2**self.word_length - 1:
            raise ValueError("Value must be <= "+str(2**self.word_length-1))
        
        if self.signed and (uint_val >= 2**(self.word_length-1)):
            uint_val = uint_val - 2**self.word_length
            
        if self.signed:
            fractional = self.word_length - 1 - self.integer_length
        else:
            fractional = self.word_length - self.integer_length
            
        return uint_val * (2**(-fractional))
        

if __name__ == "__main__":
    import doctest
    doctest.testmod()
