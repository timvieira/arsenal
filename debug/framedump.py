import sys, traceback

# TIMV: would it be possibe to change this function to work without raising
#       and exception?
def framedump():
    """
    Print the usual traceback information, followed by a listing of all the
    local variables in each frame.

    Note: this function does not work when there is no exception.
    """

    # Move to the frame where the exception occurred, which is often not the
    # same frame where the exception was caught.
    tb = sys.exc_info()[2]
    while 1:
        if not tb.tb_next:
            break
        tb = tb.tb_next

    # get the stack frames
    stack = []
    f = tb.tb_frame
    while f:
        stack.append(f)
        f = f.f_back
    stack.reverse()

    print 'Traceback:'
    print '=========='
    print traceback.format_exc()

    print 'Locals by frame:'
    print '================'
    for frame in stack:
        print 'Frame %s in %s at line %s' % (frame.f_code.co_name,
                                             frame.f_code.co_filename,
                                             frame.f_lineno)
        for key, value in frame.f_locals.iteritems():
            print '\t%10s = %r' % (key, value)

        print
        print


if __name__ == '__main__':

    def example():
        """
        A simple example where this approach comes in handy.

        Basically, we have a simple function which manipulates all the
        strings in a list. The function doesn't do any error checking, so when
        we pass a list which contains something other than strings, we get an
        error.
        """

        data = ["1", "2", 3, "4"]  # Typo: We 'forget' the quotes on data[2]
        def pad4(seq):
            """Pad each string in seq with zeros, to four places."""
            return_value = []
            for thing in seq:
                return_value.append("0" * (4 - len(thing)) + thing)
            return return_value

        print '============================================================'
        print 'The usual information'
        print '============================================================'
        # First, show the information we get from a normal traceback.print_exc().
        try:
            pad4(data)
        except:
            traceback.print_exc()

        print
        print '============================================================'
        print 'Tracebacks with the frame dump'
        print '============================================================'

        # With our new function it is to see the bad data that
        # caused the problem. The variable 'thing' has the value 3, so we know
        # that the TypeError we got was because of that. A quick look at the
        # value for 'data' shows us we simply forgot the quotes on that item.
        try:
            pad4(data)
        except:
            framedump()

    example()
