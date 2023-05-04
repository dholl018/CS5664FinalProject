import json
import re

from typing import Tuple


class MovieRecord:
    productId: str = None
    userId: str = None
    profileName: str = None
    helpfulness: str = None
    score: str = None
    time: str = None
    summary: str = None
    text: str = None

    def validate_self(self) -> bool:
        if not self.productId:
            print('No productId')
            return False
        if not self.userId:
            print('No userId')
            return False
        if not self.profileName:
            print('No profileName')
            return False
        if not self.helpfulness:
            print('No helpfulness')
            return False
        if not self.score:
            print('No score')
            return False
        if not self.time:
            print('No time')
            return False
        # if not self.summary:
        #     print('No summary')
        #     return False
        if not self.text:
            print('No text')
            return False

        return True

    def __str__(self):
        return f'{self.productId}|{self.userId}|{self.profileName}|{self.helpfulness}|{self.score}|{self.time}|{self.summary}|{self.text}'

    def as_dict(self):
        return {
            'productId': self.productId,
            'userId': self.userId,
            'profileName': self.profileName,
            'helpfulness': self.helpfulness,
            'score': self.score,
            'time': self.time,
            'summary': self.summary,
            'text': self.text
        }


def get_lines():
    with open('data/movies.txt', errors='replace') as f:
        full_line = ''
        for line in f:
            line = line.strip()
            if not line or line == '':
                # end of record
                yield full_line
                full_line = ''
            elif re.search(r'^\w+/\w+', line):
                # yield previous full line
                yield full_line

                # now start a new one
                full_line = line


def get_field_date(line: str) -> Tuple[str, str]:
    match = re.search(r'\w+/(\w+): (.+)', line)
    try:
        return match[1], match[2]
    except TypeError as e:
        print(f'Failing line: {line}')
        raise


def parse():
    with open('data/movies-formatted.txt', 'w', encoding='utf-8') as target:
        # target.write('productId|userId|profileName|helpfulness|score|time|summary|text\n')
        # with open('data/movies.txt', errors='replace') as f:
        record = MovieRecord()
        # for line in f:
        for line in get_lines():
            line = line.strip()
            line = line.strip('\n')
            if not line or line == '':
                if not record.validate_self():
                    print(f'Record invalid: {record}')
                else:
                    target.write(f'{json.dumps(record.as_dict())}\n')
                    record = MovieRecord()
            else:
                try:
                    parsed_data = get_field_date(line)
                    record.__setattr__(parsed_data[0], parsed_data[1])
                except TypeError:
                    print(f'got type error for line: {line}')


if __name__ == '__main__':
    parse()
