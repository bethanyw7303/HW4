#
# (c) 2023 Michael Fitzgerald (mpfitz@ucla.edu)
#
# Some code for querying Simbad for making a target list.
#


from astroquery.simbad import Simbad
Simbad.add_votable_fields('ra','dec')
import logging
_log = logging.getLogger('hw4prob1')

#M2, M45, HD 189733, 3C 273, NGC 1068, AU Mic, TRAPPIST-1
#target name & J2000 RA and Dec coords
def format_target_list(target_list):
    """Query Simbad for list of identifiers; returns dictionary with RA and Dec strings"""

    # an empty dictionary to hold our output
    target_info = {}
    
    # get the Simbad query for M45 (the Pleiades)
    for target_name in target_list:
        _log.debug('querying {}'.format(target_name))
        result_table = Simbad.query_object(target_name)
        print(result_table)

        # report on results
        n_result = len(result_table)
        _log.info('{}: {} objects found'.format(target_name, n_result))
        if n_result == 0:
            _log.warning('skipping....')
            continue
        if n_result > 1:
            _log.warning('using first result')

        # store RA and DEC strings as tuple for this object
        ra = result_table[0]["RA"]
        print(ra)

        dec = result_table[0]["DEC"]
        target_info[target_name] = (ra, dec)
    # sort dictionary by the "value" (ra,dec)
    target_info = dict(sorted(target_info.items(), key=lambda x:x[1]))

    return target_info


if __name__ == '__main__':

    # set up logging output
    #logging.basicConfig(level=logging.INFO,
    logging.basicConfig(level=logging.INFO,
                        format='%(name)-12s: %(levelname)-8s %(message)s',
                        )

    # define target list
    target_list = ['M2',
                   'M45',
                   'HD 189733',
                   '3C 273',
                   'NGC 1068',
                   'AU Mic',
                   'TRAPPIST-1'
                   ]

    target_info = format_target_list(target_list)

    # output results to nicely formatted file
    output_fn = 'target_list.txt'
    with open(output_fn, 'w') as f:
        for tn, (ra, dec) in target_info.items():
            # print the output to file
            #   See https://docs.python.org/3/tutorial/inputoutput.html for string
            #   formatting for the fixed-width output
            #s = 'Target {0: 20} with J2000 coordinates (RA, DEC): {1: 15}, {2: 15}.\n'.format(tn, (ra, dec))
            print(f"Target {tn} with J2000 coordinates (RA, DEC): {(ra, dec)}. \n", file=f)

#fixed width output: name is 20 char wide string, ra and dec printed as 15 char wide strings.
    # one target per line