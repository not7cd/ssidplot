import re
import subprocess
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

cellNumberRe = re.compile(r"^Cell\s+(?P<cellnumber>.+)\s+-\s+Address:\s(?P<mac>.+)$")
regexps = [
    re.compile(r"^ESSID:\"(?P<essid>.*)\"$"),
    re.compile(r"^Protocol:(?P<protocol>.+)$"),
    re.compile(r"^Mode:(?P<mode>.+)$"),
    re.compile(r"^Frequency:(?P<frequency>[\d.]+) (?P<frequency_units>.+) \(Channel (?P<channel>\d+)\)$"),
    re.compile(r"^Encryption key:(?P<encryption>.+)$"),
    re.compile(r"^Quality=(?P<signal_quality>\d+)/(?P<signal_total>\d+)\s+Signal level=(?P<signal_level_dBm>.+) d.+$"),
    re.compile(r"^Signal level=(?P<signal_quality>\d+)/(?P<signal_total>\d+).*$"),
]

# Runs the comnmand to scan the list of networks.
# Must run as super user.
# Does not specify a particular device, so will scan all network devices.
def scan(interface='wlan0'):
    logger.info('scanning %s', interface)
    cmd = ["iwlist", interface, "scan"]
    logger.info('spawning iwlist process')
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    points = proc.stdout.read().decode('utf-8')
    return points

# Parses the response from the command "iwlist scan"
def parse(content):
    logger.info('parsing')
    cells = []
    lines = content.split('\n')
    for line in lines:
        line = line.strip()
        logger.debug('parsing line: %s', line)
        cellNumber = cellNumberRe.search(line)
        if cellNumber is not None:
            logger.debug('found network %s', cellNumber.groupdict())
            cells.append(cellNumber.groupdict())
            continue
        for expression in regexps:
            result = expression.search(line)
            if result is not None:
                logger.debug('found %s', result.groupdict())
                cells[-1].update(result.groupdict())
                continue
    return cells