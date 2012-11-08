#! /bin/sh
# checks for report created with createzopecoverage and evaluate the result

MINIMUM=80
REPORT="coverage/reports/all.html"

if [ ! -f ${REPORT} ]; then
    echo "No test coverage report present; skipping test coverage validation"
    exit 0
fi

# find first percentage value in file (module test coverage) and return it
COVERAGE=`grep "[0-9]\{1,3\}[%]" ${REPORT} -m 1 -o | grep "[0-9]\{1,3\}" -o`

if [ ${COVERAGE} -lt ${MINIMUM} ]; then
    echo "Insufficient test coverage"
    exit 1
else
    exit 0
fi
