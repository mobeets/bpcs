import logging

def get_log():
    log = logging.getLogger('bpcs-steg')
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    log.addHandler(ch)
    return log

log = get_log()
