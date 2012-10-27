import dateutil.parser


def extract_timestamp(string, ignoretz=True):
    """
    Create a datetime object from `string`.
    """
    return dateutil.parser.parse(string, ignoretz=ignoretz)
