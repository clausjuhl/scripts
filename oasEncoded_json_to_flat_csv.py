import csv
import json
from pathlib import Path

"""
USECASE: Brug til at konvertere oas-encoded json-data:
    'oasDictText' fra '{date}_oas_backup.csv'
    'oasDataJsonEncoded' fra et registreringsjob, som skal ændres. flyttes...

Begge er json-encoded dicts, som skal nivelleres, og som derefter kan importeres til SAM

NOTES:
    Virker kun på ET(!) niveau
    Hvis man arbejder med digitale registreringer, skal filnavne og -placeringer huskes på!

oasDataJsonEncoded/oasDictText til SAM:
    'related_content' -> 'skematype'
    'identifier' -> 'UnikID'
    'schema' -> 'skemaversion'

Omdøb alle extracted dict-keys, da kolonnerne navngives med dict-navnet plus __ plus navn
"""

INFILE = "PR_proofread.csv"
OUTFILE_STEM = "PR"
CHUNK_SIZE = 1000  # Hvor mange entiteter skal processeres ad gangen


def main():
    # vars to reset after each outfile is written
    chunk_counter = 1
    counter = 0
    output = []
    headers = []

    def generate_file(data):
        # data is a list of dicts
        OUTFILE = Path(OUTFILE_STEM + "_" + str(chunk_counter) + "_" + "_" + str(counter) + ".csv")
        with open(OUTFILE, 'w', newline='', encoding='utf8') as ofile:
            writer = csv.DictWriter(ofile, fieldnames=sorted(headers))
            writer.writeheader()
            for row in data:
                writer.writerow(row)

    with open(Path(INFILE)) as ifile:
        for d in csv.DictReader(ifile):
            _d = {}  # out-dict
            entity = json.loads(d.get('oasDataJsonEncoded'))  # in-dict
            # entity = json.loads(d.get('oasDictText'))  # in-dict

            for k, v in entity.items():
                if isinstance(v, list):
                    # generate column for each index in list
                    temp_headers = [k + "_index_" + str(i) for i in range(len(v))]
                    [headers.append(h) for h in temp_headers if h not in headers]
                    # add data to out-dict
                    for i in range(len(v)):
                        _d[k + "_index_" + str(i)] = v[i]

                elif isinstance(v, dict):
                    # generate colum for each dict-key
                    temp_headers = [k + "__" + _k for _k in v.keys()]
                    [headers.append(h) for h in temp_headers if h not in headers]
                    # add data to out-dict
                    for _k in v.keys():
                        _d[k + "__" + _k] =  v.get(_k)

                else:
                    # Strings, bools, ints, floats...
                    # generate column if key not in headers already
                    if k not in headers:
                        headers.append(k)
                    # add data to out-dict
                    _d[k] = v

            output.append(_d)
            counter += 1

            if counter == CHUNK_SIZE:
                # save to outfile
                generate_file(output)
                # reset all counters
                chunk_counter += 1
                counter = 0
                output = []
                headers = []

        # finally, save any leftover-entities to outfile
        generate_file(output)


if __name__ == '__main__':
    main()
